"""
app.py
------
Flask application. Serves the frontend (templates/index.html) and the
backend API (/api/generate) from a single app — one service, one URL,
whether run locally or deployed.

Run locally with:
  python app.py
"""

import os
from flask import Flask, render_template, request, jsonify

from agents.orchestrator import run_pipeline

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    topic = (data.get("topic") or "").strip()
    content_type = data.get("content_type") or "Blog Post"
    tone = data.get("tone") or "Professional"
    length = data.get("length") or "Medium (~400 words)"

    if not topic:
        return jsonify({"success": False, "error": "Topic cannot be empty."}), 400

    try:
        result = run_pipeline(topic=topic, content_type=content_type, tone=tone, length=length)
        return jsonify({"success": True, "data": result})
    except RuntimeError as e:
        # Raised by gemini_client.py when the API call fails (bad key, quota, etc.)
        return jsonify({"success": False, "error": str(e)}), 502
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
