from flask import Blueprint, jsonify, request
from app.models.ollamma import CandidateTranscript
from app import db
import requests
import json
import re

candidate_transcript = Blueprint("candidate_transcripts", __name__)

OLLAMA_URL = "http://localhost:11434/api/generate"


def clean_json_response(text):
    if not text:
        return {}

    text = text.strip()

    # remove markdown fences
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # extract json object
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return {}

    text = text[start:end + 1]

    try:
        return json.loads(text)
    except Exception:
        return {}


@candidate_transcript.route("/api/evaluate-approach", methods=["POST"])
def evaluate_approach():
    try:
        data = request.get_json()

        problem = data.get("problem", "")
        test_cases = data.get("testCases", [])
        approach = data.get("approach", "")

        if not approach.strip():
            return jsonify({
                "score": 0,
                "approved": False,
                "result": "Approach is required"
            }), 400

        prompt = f"""
You are a strict coding interview evaluator.

Your job is to evaluate ONLY the candidate's stated approach for the given problem.

You must follow these rules exactly:
1. Return ONLY valid JSON.
2. Do not include markdown.
3. Do not include backticks.
4. Do not include any explanation outside JSON.
5. Output must contain exactly one JSON object.
6. The JSON object must contain exactly one key: "score"
7. "score" must be an integer from 0 to 10 only.
8. Be strict in grading.
9. If the approach is irrelevant or incorrect, give a low score.
10. If the approach is partially correct but vague or missing important details, give 5 to 6.
11. If the approach is correct and reasonably clear, give 7 to 8.
12. If the approach is correct, optimal, and clearly explained, give 9 to 10.
13. Never return anything except this format:
{{"score": 7}}

Problem:
{problem}

Test Cases:
{test_cases}

Candidate Approach:
{approach}
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "deepseek-coder",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                "score": 0,
                "approved": False,
                "error": f"Ollama error: {response.text}"
            }), 500

        raw_result = response.json().get("response", "")
        parsed = clean_json_response(raw_result)

        score = int(parsed.get("score", 0))
        approved = score > 6

        return jsonify({
            "score": score,
            "approved": approved,
            "result": raw_result
        }), 200

    except Exception as e:
        return jsonify({
            "score": 0,
            "approved": False,
            "error": str(e)
        }), 500


# ==============================
# GET TRANSCRIPTS BY CANDIDATE
# ==============================
@candidate_transcript.route("/api/transcripts/<candidate_id>", methods=["GET"])
def get_transcripts(candidate_id):
    try:
        transcripts = CandidateTranscript.query.filter_by(
            candidate_id=candidate_id
        ).order_by(CandidateTranscript.created_at.desc()).all()

        result = []
        for t in transcripts:
            result.append({
                "id": str(t.id),
                "session_id": t.session_id,
                "transcript_text": t.transcript_text,
                "ai_summary": t.ai_summary,
                "created_at": t.created_at
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==============================
# UPDATE AI SUMMARY (LLM)
# ==============================
@candidate_transcript.route("/api/transcripts/<transcript_id>", methods=["PUT"])
def update_transcript(transcript_id):
    try:
        data = request.get_json()

        transcript = CandidateTranscript.query.get(transcript_id)
        if not transcript:
            return jsonify({"error": "Not found"}), 404

        transcript.ai_summary = data.get("ai_summary")
        db.session.commit()

        return jsonify({"message": "Updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500