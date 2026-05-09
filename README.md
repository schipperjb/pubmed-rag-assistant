# 🔬 PubMed RAG Research Assistant
 
A conversational research assistant that answers scientific questions using real, published abstracts from PubMed — powered by Retrieval Augmented Generation (RAG).
 
![Python](https://img.shields.io/badge/Python-3.11-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red) ![LangChain](https://img.shields.io/badge/LangChain-latest-green) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange) ![Docker](https://img.shields.io/badge/Docker-supported-blue)
 
---
 
## What It Does
 
Instead of asking an LLM to answer from general training knowledge, this app:
 
1. **Fetches real abstracts** from PubMed based on your search topic
2. **Chunks and embeds** them into a local vector database (ChromaDB)
3. **Retrieves the most relevant chunks** when you ask a question
4. **Grounds the LLM's answer** in actual published research — with citations
This is the core RAG pattern used in production AI systems today.
 
---
 
## Demo
 
Search topic: `CRISPR Cas9 gene editing keratinocytes`
 
> **Q: How is CRISPR used to treat skin conditions?**
>
> Based on the provided research abstracts, CRISPR/Cas9 technology is being explored as a potential noninvasive strategy for psoriasis treatment. Additionally, CRISPR/Cas9 gene editing is being considered for gene repair in conditions like epidermolysis bullosa. Various models are being evaluated for their ability to replicate key features of human psoriasis, with CRISPR/Cas9 gene editing used in generating targeted models.
>
> *(Citations: PMID 41171167, 39944129, 40106146)*
 
---
 
## Tech Stack
 
- **[Streamlit](https://streamlit.io/)** — Web UI
- **[LangChain](https://www.langchain.com/)** — RAG pipeline orchestration
- **[ChromaDB](https://www.trychroma.com/)** — Local vector store
- **[OpenAI](https://openai.com/)** — Embeddings + GPT-3.5-turbo
- **[Biopython Entrez](https://biopython.org/)** — PubMed API access
---

## How to Run
 
### 1. Clone the repo
```bash
git clone https://github.com/schipperjb/pubmed-rag-assistant.git
cd pubmed-rag-assistant
```
 
### 2. Create a conda environment
```bash
conda create -n rag-project python=3.11
conda activate rag-project
```
 
### 3. Install dependencies
```bash
pip install openai chromadb langchain langchain-openai langchain-community langchain-core langchain-text-splitters tiktoken streamlit biopython python-dotenv
```
 
### 4. Set up your API key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-openai-key-here
```
 
### 5. Run the app
```bash
streamlit run rag_app.py
```
 
---

## Run with Docker

No Python setup needed — just Docker!

### 1. Build the image
```bash
docker build -t rag-pubmed-app .
```

### 2. Run the container
```bash
docker run -p 8501:8501 --env-file .env rag-pubmed-app
```

### 3. Open in browser
```
http://localhost:8501
```

Make sure your `.env` file contains your OpenAI API key:
```
OPENAI_API_KEY=your-key-here
```
 
## How It Works
 
```
User Query
    │
    ▼
PubMed API (Biopython Entrez)
    │  fetches real abstracts
    ▼
Text Splitter (LangChain)
    │  chunks abstracts into 500-char pieces
    ▼
OpenAI Embeddings
    │  converts chunks to vectors
    ▼
ChromaDB Vector Store
    │  stores and indexes vectors locally
    ▼
Retriever (top 4 most relevant chunks)
    │
    ▼
GPT-3.5-turbo
    │  answers using only retrieved context
    ▼
Cited Answer
```
 
---
 
## Background
 
This project was built to explore RAG pipelines hands-on, combining a background in molecular biology and genomics with applied AI/ML development. The CRISPR and epidermolysis bullosa use cases are areas of personal research interest from earlier lab work.
 
---
 
## Notes
 
- A small amount of OpenAI API credit is required (pennies per session)
- PubMed abstracts are free and publicly available via the Entrez API
- The `.env` file is gitignored — never commit your API key
---
 
*Built by Jessica Schipper — [LinkedIn](https://linkedin.com/in/jessicaschipper) · [GitHub](https://github.com/schipperjb)*
