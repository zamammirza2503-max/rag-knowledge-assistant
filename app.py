import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag import RAGEngine

load_dotenv()

st.set_page_config(page_title="RAG Knowledge Assistant", page_icon="📚", layout="wide")
st.title("📚 RAG Knowledge Assistant")
st.caption("A small semantic-search + LLM application designed to be easy to explain in an interview.")

if not os.getenv("OPENAI_API_KEY"):
    st.warning("Set OPENAI_API_KEY in .env before asking questions.")

@st.cache_resource
def get_engine():
    return RAGEngine(
        docs_dir=Path("data"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        answer_model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
    )

engine = get_engine()

with st.sidebar:
    st.header("Retrieval")
    top_k = st.slider("Top-k chunks", 1, 5, 3)
    st.write(f"Indexed chunks: **{len(engine.chunks)}**")
    st.divider()
    st.write("**Files**")
    for name in engine.source_names:
        st.write(f"- {name}")

question = st.text_input("Ask a question about the company knowledge base")

if question:
    with st.spinner("Retrieving relevant context and generating an answer..."):
        answer, sources = engine.answer(question, top_k=top_k)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")
    for source, score in sources:
        st.write(f"- `{source}` — similarity {score:.3f}")
