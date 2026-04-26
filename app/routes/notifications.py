from flask import Blueprint, jsonify
from app.models.notification import Notification

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("/", methods=["GET"])
def get_notifications():
    notifications = Notification.query.order_by(Notification.created_at.desc()).all()

    result = []
    for item in notifications:
        result.append({
            "id": str(item.id),
            "title": item.title,
            "message": item.message,
            "type": item.type,
            "is_read": item.is_read
        })

    return jsonify(result)