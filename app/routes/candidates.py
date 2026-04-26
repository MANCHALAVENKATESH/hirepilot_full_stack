from flask import Blueprint, jsonify
from app.models.candidate import Candidate

candidates_bp = Blueprint("candidates", __name__)

@candidates_bp.route("/", methods=["GET"])
def get_candidates():
    candidates = Candidate.query.order_by(Candidate.created_at.desc()).all()

    result = []
    for candidate in candidates:
        result.append({
            "id": str(candidate.id),
            "full_name": candidate.full_name,
            "email": candidate.email,
            "location": candidate.location,
            "current_title": candidate.current_title,
            "current_company": candidate.current_company
        })

    return jsonify(result)