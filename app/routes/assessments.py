from flask import Blueprint, jsonify
from app.models.assessment import Assessment

assessments_bp = Blueprint("assessments", __name__)

@assessments_bp.route("/", methods=["GET"])
def get_assessments():
    assessments = Assessment.query.order_by(Assessment.created_at.desc()).all()

    result = []
    for item in assessments:
        result.append({
            "id": str(item.id),
            "name": item.name,
            "role_title": item.role_title,
            "difficulty": item.difficulty,
            "duration_minutes": item.duration_minutes,
            "total_questions": item.total_questions,
            "status": item.status
        })
    return jsonify(result)