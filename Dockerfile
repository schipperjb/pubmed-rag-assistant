FROM python:3.11-slim

WORKDIR /app

COPY rag_app.py .

RUN pip install openai chromadb langchain langchain-openai langchain-community langchain-core langchain-text-splitters tiktoken streamlit biopython python-dotenv

EXPOSE 8501

CMD ["streamlit", "run", "rag_app.py", "--server.port=8501", "--server.address=0.0.0.0"]