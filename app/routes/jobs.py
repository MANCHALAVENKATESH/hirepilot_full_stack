from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.job import Job
import re
import pdb
jobs_bp = Blueprint("jobs", __name__)




@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    try:
        jobs = Job.query.order_by(Job.created_at.desc()).all()

        result = []
        for job in jobs:
            if job.experience_max is not None:
                experience = f"{job.experience_min}–{job.experience_max} yrs"
            elif job.experience_min is not None:
                experience = f"{job.experience_min}+ yrs"
            else:
                experience = None

            result.append({
                "id": str(job.id),
                "title": job.title,
                "department": job.department,
                "location": job.location,
                "employment_type": job.employment_type,
                "experience": experience,
                "experience_min": job.experience_min,
                "experience_max": job.experience_max,
                "status": job.status
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_job_from_data(data, default_status="draft"):
    job = Job(
        organization_id=data.get("organization_id"),
        created_by=data.get("created_by"),
        title=data.get("title"),
        department=data.get("department"),
        location=data.get("location"),
        employment_type=data.get("employmentType"),
        experience=data.get("experienceRange"),
        skills=data.get("skills", []),
        description=data.get("description"),
        status=data.get("status", default_status),
        ai_matching_enabled=data.get("ai_matching_enabled", True),
    )

    db.session.add(job)
    db.session.commit()

    return job

@jobs_bp.route("/save-draft", methods=["POST"])
def save_draft():
    try:
        data = request.get_json()

        if not data.get("title"):
            return jsonify({"error": "Title is required"}), 400

        job = create_job_from_data(data, default_status="draft")

        return jsonify({
            "message": "Draft saved successfully",
            "id": str(job.id),
            "status": job.status,
            "experience_min": job.experience_min,
            "experience_max": job.experience_max
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@jobs_bp.route("/publish", methods=["POST"])
def publish_job():
    try:
        data = request.get_json()
        print(data)

        required_fields = [
            "title",
            "department",
            "location",
            "employmentType",
            "description",
            "experienceRange"
        ]

        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        # force publish status
        data["status"] = "published"

        # create job
        job = create_job_from_data(data, default_status="published")

        return jsonify({
            "message": "Job published successfully",
            "id": str(job.id),
            "status": job.status,
            "title": job.title,
            "department": job.department,
            "location": job.location,
            "employment_type": job.employment_type,
            "experience": job.experience,
            "skills": job.skills if job.skills else [],
            "description": job.description
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500