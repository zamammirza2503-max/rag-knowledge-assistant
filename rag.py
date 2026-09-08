import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


class RAGEngine:
    def __init__(self, docs_dir, embedding_model, answer_model):

        # Save constructor arguments
        self.docs_dir = docs_dir
        self.embedding_model = embedding_model
        self.answer_model = answer_model

        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or api_key == "your_key_here":
            raise ValueError(
                "OPENAI_API_KEY is missing or still set to 'your_key_here'. "
                "Please check your .env file."
            )

        # Create OpenAI client
        self.client = OpenAI(api_key=api_key)

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
                self.chunks.append(
                    {
                        "source": path.name,
                        "chunk_id": i,
                        "text": chunk,
                    }
                )

        if not self.chunks:
            raise RuntimeError(
                "No .txt or .md documents found in data/"
            )

        # Create embeddings for all document chunks
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=[c["text"] for c in self.chunks],
        )

        self.embeddings = [
            item.embedding
            for item in response.data
        ]

    def retrieve(self, question, top_k=3):

        # Create embedding for the user's question
        query_embedding = self.client.embeddings.create(
            model=self.embedding_model,
            input=[question],
        ).data[0].embedding

        scored = []

        for chunk, embedding in zip(
            self.chunks,
            self.embeddings
        ):
            score = cosine_similarity(
                query_embedding,
                embedding
            )

            scored.append((score, chunk))

        # Highest similarity first
        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return scored[:top_k]

    def answer(self, question, top_k=3):

        # Retrieve relevant chunks
        results = self.retrieve(question, top_k)

        # Build context
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

Give a concise answer and mention the relevant source file names.
"""

        # Generate answer
        response = self.client.responses.create(
            model=self.answer_model,
            input=prompt,
        )

        sources = [
            (chunk["source"], score)
            for score, chunk in results
        ]

        return response.output_text, sources
