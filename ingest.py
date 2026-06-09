"""
Milestone 3: Document ingestion pipeline for the UTEP Parking Unofficial Guide.
Scrapes 6 UTEP official pages + 4 Reddit threads, cleans them, and chunks them
to 600 chars with 150-char overlap as specified in planning.md.

Run:  python ingest.py
Output: documents/ folder with cleaned .txt files + chunks.json for Milestone 4
"""

import sys
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time
import random

# Fix Windows console encoding for emoji/Unicode in Reddit posts
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 600
OVERLAP = 150

UTEP_SOURCES = [
    {
        "url": "https://www.utep.edu/parking-and-transportation/permits-and-parking/prices-fees.html",
        "name": "utep_permit_pricing",
    },
    {
        "url": "https://www.utep.edu/parking-and-transportation/parking/student-permits.html",
        "name": "utep_student_permits",
    },
    {
        "url": "https://www.utep.edu/parking-and-transportation/resources/26permitguide.html",
        "name": "utep_permit_guide_2025_2026",
    },
    {
        "url": "https://www.utep.edu/utep-ticket-center/parking-garages/",
        "name": "utep_parking_garages",
    },
    {
        "url": "https://www.utep.edu/parking-and-transportation/permits-and-parking/visitors-parking.html",
        "name": "utep_visitor_parking",
    },
    {
        "url": "https://www.utep.edu/parking-and-transportation/about-and-contact/faq.html",
        "name": "utep_parking_faq",
    },
]

# Using old.reddit.com — serves plain server-rendered HTML, no API key required.
REDDIT_SOURCES = [
    {
        "url": "https://old.reddit.com/r/UTEP/comments/1f2sidj/free_parking_where_on_utep/",
        "name": "reddit_free_parking",
    },
    {
        "url": "https://old.reddit.com/r/UTEP/comments/1rnqbii/parking/",
        "name": "reddit_schuster_sunbowl",
    },
    {
        "url": "https://old.reddit.com/r/UTEP/comments/164pm4d/looking_for_parking_pass_or_other_ideas/",
        "name": "reddit_parking_pass_ideas",
    },
    {
        "url": "https://old.reddit.com/r/UTEP/comments/1n10kh3/parking/",
        "name": "reddit_overflow_lot",
    },
]


def clean_text(text: str) -> str:
    """Normalize whitespace and remove blank lines."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def scrape_utep_page(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # UTEP pages put their main body in div.rightSidebar (col-md-9).
    # Fall back to the full body if not found.
    content = (
        soup.find("div", class_="rightSidebar")
        or soup.find("div", class_=re.compile(r"col-md-9"))
        or soup.find("div", id="container")
        or soup.body
    )

    # Strip nav, footer, scripts, and sidebar navigation from the content area
    if content:
        for tag in content.find_all(["nav", "footer", "script", "style", "aside"]):
            tag.decompose()
        # Remove the left-side nav menu div
        for tag in content.find_all("div", class_=re.compile(r"leftSidebar|col-md-3")):
            tag.decompose()

    raw = (content or soup).get_text(separator="\n")
    return clean_text(raw)


def scrape_reddit_thread(url: str) -> str:
    """Scrape a Reddit thread from old.reddit.com (server-rendered HTML)."""
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    parts = []

    # Post title and optional self-text body
    title_tag = soup.find("a", class_="title")
    if title_tag:
        parts.append(f"POST TITLE: {title_tag.get_text().strip()}")

    selftext = soup.find("div", class_="expando")
    if selftext:
        body = selftext.get_text().strip()
        if body:
            parts.append(f"POST BODY: {body}")

    # Every comment's text body (includes nested replies)
    for comment_div in soup.find_all("div", class_="usertext-body"):
        text = comment_div.get_text().strip()
        if text and len(text) > 10:
            parts.append(f"COMMENT: {text}")

    return clean_text("\n\n".join(parts))


def _next_word_start(text: str, pos: int) -> int:
    """Return the index of the start of the next complete word at or after pos."""
    length = len(text)
    # If we landed mid-word, skip to the end of the current word
    if pos > 0 and pos < length and text[pos - 1] not in (" ", "\n", "\t"):
        while pos < length and text[pos] not in (" ", "\n", "\t"):
            pos += 1
    # Skip any whitespace to reach the start of the next word
    while pos < length and text[pos] in (" ", "\n", "\t"):
        pos += 1
    return pos


def chunk_text(text: str, source_name: str) -> list[dict]:
    """
    Split text into ~CHUNK_SIZE char pieces with OVERLAP overlap.
    Both the start and end of each chunk snap to word boundaries so no chunk
    begins or ends mid-word. The nominal advance step is CHUNK_SIZE - OVERLAP.
    """
    chunks = []
    index = 0
    length = len(text)
    step = CHUNK_SIZE - OVERLAP  # nominal advance: 450 chars

    nominal_start = 0
    while nominal_start < length:
        # Snap start forward to nearest word boundary
        start = _next_word_start(text, nominal_start)
        if start >= length:
            break

        end = min(start + CHUNK_SIZE, length)

        # Snap end backward to a word boundary (only when not at the text end)
        if end < length:
            nl = text.rfind("\n", start + step, end)
            sp = text.rfind(" ",  start + step, end)
            boundary = nl if nl != -1 else sp
            if boundary != -1:
                end = boundary

        chunk = text[start:end].strip()
        if chunk:
            chunks.append({
                "text": chunk,
                "source": source_name,
                "chunk_index": index,
            })
            index += 1

        nominal_start += step  # advance by fixed step from the nominal (pre-snap) position

    return chunks


def process_source(name: str, text: str, all_chunks: list) -> int:
    path = os.path.join(DOCUMENTS_DIR, f"{name}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    chunks = chunk_text(text, name)
    all_chunks.extend(chunks)
    return len(chunks)


def main():
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    all_chunks: list[dict] = []

    print("=== Scraping UTEP official pages ===")
    for source in UTEP_SOURCES:
        print(f"  {source['name']} ...", end=" ", flush=True)
        try:
            text = scrape_utep_page(source["url"])
            n = process_source(source["name"], text, all_chunks)
            print(f"{n} chunks  ({len(text)} chars)")
        except Exception as exc:
            print(f"FAILED: {exc}")
        time.sleep(1)

    print("\n=== Scraping Reddit threads ===")
    for source in REDDIT_SOURCES:
        print(f"  {source['name']} ...", end=" ", flush=True)
        try:
            text = scrape_reddit_thread(source["url"])
            n = process_source(source["name"], text, all_chunks)
            print(f"{n} chunks  ({len(text)} chars)")
        except Exception as exc:
            print(f"FAILED: {exc}")
        time.sleep(1)

    # Persist chunks for Milestone 4
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    total = len(all_chunks)
    print(f"\nTotal chunks written: {total}")
    if total < 50:
        print("WARNING: fewer than 50 chunks — some documents may have failed or chunks are too large.")
    elif total > 2000:
        print("WARNING: more than 2000 chunks — chunks may be too small.")

    # Checkpoint: print 5 random chunks for manual inspection
    print("\n=== 5 Random Chunks (checkpoint inspection) ===")
    samples = random.sample(all_chunks, min(5, total))
    for i, chunk in enumerate(samples, 1):
        print(f"\n--- Chunk {i} | source: {chunk['source']} | index: {chunk['chunk_index']} | {len(chunk['text'])} chars ---")
        print(chunk["text"])


if __name__ == "__main__":
    main()
