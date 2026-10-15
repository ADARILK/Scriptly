"""
research_agent.py
------------------
Agent #1 in the pipeline. Given a topic, produces structured research —
key points, a suggested outline, and an angle — for the Writer Agent to use.
"""

from .gemini_client import call_gemini

SYSTEM_INSTRUCTION = """You are a Research Agent inside a multi-agent content
creation pipeline. Your only job is to research a topic and hand off clean,
structured findings to a Writer Agent. You do NOT write final content.

Always respond in this exact format:

KEY POINTS:
- point 1
- point 2
- point 3
(4-6 points)

SUGGESTED OUTLINE:
1. section 1
2. section 2
3. section 3
(3-5 sections)

ANGLE:
One sentence describing the most interesting/useful angle to take on this topic.
"""


def run_research(topic: str) -> dict:
    prompt = f"Research the topic: \"{topic}\". Follow the required format exactly."
    raw_output = call_gemini(SYSTEM_INSTRUCTION, prompt, temperature=0.6)
    return {"agent": "Research Agent", "raw_output": raw_output}
