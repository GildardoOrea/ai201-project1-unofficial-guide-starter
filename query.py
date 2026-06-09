"""
Milestone 5 — grounded generation.

ask(question) → {"answer": str, "sources": list[str]}

The LLM is instructed to answer ONLY from the retrieved chunks.
If the chunks don't cover the question it must say so explicitly
rather than drawing on its training knowledge.
"""

import os
from dotenv import load_dotenv
from groq import Groq
from embed import retrieve

load_dotenv()

_groq_client: Groq | None = None

SYSTEM_PROMPT = """\
You are the UTEP Parking Unofficial Guide — a helpful assistant that answers \
questions about parking at the University of Texas at El Paso.

RULES YOU MUST FOLLOW:
1. Answer ONLY using information from the DOCUMENTS provided below. \
Do not use any knowledge from your training data.
2. If the documents do not contain enough information to answer the question, \
respond with exactly: "I don't have enough information in my sources to answer that."
3. Be specific and direct. Cite which document your answer comes from \
by referencing the source name in your response (e.g. "According to the UTEP FAQ...").
4. Never invent prices, lot names, policies, or student opinions that are not \
explicitly stated in the documents.
"""

USER_TEMPLATE = """\
DOCUMENTS:
{context}

QUESTION: {question}

Answer based only on the documents above. If a document is a Reddit post or comment, \
you may characterize it as student opinion. If it is an official UTEP page, \
characterize it as official university information.
"""


def _get_client() -> Groq:
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not found — check your .env file.")
        _groq_client = Groq(api_key=api_key)
    return _groq_client


def _format_context(hits: list[dict]) -> str:
    """Turn retrieved chunks into a numbered context block for the prompt."""
    parts = []
    for i, hit in enumerate(hits, 1):
        parts.append(f"[Document {i} — source: {hit['source']}]\n{hit['text']}")
    return "\n\n".join(parts)


def ask(question: str, k: int = 5) -> dict:
    """
    Retrieve the top-k chunks for question, then ask Groq to generate a
    grounded answer.  Returns {"answer": str, "sources": list[str]}.
    """
    hits = retrieve(question, k=k)
    context = _format_context(hits)

    client = _get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_TEMPLATE.format(
                    context=context, question=question
                ),
            },
        ],
        temperature=0.2,   # low temperature = less hallucination
        max_tokens=512,
    )

    answer = response.choices[0].message.content.strip()

    # Collect unique source names from the retrieved chunks
    seen = set()
    sources = []
    for hit in hits:
        if hit["source"] not in seen:
            seen.add(hit["source"])
            sources.append(hit["source"])

    return {"answer": answer, "sources": sources}
