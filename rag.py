import os
from pathlib import Path

import numpy as np
from openai import OpenAI


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


class RAGEngine:
    def __init__(self, docs_dir, embedding_model, answer_model):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embedding_model = embedding_model
        self.answer_model = answer_model
        self.chunks = []
        self.embeddings = []
        self._load_documents()

    @property
    def source_names(self):
        return sorted({chunk["source"] for chunk in self.chunks})

    def _chunk(self, text, size=900, overlap=120):
        text = " ".join(text.split())
        chunks = []
        start = 0
        while start < len(text):
            end = start + size
            chunks.append(text[start:end])
            if end >= len(text):
                break
            start = end - overlap
        return chunks

    def _load_documents(self):
        docs_dir = Path(self.docs_dir)
        for path in sorted(docs_dir.glob("*")):
            if path.suffix.lower() not in {".txt", ".md"}:
                continue
            text = path.read_text(encoding="utf-8")
            for i, chunk in enumerate(self._chunk(text)):
                self.chunks.append({"source": path.name, "chunk_id": i, "text": chunk})

        if not self.chunks:
            raise RuntimeError("No .txt or .md documents found in data/")

        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=[c["text"] for c in self.chunks],
        )
        self.embeddings = [item.embedding for item in response.data]

    def retrieve(self, question, top_k=3):
        query_embedding = self.client.embeddings.create(
            model=self.embedding_model,
            input=[question],
        ).data[0].embedding

        scored = []
        for chunk, embedding in zip(self.chunks, self.embeddings):
            score = cosine_similarity(query_embedding, embedding)
            scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

    def answer(self, question, top_k=3):
        results = self.retrieve(question, top_k)
        context = "\n\n".join(
            f"[Source: {chunk['source']}]\n{chunk['text']}"
            for score, chunk in results
        )

        prompt = f"""You are a company knowledge assistant.
Answer the user's question using only the supplied context.
If the context does not contain the answer, say that you do not have enough information.
Do not invent policies.

Context:
{context}

Question:
{question}

Give a concise answer and mention the relevant source file names."""

        response = self.client.responses.create(
            model=self.answer_model,
            input=prompt,
        )

        sources = [(chunk["source"], score) for score, chunk in results]
        return response.output_text, sources
