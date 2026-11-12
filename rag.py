"""Retrieval-Augmented Generation (RAG) engine.

1. Load Markdown/text documents and split them into chunks along their headings.
2. Turn every chunk into an embedding vector (once, at start-up).
3. For a question: embed it, score all chunks (semantic + keyword match),
   take the best top-k chunks.
4. Ask the LLM to answer using ONLY those chunks and to cite them as [1], [2], ...
"""
import re
from pathlib import Path

import numpy as np

from llm import chat, embed, make_client, setting

WORD = re.compile(r"[a-z0-9]+(?:[-.][a-z0-9]+)*")
STOPWORDS = set(
    "a an and are as at be by can do does for from how i in is it of on or our "
    "should the to what when where which who why with you your we must".split()
)


def tokens(text):
    return {t for t in WORD.findall(text.lower()) if t not in STOPWORDS and len(t) > 1}


class RAGEngine:
    def __init__(self, docs_dir, max_chunk_chars=1200):
        self.docs_dir = Path(docs_dir)
        self.max_chunk_chars = max_chunk_chars
        self.client = make_client()
        self.embedding_model = setting("EMBEDDING_MODEL", "gemini-embedding-001")

        self.chunks = self._load_documents()
        self.matrix = self._embed([c["embed_text"] for c in self.chunks])

    # ---------- indexing ----------

    @property
    def source_names(self):
        return sorted({c["source"] for c in self.chunks})

    def _split_markdown(self, text):
        """Split a document into (section title, section text) along ## / ### headings."""
        title = ""
        sections, current_heading, buf = [], "", []
        for line in text.splitlines():
            if line.startswith("# ") and not title:
                title = line[2:].strip()
                continue
            if re.match(r"#{2,3} ", line):
                if buf:
                    sections.append((current_heading, "\n".join(buf).strip()))
                current_heading, buf = line.lstrip("#").strip(), []
            else:
                buf.append(line)
        if buf:
            sections.append((current_heading, "\n".join(buf).strip()))
        return title, [(h, t) for h, t in sections if t]

    def _load_documents(self):
        chunks = []
        for path in sorted(self.docs_dir.glob("*")):
            if path.suffix.lower() not in {".md", ".txt"}:
                continue
            title, sections = self._split_markdown(path.read_text(encoding="utf-8"))
            for heading, body in sections:
                # very long sections are split again by paragraphs
                parts, part = [], ""
                for para in body.split("\n\n"):
                    if part and len(part) + len(para) > self.max_chunk_chars:
                        parts.append(part)
                        part = ""
                    part = f"{part}\n\n{para}".strip()
                parts.append(part)
                for p in parts:
                    chunks.append({
                        "source": path.name,
                        "title": title or path.stem,
                        "section": heading or "(introduction)",
                        "text": p,
                        # document + section title help retrieval a lot
                        "embed_text": f"{title} > {heading}\n{p}",
                        "tokens": tokens(f"{heading} {p}"),
                    })
        if not chunks:
            raise RuntimeError(f"No .md or .txt documents found in {self.docs_dir}")
        return chunks

    def _embed(self, texts):
        vectors = []
        for i in range(0, len(texts), 90):  # API accepts up to 100 inputs per call
            resp = embed(self.client, self.embedding_model, texts[i:i + 90])
            vectors += [d.embedding for d in resp.data]
        m = np.asarray(vectors, dtype=np.float32)
        return m / np.clip(np.linalg.norm(m, axis=1, keepdims=True), 1e-9, None)

    # ---------- retrieval ----------

    def retrieve(self, question, top_k=4):
        q = self._embed([question])[0]
        semantic = self.matrix @ q  # cosine similarity (vectors are normalised)

        # Keyword overlap helps with exact codes like "-F12", "IEC 81346" or "2.5 mm2"
        q_tokens = tokens(question)
        keyword = np.array([
            len(q_tokens & c["tokens"]) / max(len(q_tokens), 1) for c in self.chunks
        ], dtype=np.float32)

        scores = 0.85 * semantic + 0.15 * keyword
        best = np.argsort(-scores)[:top_k]
        return [(float(scores[i]), self.chunks[i]) for i in best]

    # ---------- generation ----------

    def answer(self, question, top_k=4):
        results = self.retrieve(question, top_k)
        context = "\n\n".join(
            f"[{n}] {c['title']} — {c['section']} ({c['source']})\n{c['text']}"
            for n, (_, c) in enumerate(results, start=1)
        )
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant for electrical design engineers. Answer ONLY from the "
                    "numbered context passages. Cite the passages you used like [1] or [2] "
                    "after the sentence. If the passages do not contain the answer, say clearly "
                    "that the documentation does not cover it — never guess values, ratings or "
                    "rules. Be concise; use a short list when it helps."
                ),
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ]
        response = chat(self.client, messages=messages)
        return response.choices[0].message.content or "", results
