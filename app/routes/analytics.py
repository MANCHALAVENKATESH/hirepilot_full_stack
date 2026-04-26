from flask import Blueprint, jsonify
from app.models.application import Application
from app.models.job import Job
from app.models.assessment import AssessmentSubmission

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/", methods=["GET"])
def get_analytics():
    return jsonify({
        "applications": Application.query.count(),
        "jobs": Job.query.count(),
        "assessment_submissions": AssessmentSubmission.query.count()
    })