from flask import Blueprint, jsonify

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/", methods=["GET"])
def get_settings():
    return jsonify({
        "message": "Settings endpoint working"
    })