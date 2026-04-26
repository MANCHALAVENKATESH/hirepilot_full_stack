from flask import Blueprint, jsonify
from app.models.application import Application

pipeline_bp = Blueprint("pipeline", __name__)

@pipeline_bp.route("/", methods=["GET"])
def get_pipeline():
    applications = Application.query.all()

    data = []
    for app in applications:
        data.append({
            "id": str(app.id),
            "candidate_id": str(app.candidate_id) if app.candidate_id else None,
            "job_id": str(app.job_id) if app.job_id else None,
            "current_stage_id": str(app.current_stage_id) if app.current_stage_id else None,
            "status": app.status,
            "ai_match_score": float(app.ai_match_score) if app.ai_match_score else None
        })

    return jsonify(data)