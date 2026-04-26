from flask import Blueprint, jsonify
from app.models.integration import Integration

integrations_bp = Blueprint("integrations", __name__)

@integrations_bp.route("/", methods=["GET"])
def get_integrations():
    integrations = Integration.query.all()

    result = []
    for item in integrations:
        result.append({
            "id": str(item.id),
            "provider_name": item.provider_name,
            "status": item.status,
            "config": item.config
        })

    return jsonify(result)