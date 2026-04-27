#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:38:23 2026

@author: jessicaschipper
"""

import os
import streamlit as st
from Bio import Entrez
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

os.environ["OPENAI_API_KEY"] = ""

Entrez.email = "your_email_here

# ---- PAGE CONFIG ----
st.set_page_config(page_title="PubMed Research Assistant", page_icon="🔬")
st.title("PubMed Research Assistant")
st.caption("Ask questions answered by real published research")

# ---- SIDEBAR: SEARCH SETTINGS ----
st.sidebar.header("Search Settings")
search_query = st.sidebar.text_input(
    "PubMed search topic",
    value="CRISPR Cas9 gene editing keratinocytes"
)
max_results = st.sidebar.slider("Number of papers", min_value=5, max_value=20, value=10)
load_button = st.sidebar.button("Load Papers")

# ---- SESSION STATE ----
if "chain" not in st.session_state:
    st.session_state.chain = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "papers_loaded" not in st.session_state:
    st.session_state.papers_loaded = False

# ---- FETCH + BUILD RAG ----
def fetch_and_build(query, max_results):
    search = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    ids = Entrez.read(search)["IdList"]

    if not ids:
        raise ValueError("No PubMed results found. Try different search terms.")

    docs = []
    for pmid in ids:
        try:
            fetch = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
            text = fetch.read()
            if isinstance(text, bytes):
                text = text.decode("utf-8")
            text = text.strip()
            if len(text) > 100:
                docs.append(Document(
                    page_content=text,
                    metadata={"pmid": pmid}
                ))
        except Exception as e:
            print(f"Skipping {pmid}: {e}")
            continue

    if not docs:
        raise ValueError("Could not retrieve any abstracts.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    chunks = [c for c in chunks if c.page_content and len(c.page_content.strip()) > 50]

    if not chunks:
        raise ValueError("No usable content found.")

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_template("""
You are a scientific research assistant. Answer the question 
using only the research abstracts provided as context.
If the context doesn't contain enough information, say so.
Cite the paper titles when relevant.

Context:
{context}

Question: {question}
""")
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    return chain, len(docs)
# ---- LOAD PAPERS BUTTON ----
if load_button:
    with st.spinner(f"Fetching papers from PubMed..."):
        chain, num_papers = fetch_and_build(search_query, max_results)
        st.session_state.chain = chain
        st.session_state.papers_loaded = True
        st.session_state.messages = []
    st.sidebar.success(f"Loaded {num_papers} papers!")

# ---- CHAT INTERFACE ----
if st.session_state.papers_loaded:
    st.divider()
    st.subheader("Ask a question")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if question := st.chat_input("e.g. How is CRISPR used to treat skin conditions?"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching papers..."):
                answer = st.session_state.chain.invoke(question)
            st.write(answer.content)
            st.session_state.messages.append({"role": "assistant", "content": answer.content})
else:
    st.info("Enter a search topic in the sidebar and click Load Papers to get started.")