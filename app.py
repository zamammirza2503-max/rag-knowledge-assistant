from pathlib import Path

import streamlit as st

from llm import friendly_error
from rag import RAGEngine

st.set_page_config(page_title="Electrical Design Docs Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Electrical Design Docs Assistant")
st.caption(
    "RAG demo: ask questions about internal engineering standards and get answers with sources. "
    "All documents are fictional sample guidelines of *Demo Automation GmbH*, written for this "
    "demo — not real design rules."
)

EXAMPLES = [
    "Which wire colour do we use for 24 V DC control circuits?",
    "What cross-section do I need behind a 16 A breaker?",
    "How is a conveyor motor with a frequency inverter protected?",
    "What does the tag =BHS1+CAB2-K12 mean?",
    "What has to happen before a project can be released?",
    "How much spare space must a control cabinet have?",
]


@st.cache_resource(show_spinner="Indexing the documentation (creating embeddings)...")
def get_engine():
    return RAGEngine(Path(__file__).parent / "data")


try:
    engine = get_engine()
except Exception as e:  # missing key, quota, ...
    st.error(friendly_error(e))
    st.stop()

with st.sidebar:
    st.header("Knowledge base")
    st.write(f"**{len(engine.source_names)}** documents · **{len(engine.chunks)}** chunks")
    st.markdown("\n".join(f"- {name}" for name in engine.source_names))
    st.divider()
    top_k = st.slider("Passages used per answer (top-k)", 2, 8, 4)
    st.divider()
    st.subheader("Try asking")
    for q in EXAMPLES:
        if st.button(q, use_container_width=True):
            st.session_state.pending = q
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.history = []

st.session_state.setdefault("history", [])


def show_sources(results):
    with st.expander(f"📚 Sources ({len(results)} passages retrieved)"):
        for n, (score, c) in enumerate(results, start=1):
            st.markdown(f"**[{n}] {c['title']} › {c['section']}**  \n`{c['source']}` · relevance {score:.2f}")
            st.caption(c["text"][:600] + ("…" if len(c["text"]) > 600 else ""))


for turn in st.session_state.history:
    with st.chat_message("user"):
        st.write(turn["question"])
    with st.chat_message("assistant"):
        st.markdown(turn["answer"])
        show_sources(turn["results"])

question = st.chat_input("Ask about cabinet design, wiring, tagging, PLC I/O, release process...")
question = question or st.session_state.pop("pending", None)

if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching the documentation and writing an answer..."):
                answer, results = engine.answer(question, top_k=top_k)
        except Exception as e:
            st.error(friendly_error(e))
            st.stop()
        st.markdown(answer)
        show_sources(results)
    st.session_state.history.append({"question": question, "answer": answer, "results": results})
