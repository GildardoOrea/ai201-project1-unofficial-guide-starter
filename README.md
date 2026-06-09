# The Unofficial Guide — Project 1

---

## Domain

The domain for this system is parking at the University of Texas at El Paso (UTEP). This knowledge is valuable because the official UTEP parking website only tells you the rules, things like permit prices, zone maps, citation procedures, but it does not tell you the reality of daily campus life. Students need to know what to do when permits sell out before they can buy one, which garages actually have open spots at 10 AM, and where the informal free street parking options are located. By combining official university guidelines with real student experiences from reddit/UTEP, this system bridges the gap between what the university publishes and what students actually encounter on the ground.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | UTEP Permit Pricing and Fees | Official university page | https://www.utep.edu/parking-and-transportation/permits-and-parking/prices-fees.html |
| 2 | UTEP Student Permits | Official university page | https://www.utep.edu/parking-and-transportation/parking/student-permits.html |
| 3 | UTEP Student Parking Permit Sales Guide 2025–2026 | Official university page | https://www.utep.edu/parking-and-transportation/resources/26permitguide.html |
| 4 | UTEP Parking Garages (Ticket Center) | Official university page | https://www.utep.edu/utep-ticket-center/parking-garages/ |
| 5 | UTEP Paid Visitor Parking | Official university page | https://www.utep.edu/parking-and-transportation/permits-and-parking/visitors-parking.html |
| 6 | UTEP Parking & Transportation FAQ | Official university page | https://www.utep.edu/parking-and-transportation/about-and-contact/faq.html |
| 7 | r/UTEP — "Free parking where on utep?" | Reddit thread | https://www.reddit.com/r/UTEP/comments/1f2sidj/free_parking_where_on_utep/ |
| 8 | r/UTEP — "Parking" (Schuster/Sun Bowl garages) | Reddit thread | https://www.reddit.com/r/UTEP/comments/1rnqbii/parking/ |
| 9 | r/UTEP — "Looking for parking pass or other ideas" | Reddit thread | https://www.reddit.com/r/UTEP/comments/164pm4d/looking_for_parking_pass_or_other_ideas/ |
| 10 | r/UTEP — "Parking" (overflow lot / permit struggles) | Reddit thread | https://www.reddit.com/r/UTEP/comments/1n10kh3/parking/ |

---

## Chunking Strategy

**Chunk size:** 600 characters

**Overlap:** 150 characters

**Why these choices fit my documents:** The corpus is a hybrid of two document types. The UTEP official pages contain structured lists and FAQ-style Q&A paragraphs, where a single policy answer typically fits in one or two sentences (100–200 characters). The Reddit threads contain conversational comments ranging from a single sentence to short paragraphs. A 600-character chunk is large enough to capture a complete Q&A exchange from the FAQ or a full Reddit comment without losing context, but small enough to avoid merging multiple unrelated comments into a single embedding. The 150-character overlap ensures that if a multi-step parking strategy is described across two paragraphs, the transition is preserved in at least one chunk so retrieval can find it.

The chunker snaps both the start and end of each chunk to the nearest word boundary, so that no chunk begins mid-word, which would degrade the quality of embeddings for short or unusual leading fragments.

**Final chunk count:** 85 chunks across 10 documents

---

## Sample Chunks

**Chunk 1 — source: `utep_permit_pricing` (chunk index 0)**
```
UTEP
Parking and Transportation
Permits and Parking
Permit Pricing and Fees
Multi-Year Employee Permits
Eligibility Notice:
These permit types and prices are available to
full-time UTEP employees only
. Employees must be benefits-eligible and have an active payroll record to qualify. Part-time employees, contractors, and affiliates should contact Parking & Transportation for alternative permit options.
Multi-year permits are
prorated monthly
on the
16th of each month
from September through May
. The prices listed reflect the cost of a full year.
These permits renew automatically each year
```

**Chunk 2 — source: `utep_parking_faq` (chunk index 0)**
```
UTEP
Parking and Transportation
About and Contact
How Can We Help?
Find answers to the most common questions about parking and transportation at UTEP. Need more help? Email
parking@utep.edu
or call (915) 747-5724.
Jump to a section
Permits
Cross-Parking
Returns
Payments
Citations
Lots and Events
Visitor Parking
ADA/DV
Enforcement
Shuttles
Lost Permit
Contact
Permits
Do I need a permit?
Yes. All vehicles on campus must have a valid permit or pay for hourly parking. Enforcement is 24/7.
```

**Chunk 3 — source: `utep_student_permits` (chunk index 0)**
```
UTEP
Parking and Transportation
Student Permits
Blue Perimeter Permit – $225 YEARLY
Valid: Specific blue lot & any remote lot, 7am–8pm daily. No cross-parking between blue lots before 3pm.
After 3:00PM: Cross-park into any Blue or Silver perimeter lot
After 4:00PM: Cross-park into either Gold garage
After 5:00PM: Cross-park into inner campus Orange and Red lots
Sale price and refund amount both prorate quarterly based on the yearly price
Where is my lot?
CR2 Crosby 2  DA1 Dawson 1  GR1 Glory Road 1
GR2 Glory Road 2  GR3 Glory Road 3
```

**Chunk 4 — source: `reddit_free_parking` (chunk index 0)**
```
POST TITLE: Free parking where on utep?
POST BODY: I recently got a car, and unfortunately the parking permits have all been sold. Please where is some free parking that is a good distance from utep? Any suggestions?
COMMENT: Share news, blog-posts, gossip and other interesting things about our beloved University of Texas at El Paso!
As a new community, we encourage everyone to subscribe and to tell their friends about this subreddit.
Related Subreddits: /r/ElPaso  /r/LasCruces
Student Resources: UTEP Official Website
```

**Chunk 5 — source: `reddit_overflow_lot` (chunk index 0)**
```
POST TITLE: Parking
POST BODY: Hello! I transferred to UTEP this year and I'm just confused about parking. Is it normal to struggle to find a parking spot? I paid for a spot in sun bowl 3 but when I went this morning at around 10am there were no spots along with several other cars looking as well. Do they sell more passes than they have lots? I looked at the parked cars and some of them had blue/red/green passes. But I wasn't completely sure if some of them were staff permits. I guess I'm just wondering if I just paid 300 only to still struggle finding a parking spot
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`, running locally

**Production tradeoff reflection:** For this prototype, `all-MiniLM-L6-v2` is ideal — it runs entirely on the local machine, has no cost, and returns embeddings quickly. If I were deploying this for the full UTEP student body with cost not as a constraint, the primary tradeoff I would weigh is accuracy on domain-specific vocabulary versus latency. I would consider switching to a heavier model like `text-embedding-3-large` from OpenAI. UTEP parking has campus-specific shorthand like "SBG," "Schuster," "Gold garage," "cross-parking" that a larger model trained on more diverse data would embed with higher fidelity. However, a cloud-hosted embedding model introduces per-token cost and network latency for every query. A secondary consideration is multilingual support: UTEP's student population is bilingual, and some students may phrase questions in Spanish; `all-MiniLM-L6-v2` was not trained for multilingual use, whereas models like `multilingual-e5-large` or OpenAI's embedding models handle cross-lingual queries more robustly.

---

## Retrieval Test Results

**Query 1:** `"How much does a standard student parking permit cost for 2025-2026?"`

| Rank | Distance | Source | Chunk preview |
|------|----------|--------|---------------|
| 1 | 0.2212 | `utep_permit_pricing` | `"Yearly Permit Prices Permit Type Yearly Price IC Reserved Spaces $930.00 IC Red $600.00 IC Orange $525.00 Sun Bowl Parking Garage (SBG) $575.00..."` |
| 2 | 0.2762 | `utep_permit_pricing` | `"Student Permit Prices Permit Type Yearly Price Sun Bowl Parking Garages (SBG) $400.00 Schuster Parking Garage (SCG) $400.00 Perimeter (Silver) $300.00..."` |
| 3 | 0.2990 | `utep_permit_guide_2025_2026` | `"Student Parking Permit Sales Guide 2025–2026 — Permit Sales Begin: August 12 at 9:00 AM (MST)..."` |

**Why chunks 1 and 2 are relevant:** Both are from `utep_permit_pricing` and contain the actual price tables. Chunk 1 covers employee/garage prices, chunk 2 specifically covers the student permit price table. The distance scores (0.22 and 0.28) are well below the 0.5 warning threshold, indicating strong semantic match.

---

**Query 2:** `"Where can I find free parking near UTEP without buying a permit?"`

| Rank | Distance | Source | Chunk preview |
|------|----------|--------|---------------|
| 1 | 0.2727 | `reddit_free_parking` | `"POST TITLE: Free parking where on utep? POST BODY: I recently got a car, and unfortunately the parking permits have all been sold..."` |
| 2 | 0.3177 | `utep_visitor_parking` | `"Visitor parking is available at several locations around campus..."` |
| 3 | 0.3392 | `reddit_overflow_lot` | `"COMMENT: If there is no parking spots where you have a permit, I recommend you call parking to let them know..."` |

**Why chunks 1 and 2 are relevant:** Chunk 1 is a direct Reddit thread from a student asking the exact same question, strong semantic overlap. Chunk 2 provides the official visitor alternative, which gives the LLM both the informal student perspective and the official fallback option to combine in its answer.

---

**Query 3:** `"Are the Schuster and Sun Bowl parking garages worth it?"`

| Rank | Distance | Source | Chunk preview |
|------|----------|--------|---------------|
| 1 | 0.4522 | `reddit_overflow_lot` | `"POST TITLE: Parking — I paid for a spot in sun bowl 3 but when I went this morning at around 10am there were no spots..."` |
| 2 | 0.4540 | `reddit_overflow_lot` | `"I looked at the parked cars and some of them had blue/red/green passes... I just paid 300 only to still struggle finding a parking spot"` |
| 3 | 0.4594 | `utep_permit_pricing` | `"Student Permit Prices... Sun Bowl Parking Garages (SBG) $400.00, Schuster Parking Garage (SCG) $400.00..."` |

The higher distance scores +0.45+ on this query reflect a real gap: no retrieved chunk directly uses the phrase "worth it" about these garages. The closest match is students describing frustration with Sun Bowl availability, which is semantically related but not a direct answer.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt contains four explicit rules given to the LLM before any user query:

1. Answer **only** using information from the provided documents — no training knowledge.
2. If the documents do not contain enough information, respond with the exact phrase: *"I don't have enough information in my sources to answer that."*
3. Be specific and cite which document the answer comes from by name in the response.
4. Never invent prices, lot names, policies, or student opinions not explicitly stated in the documents.

The prompt is passed as the `system` role message in the Groq API call, and `temperature=0.2` is set to reduce creative generation. Retrieved chunks are injected into the user message as a numbered context block, each labeled with its source filename.

**How source attribution is surfaced in the response:**

Attribution is enforced at two levels. First, the system prompt instructs the LLM to name the source document in its prose. Second, the `ask()` function in `query.py` programmatically collects the unique source filenames from the top-5 retrieved chunks and appends them to the return value as a `sources` list, this list is displayed in the "Retrieved from" box in the UI regardless of whether the LLM remembered to cite them in its answer.

---

## Example Responses

**Example 1 — grounded answer with source citation:**

> **Question:** How much does a student parking permit cost for 2025-2026?
>
> **Answer:** According to the `utep_permit_pricing` document, the student permit prices are: Sun Bowl Parking Garages (SBG) $400.00, Schuster Parking Garage (SCG) $400.00, Perimeter (Silver) $300.00, Perimeter (Blue) $225.00, Evening (4PM to 8PM) $150.00, Remote (GRN) $165.00, Miner Housing (Purple) $225.00, Motorcycle $150.00, Motorcycle (Secondary) $30.00. If I had to choose one as the "standard" student permit, the Perimeter (Blue) at $225.00 is mentioned across multiple official documents as the common student option.
>
> **Retrieved from:** utep_permit_pricing · utep_permit_guide_2025_2026 · utep_student_permits

---

**Example 2 — combining official information with student opinion:**

> **Question:** What do students say about the overflow parking lot?
>
> **Answer:** According to the `reddit_overflow_lot` document (student opinion), students report struggling to find parking spots even after purchasing a permit. One student paid $300 for a Sun Bowl 3 spot but found no available spaces at 10 AM. A comment in the same thread suggests calling the Parking and Transportation office when your permitted lot is full — they may direct you to additional parking. Another student comment mentions that parking typically improves after census day (roughly 20 days into the semester) as some students drop classes.
>
> **Retrieved from:** reddit_overflow_lot · reddit_free_parking · reddit_schuster_sunbowl · utep_permit_guide_2025_2026

---

**Example 3 — out-of-scope refusal:**

> **Question:** How do I fix a flat tire?
>
> **Answer:** I don't have enough information in my sources to answer that.
>
> **Retrieved from:** reddit_parking_pass_ideas · utep_parking_faq · reddit_overflow_lot · utep_permit_guide_2025_2026

The retriever still ran and returned chunks but the LLM correctly determined that none of those chunks addressed the question and refused to generate a plausible sounding answer from its training data.

---

## Query Interface

The interface is a Gradio web app launched with `python app.py`, accessible at `http://localhost:7860`.

**Input field:** A textbox labeled "Your question" with a placeholder prompt. The user types a plain-language question and presses Enter or clicks the "Ask" button.

**Output fields:**
- **Answer** — a multi-line textbox showing the LLM's grounded response, including inline source citations in the prose.
- **Retrieved from** — a separate textbox listing the source document filenames the answer was drawn from.

**Pre-loaded examples:** Five clickable example questions appear below the interface so a first-time user can immediately try the system without typing.

**Sample interaction transcript:**

```
Question: What are my options if student parking passes are sold out?

Answer:
According to student opinion in the reddit_parking_pass_ideas and reddit_overflow_lot
documents, if the standard student parking passes are completely sold out, some
alternatives include:
1. Waiting for census day (~20 days in) when more parking may become available, as
   some students drop classes and return their permits.
2. Contacting the Parking and Transportation office if your permitted lot is full —
   they may provide access to additional parking.
3. Looking at the Schuster Garage on the southside of campus, though these also
   sell out quickly according to reddit_schuster_sunbowl.
Note: these are student opinions and not official university policy.

Retrieved from:
  • reddit_parking_pass_ideas
  • reddit_overflow_lot
  • reddit_schuster_sunbowl
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Where are the best places to find free parking near UTEP campus without buying a permit? | Specific street/neighborhood options from r/UTEP threads; note they require a walk | Mentioned parking near surrounding businesses and a park area, noting it requires a walk; did not name specific streets | Relevant | Partially accurate |
| 2 | What are my best alternatives if student parking passes are completely sold out? | Official alternatives (visitor parking, overflow lot) + Reddit workarounds | Covered Reddit strategies well (census day, call parking office, Schuster); underemphasized official visitor parking option | Relevant | Partially accurate |
| 3 | How much does a standard student parking permit cost for the 2025–2026 academic year? | Exact dollar amounts from the official 2025-2026 permit guide | Listed the full student price table correctly ($225–$400 range); hedged on which was "standard" but all prices were accurate | Relevant | Accurate |
| 4 | Are the Schuster and Sun Bowl parking garages worth the price, and do they fill up too quickly during peak hours? | Official pricing + student consensus on morning availability | Retrieved the correct garage prices ($400) and the student concern that permits are oversold; ended with an overly cautious partial refusal despite having relevant data | Relevant | Partially accurate |
| 5 | Where is the overflow parking lot located, and what do students actually say about using it? | Official location/shuttle info + student complaints about wait times and convenience | Could not locate specific overflow lot location; provided general parking frustration from Reddit instead | Partially relevant | Inaccurate |

---

## Failure Case Analysis

**Question that failed:** *"Where is the overflow parking lot located, and what do students actually say about using it?"*

**What the system returned:** The system retrieved Reddit threads about general parking frustration and a snippet mentioning the Campbell building area, but stated it could not find the overflow lot's specific location. It correctly declined to invent a location, but the response was not useful.

**Root cause (tied to a specific pipeline stage — document collection):** This failure originates in Milestone 1, not in retrieval or generation. The term "overflow lot" is a colloquial label used by students in Reddit discussions, but none of the 10 collected documents was a UTEP-specific page that maps that term to an actual address or lot name. The 4 Reddit threads reference the overflow lot by name in passing without ever describing where it is. The embedding model embedded the query correctly and retrieved the most semantically similar chunks available — but those chunks discussed general parking scarcity, not overflow lot logistics. The retriever cannot return information that was never ingested.

**What I would change to fix it:** Add an 11th document specifically targeting the overflow lot — either the UTEP Parking shuttle and remote lot page, or a Reddit thread that explicitly names the overflow lot's address or cross-streets. A more targeted collection phase would have surfaced the answer this evaluation question required.

---

## Spec Reflection

**One way the spec helped during implementation:** The Chunking Strategy section of `planning.md` forced a deliberate decision about chunk size before writing any code. Specifying 600 characters with 150-character overlap and writing down *why* those numbers fit a hybrid corpus of FAQ paragraphs and Reddit comments meant that when the first chunker produced mid-word cuts, I had a clear definition of what "correct" looked like. Without the spec, I might have accepted the first working chunker and moved on. The spec gave me a concrete standard to test against.

**One way implementation diverged from the spec, and why:** The spec's AI Tool Plan stated that Claude would be given the Documents section and asked to produce a BeautifulSoup scraper for both UTEP URLs and Reddit threads. In practice, two things forced changes the spec did not anticipate. First, UTEP pages are structured so that the main content lives inside `div.rightSidebar` the initial scraper targeted `<main>` and returned only the text "Main Content". Second, the Reddit JSON API now returns 403 for unauthenticated scripts; the spec assumed the `.json` trick would work but it no longer does. Both required diagnosing the actual HTML structure at runtime and switching Reddit scraping to `old.reddit.com`. The spec couldn't have anticipated these infrastructure realities, which is exactly why the milestone asks you to verify output before moving on.

---

## AI Usage

**Instance 1 — Milestone 3: Document ingestion pipeline**

- *What I gave the AI:* The `## Documents` and `## Chunking Strategy` sections of `planning.md`, specifying 10 source URLs 6 UTEP pages and 4 Reddit threads, 600-character chunk size, and 150-character overlap. I asked Claude to implement a scraping and chunking script matching those specs.
- *What it produced:* An `ingest.py` using `requests` plus `BeautifulSoup` targeting the `<main>` HTML element for UTEP pages and the Reddit JSON API for Reddit.
- *What I changed or overrode:* The initial UTEP scraper returned only "Main Content" around 12 characters because the actual page content lives in `div.rightSidebar`, not `<main>`. I diagnosed this by inspecting the raw HTML and directed Claude to retarget the correct CSS class. Separately, the Reddit JSON API returned 403 for all 4 threads. I switched to `old.reddit.com`, which serves plain server-rendered HTML and does not require authentication. I also overrode the chunking logic twice, the first version cut mid-word, and fixing only the end-snapping created a cascade of tiny chunks. The final version uses a fixed step of 450 characters with word-boundary snapping on both the start and end of each chunk.

**Instance 2 — Milestone 5: Grounded generation and Gradio interface**

- *What I gave the AI:* My grounding requirements from the project instructions ("answer only from retrieved context, include source attribution, refuse out-of-scope questions"), my chosen LLM which was `llama-3.3-70b-versatile` via Groq, and the boilerplate Gradio code from the project instructions. I asked Claude to produce `query.py` with a system prompt that enforces grounding and `app.py` with the Gradio interface.
- *What it produced:* A `query.py` with a 4-rule system prompt, `temperature=0.2`, and source list construction. An `app.py` with an input textbox, separate answer and sources output boxes, and the 5 evaluation questions pre-loaded as clickable examples.
- *What I changed or overrode:* I tested the out-of-scope refusal with "How do I fix a flat tire?" and "What are the best restaurants near UTEP?" before accepting the grounding prompt. Both returned the correct refusal phrase without hallucinating, so the prompt was accepted but refused. I also verified that the sources list in the UI correctly showed filenames even when the LLM forgot to cite them in its prose, confirming that attribution is structurally guaranteed by the pipeline, not dependent on LLM behavior.
