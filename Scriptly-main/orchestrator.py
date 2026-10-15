"""
orchestrator.py
----------------
Coordinates the multi-agent pipeline:

  Research Agent  -->  Writer Agent  -->  Editor Agent

Each agent's output becomes the next agent's input. Every step is logged
so the frontend can show an "agent activity" trace.
"""

import datetime
from .research_agent import run_research
from .writer_agent import write_draft
from .editor_agent import edit_content


def _log(logs: list, message: str):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    logs.append(f"[{timestamp}] {message}")


def run_pipeline(topic: str, content_type: str, tone: str, length: str) -> dict:
    logs = []

    _log(logs, f"Orchestrator: received request -> topic='{topic}', type='{content_type}'")

    _log(logs, "Orchestrator: dispatching task to Research Agent...")
    research_result = run_research(topic)
    _log(logs, "Research Agent: completed research, handing off to Writer Agent.")

    _log(logs, "Orchestrator: dispatching task to Writer Agent...")
    writer_result = write_draft(
        topic=topic,
        research_notes=research_result["raw_output"],
        content_type=content_type,
        tone=tone,
        length=length,
    )
    _log(logs, "Writer Agent: draft complete, handing off to Editor Agent.")

    _log(logs, "Orchestrator: dispatching task to Editor Agent...")
    editor_result = edit_content(
        draft=writer_result["raw_output"],
        content_type=content_type,
        tone=tone,
    )
    _log(logs, "Editor Agent: review complete. Pipeline finished.")

    return {
        "topic": topic,
        "research": research_result,
        "draft": writer_result,
        "final": editor_result,
        "logs": logs,
    }
