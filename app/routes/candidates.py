from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.candidate import Candidate
from werkzeug.utils import secure_filename
import os
import pymupdf  # PyMuPDF
import requests

candidates_bp = Blueprint("candidates", __name__)

UPLOAD_FOLDER = "uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@candidates_bp.route("/api/jobs/<job_id>/candidates", methods=["GET"])
def get_candidates_by_job(job_id):
    try:
        candidates = Candidate.query.filter_by(job_id=job_id).order_by(Candidate.created_at.desc()).all()

        result = []
        for c in candidates:
            result.append({
                "id": str(c.id),
                "job_id": str(c.job_id),
                "full_name": c.full_name,
                "email": c.email,
                "phone": c.phone,
                "experience": c.experience,
                "skills": c.skills or [],
                "summary": c.summary,
                "resume_filename": c.resume_filename,
                "ats_score": c.ats_score,
                "match_score": c.match_score,
                "recommendation": c.recommendation,
            })

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@candidates_bp.route("/create", methods=["POST"])
def create_candidate():
    try:
        form = request.form
        resume = request.files.get("resume")

        resume_filename = None
        resume_path = None

        if resume:
            resume_filename = secure_filename(resume.filename)
            resume_path = os.path.join(UPLOAD_FOLDER, resume_filename)
            resume.save(resume_path)

        skills_raw = form.get("skills", "")
        skills = [s.strip() for s in skills_raw.split(",") if s.strip()]

        candidate = Candidate(
            job_id=form.get("job_id"),
            full_name=form.get("full_name"),
            email=form.get("email"),
            phone=form.get("phone"),
            experience=form.get("experience"),
            skills=skills,
            summary=form.get("summary"),
            resume_filename=resume_filename,
            resume_path=resume_path,
            ats_score=78,
            match_score=82,
            recommendation="Recommended"
        )

        db.session.add(candidate)
        db.session.commit()

        return jsonify({
            "message": "Candidate created successfully",
            "id": str(candidate.id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
  
OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_text_from_pdf(file):
    doc = pymupdf.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    print(text)
    return text
import requests




@candidates_bp.route("/extract-resume", methods=["POST"])
def extract_resume():
    print("Extraccted Api Call")
    try:
        file = request.files.get("resume")
        if not file:
            return jsonify({"error": "Resume file is required"}), 400

        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        prompt = f"""
You are a senior HR assistant and resume parser.

Your task is to extract structured candidate information from resume text.

Rules:
- Output ONLY JSON (no markdown, no explanation)
- Be precise and avoid hallucination
- Do not invent information
- Normalize skills into a clean list

Return ONLY valid JSON:

{{
  "full_name": "",
  "email": "",
  "phone": "",
  "experience": "",
  "skills": [],
  "summary": ""
}}

Resume:
{text}
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

        result = response.json()["response"]
        print(result)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500