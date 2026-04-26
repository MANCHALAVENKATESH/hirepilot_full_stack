from flask import Blueprint, jsonify
from sqlalchemy import func
from app.models.job import Job
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.notification import Notification

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET"])
def get_dashboard():
    total_jobs = Job.query.count()
    total_candidates = Candidate.query.count()
    total_applications = Application.query.count()
    unread_notifications = Notification.query.filter_by(is_read=False).count()

    return jsonify({
        "metrics": {
            "total_jobs": total_jobs,
            "total_candidates": total_candidates,
            "total_applications": total_applications,
            "unread_notifications": unread_notifications
        }
    })