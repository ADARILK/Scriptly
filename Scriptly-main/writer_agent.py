"""
writer_agent.py
----------------
Agent #2 in the pipeline. Takes the Research Agent's output and turns it
into a first draft matching the requested content type, tone, and length.
"""

from .gemini_client import call_gemini

SYSTEM_INSTRUCTION = """You are a Writer Agent inside a multi-agent content
creation pipeline. You receive structured research notes from a Research
Agent and your job is to turn them into a well-written first draft.

Rules:
- Use the research notes as your source material, don't ignore them.
- Match the requested content type, tone, and length as closely as possible.
- Do not add meta-commentary like "Here is your draft" — output only the
  content itself.
"""


def write_draft(topic: str, research_notes: str, content_type: str, tone: str, length: str) -> dict:
    prompt = f"""
Topic: {topic}
Content type to produce: {content_type}
Tone: {tone}
Target length: {length}

Research notes from the Research Agent:
---
{research_notes}
---

Write the first draft now.
"""
    raw_output = call_gemini(SYSTEM_INSTRUCTION, prompt, temperature=0.8)
    return {"agent": "Writer Agent", "raw_output": raw_output}
