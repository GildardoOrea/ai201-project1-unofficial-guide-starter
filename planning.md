# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
The domain I chose was the University of Texas at El Paso parking.
This knowledge is valuable because the official UTEP parking website only tells you the rules, like how much permits costs, where the zones are located, and how to pay fines. But it does not tell you the reality of the commute and what parking areas around campues are available for free parking. Students need to know what to do when passes inevitably sell out, which garages actually have open spots from 7:00 AM through 5:00 PM, and where the secret free street parking is located. By combining official university guideliness with real student experiences from Reddit, the system bridges the gap between what the university says and what students actually experience on the ground.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | UTEP | Permit Pricing and Fees | https://www.utep.edu/parking-and-transportation/permits-and-parking/prices-fees.html |
| 2 | UTEP | Student Permits | https://www.utep.edu/parking-and-transportation/parking/student-permits.html |
| 3 | UTEP | Student Parking Permit Sales Guide 2025–2026 | https://www.utep.edu/parking-and-transportation/resources/26permitguide.html |
| 4 | UTEP | Parking Garages (Ticket Center) | https://www.utep.edu/utep-ticket-center/parking-garages/ |
| 5 | UTEP | Paid Visitor Parking | https://www.utep.edu/parking-and-transportation/permits-and-parking/visitors-parking.html |
| 6 | UTEP | Parking & Transportation FAQ | https://www.utep.edu/parking-and-transportation/about-and-contact/faq.html |
| 7 | Reddit | Free parking where on UTEP? | https://www.reddit.com/r/UTEP/comments/1f2sidj/free_parking_where_on_utep/ |
| 8 | Reddit| Parking (Schuster/Sun Bowl garages) | https://www.reddit.com/r/UTEP/comments/1rnqbii/parking/ |
| 9 | Reddit | Looking for parking pass or other ideas |  https://www.reddit.com/r/UTEP/comments/164pm4d/looking_for_parking_pass_or_other_ideas/ |
| 10 | Reddit| Parking (overflow lot / permit) | https://www.reddit.com/r/UTEP/comments/1n10kh3/parking/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size: 600 characters**

**Overlap: 150 characters**

**Reasoning: My dataset is a hybrid of short, punchy Reddit comments and structured FAQ lists from the official university pages. If I make the chunks too large, a single chunk might capture multiple unrelated Reddit comments, which can dilute the semantic meaning and make retrieval messy. A fixed size of 600 characters is just enough to capture a full paragraph from an official policy or a complete thought from a Reddit user without losing focus. The 150-character overlap ensures that if a student explains a multi-step parking strategy across two paragraphs, or if a sentence is split at the 600-character mark, the context is not lost.**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model: all-MiniLM-L6-v2 via sentence-transformers**

**Top-k: 5**

**Production tradeoff reflection: If I were deploying this for the entire student body and cost was not a constraint, the primary tradeoff I would weight is accuracy on domain-specific text versus latency. I would consider switching to a heavier, commercial model like OpenAI's text-embedding-3-large. A larger model with deeper semantic understanding would likely perform better at capturing UTEP-specific slang, campus abbreviations (like identifying that "Schuster" refers to a parking garage), and the highly contextual jargon often found in Reddit threads. However, relying on a massive API-based model introduces network latency and recurring per-token costs. For this prototype, all-MiniLM-L6-v2 is ideal because it runs entirely locally, costs nothing, and returns results fast enough to keep the user experience smooth.**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Where are the best places to find free parking near the UTEP campus if I don't want to buy a permit? | The system should mention specific street parking areas or neighborhoods discussed in the r/UTEP threads, while noting that these options usually require a significant walk to campus. |
| 2 | What are my best alternatives or strategies if the standard student parking passes are completely sold out? | The system should list official alternatives like paid visitor parking or the overflow lot, alongside any unofficial workarounds mentioned by students on Reddit. |
| 3 | How much does a standard student parking permit cost for the 2025–2026 academic year? | The system must return the exact dollar amounts retrieved specifically from the official UTEP 2025-2026 permit guide |
| 4 | Are the Schuster and Sun Bowl parking garages worth the price, and do they fill up too quickly during peak hours? | The system should combine the official pricing of the garages with student consensus on morning availability and traffic from the Reddit threads. |
| 5 | Where is the overflow parking lot located, and what do students actually say about using it? | The system should provide the official location/shuttle info for the overflow lot and contrast it with student complaints or tips regarding wait times and convenience. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. My document set contains inherently conflicting perspectives. From one side, UTEP pages state strict, definitive rules like "You must have a permit to park here", while Reddit threads offer informal workarounds like "They never check the overflow lot after 4 PM". The primary risk is that the LLM will struggle to keep these contexts separate, potentially hallucinating a new "official" policy based on a Reddit rumor or failing to properly attribute the informal advice to its student source.

2. Second is that because I am using a fixed-size chunking strategy on highly conversational Reddit threads, there is a high risk that key contextual information like the specific name of a building or lot gets split across chunks. If a student writes a long complaing about "A parking lot called schuster" but the word "garage" or "parking" falls into the adjacent chunk, the all-MiniLM-L6-v2 embedding model might score the chunk too low on relevance, causing the system to miss crucial student opinions during retrieval.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

 [Document Ingestion] - Python / BeautifulSoup for scraping UTEP & Reddit
         |
         v
     [Chunking] - Custom Python: 600 chars, 150 overlap
         |
         v
   [Embed & Store] - sentence-transformers: all-MiniLM-L6-v2 + ChromaDB
         |
         v
    [Retrieval] - ChromaDB Semantic Search: top-k=5
         |
         v
    [Generation] - Groq API: llama-3.3-70b-versatile

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Tool: Claude Sonnet

Input: I will provide my documents list and my chunking strategy with the fixed-size, 600 characters, 150 overlap. I will ask it to write an ingestion script using BeautifulSoup to scrape the UTEP URLs and clean the Reddit text.

Output: A Python script containing a clean_text() function to strip HTML/nav bars, and a chunk_text() function that splits the text exactly to my specified dimensions.

Verification: I will print out 5 random chunks before moving on. I will manually verify that they contain no leftover HTML tags, that they are roughly 600 characters long, and that the 150-character overlap successfully captures context across chunk boundaries.

**Milestone 4 — Embedding and retrieval:**
Tool: Claude Sonnet

Input: I will provide my "Retrieval Approach" section, specifying sentence-transformers in all-MiniLM-L6-v2, ChromaDB, and a top-k=5 requirement. I will also provide the course requirement that chunks must be stored with their source metadata.

Output: A Python script that initializes the ChromaDB client, embeds the chunks generated in Milestone 3, and a retrieve_context(query) function that returns the top 5 chunks.

Verification: I will pass 3 of the questions from my Evaluation Plan into the retrieve_context() function. I will inspect the output to ensure exactly 5 chunks are returned, that their distance scores are reasonable like < 0.5, and that the retrieved text visibly relates to the query.

**Milestone 5 — Generation and interface:**
Tool: Claude Sonnet

Input: I will provide the course's strict grounding requirements, it must answer only from context, must cite sources, my Groq LLM choice (llama-3.3-70b-versatile), and the boilerplate Gradio web UI code from the instructions.

Output: A robust system prompt that forces the LLM to refuse questions outside the context, the Groq API generation function, and a working app.py Gradio interface that displays the answer alongside the retrieved sources.

Verification: I will run two tests. First, I will ask a valid question from my Evaluation Plan and verify the UI explicitly names the UTEP or Reddit source. Second, I will ask an out-of-scope question for example "How do I fix a flat tire?" to verify the model refuses to answer rather than hallucinating from its general training data.