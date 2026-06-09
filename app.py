"""
Milestone 5 — Gradio web interface for the UTEP Parking Unofficial Guide.

Run:  python app.py
Then open http://localhost:7860 in your browser.
"""

import sys
import gradio as gr
from query import ask

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def handle_query(question: str):
    question = question.strip()
    if not question:
        return "Please enter a question.", ""

    result = ask(question)
    sources_text = "\n".join(f"  • {s}" for s in result["sources"])
    return result["answer"], sources_text


with gr.Blocks(title="UTEP Parking Unofficial Guide") as demo:
    gr.Markdown(
        """
        # UTEP Parking Unofficial Guide
        Ask anything about parking at UTEP — permits, garages, free street parking,
        overflow lots, citations, and more. Answers are grounded in official UTEP
        pages and real student posts from r/UTEP.
        """
    )

    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. Where can I find free parking near campus?",
            lines=2,
            scale=4,
        )
        btn = gr.Button("Ask", variant="primary", scale=1)

    answer_box = gr.Textbox(label="Answer", lines=10, interactive=False)
    sources_box = gr.Textbox(label="Retrieved from", lines=4, interactive=False)

    btn.click(handle_query, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(handle_query, inputs=inp, outputs=[answer_box, sources_box])

    gr.Examples(
        examples=[
            ["How much does a student parking permit cost for 2025-2026?"],
            ["Where can I find free parking near UTEP without buying a permit?"],
            ["Are the Schuster and Sun Bowl garages worth it, do they fill up fast?"],
            ["What are my options if student parking passes are sold out?"],
            ["Where is the overflow parking lot and what do students say about it?"],
        ],
        inputs=inp,
    )

if __name__ == "__main__":
    demo.launch()
