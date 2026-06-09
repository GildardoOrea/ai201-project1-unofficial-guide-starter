"""
Milestone 4: Embed chunks into ChromaDB and test retrieval.

Run:  python embed.py
  - First run: loads chunks.json, embeds with all-MiniLM-L6-v2, stores in ./chroma_db/
  - Subsequent runs: skips re-embedding (collection already populated) and goes
    straight to retrieval tests.

The retrieve() function is importable by Milestone 5 (app.py / query.py).
"""

import sys
import json
import chromadb
from sentence_transformers import SentenceTransformer

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHUNKS_FILE = "chunks.json"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "utep_parking"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

# ---------------------------------------------------------------------------
# Model + collection (module-level so imports in app.py don't re-init)
# ---------------------------------------------------------------------------

_model: SentenceTransformer | None = None
_collection = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"Loading embedding model ({EMBEDDING_MODEL})...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


# ---------------------------------------------------------------------------
# Build the vector store
# ---------------------------------------------------------------------------

def build_index() -> int:
    """
    Embed all chunks from chunks.json and upsert into ChromaDB.
    Safe to call more than once — uses upsert so existing entries are overwritten.
    Returns the number of chunks indexed.
    """
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    model = _get_model()
    collection = _get_collection()

    texts = [c["text"] for c in chunks]
    ids = [f"{c['source']}__chunk{c['chunk_index']}" for c in chunks]
    metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]

    print(f"Embedding {len(chunks)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_list=True)

    print("Storing in ChromaDB...")
    # Upsert in batches of 500 to stay within ChromaDB's default limits
    batch_size = 500
    for i in range(0, len(chunks), batch_size):
        collection.upsert(
            ids=ids[i : i + batch_size],
            documents=texts[i : i + batch_size],
            embeddings=embeddings[i : i + batch_size],
            metadatas=metadatas[i : i + batch_size],
        )

    return len(chunks)


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """
    Embed query and return the top-k most similar chunks from ChromaDB.
    Each result dict has: text, source, chunk_index, distance.
    """
    model = _get_model()
    collection = _get_collection()

    query_embedding = model.encode(query, convert_to_list=True)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "text": text,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": round(dist, 4),
        })
    return hits


# ---------------------------------------------------------------------------
# Retrieval test (checkpoint)
# ---------------------------------------------------------------------------

TEST_QUERIES = [
    # Q3 — exact dollar amounts should surface from utep_permit_pricing
    "How much does a standard student parking permit cost for 2025-2026?",
    # Q4 — should pull from both official garage pages and Reddit Schuster/Sun Bowl thread
    "Are the Schuster and Sun Bowl parking garages worth the price and do they fill up quickly?",
    # Q1 — should surface Reddit tips about free street parking near campus
    "Where can I find free parking near UTEP campus without buying a permit?",
]


def run_retrieval_tests():
    print("\n" + "=" * 60)
    print("RETRIEVAL TESTS (checkpoint)")
    print("=" * 60)

    for query in TEST_QUERIES:
        print(f"\nQuery: {query!r}")
        hits = retrieve(query)
        for rank, hit in enumerate(hits, 1):
            relevant = "OK" if hit["distance"] < 0.5 else "??"
            print(
                f"  [{rank}] {relevant} dist={hit['distance']:.4f}  "
                f"source={hit['source']}  chunk={hit['chunk_index']}"
            )
            # Print first 200 chars of the chunk so relevance is visible
            preview = hit["text"].replace("\n", " ")[:200]
            print(f"       {preview}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    collection = _get_collection()

    if collection.count() == 0:
        n = build_index()
        print(f"\nIndexed {n} chunks into ChromaDB at {CHROMA_DIR!r}")
    else:
        print(
            f"Collection already has {collection.count()} chunks — skipping re-embed. "
            f"Delete {CHROMA_DIR!r} and re-run to rebuild."
        )

    run_retrieval_tests()
