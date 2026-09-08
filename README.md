# RAG Knowledge Assistant

A small, Retrieval-Augmented Generation (RAG) application built with **Python, Streamlit, OpenAI embeddings, cosine similarity, and the OpenAI Responses API**.

## What it demonstrates

- Document ingestion from local Markdown/text files
- Embedding-based semantic retrieval
- Top-k context selection
- Grounded LLM answers with source names
- A simple, understandable RAG pipeline
- Streamlit UI
- No framework magic: retrieval logic is implemented directly in Python

## Architecture

![RAG Knowledge Assistant](docs/RAG-Knowledge-Assistant.png)

```text
User question
     |
     v
Streamlit UI
     |
     v
OpenAI embedding
     |
     v
Cosine similarity search
     |
     v
Top-k document chunks
     |
     v
Prompt + retrieved context
     |
     v
OpenAI Responses API
     |
     v
Answer + sources
```

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Add your API key to `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5.6-luna
EMBEDDING_MODEL=text-embedding-3-small
```

Run:

```bash
streamlit run app.py
```
