from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.job import Job

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()

    result = []
    for job in jobs:
        result.append({
            "id": str(job.id),
            "title": job.title,
            "department": job.department,
            "location": job.location,
            "employment_type": job.employment_type,
            "status": job.status
        })

    return jsonify(result)

@jobs_bp.route("/", methods=["POST"])
def create_job():
    data = request.get_json()

    job = Job(
        organization_id=data.get("organization_id"),
        created_by=data.get("created_by"),
        title=data.get("title"),
        department=data.get("department"),
        location=data.get("location"),
        employment_type=data.get("employment_type"),
        experience_min=data.get("experience_min"),
        experience_max=data.get("experience_max"),
        description=data.get("description"),
        status=data.get("status", "draft"),
        ai_matching_enabled=data.get("ai_matching_enabled", True)
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({"message": "Job created", "id": str(job.id)}), 201