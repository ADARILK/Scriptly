"""
editor_agent.py
----------------
Agent #3 in the pipeline. Reviews the Writer Agent's draft, fixes
grammar/clarity/flow, and produces a polished final version plus notes
on what changed.
"""

from .gemini_client import call_gemini

SYSTEM_INSTRUCTION = """You are an Editor Agent inside a multi-agent content
creation pipeline. You receive a draft from a Writer Agent. Your job is to
polish it: fix grammar, tighten sentences, improve flow, and make sure it
matches the requested tone and content type.

Always respond in this exact format:

FINAL CONTENT:
<the fully polished final version of the content, ready to publish>

EDITOR NOTES:
- change 1
- change 2
- change 3
(2-4 short bullet points describing what you improved and why)
"""


def edit_content(draft: str, content_type: str, tone: str) -> dict:
    prompt = f"""
Content type: {content_type}
Tone required: {tone}

Draft from the Writer Agent:
---
{draft}
---

Review and polish this draft now. Follow the required format exactly.
"""
    raw_output = call_gemini(SYSTEM_INSTRUCTION, prompt, temperature=0.5)
    return {"agent": "Editor Agent", "raw_output": raw_output}
