from flask import request, jsonify, Blueprint
from database import db
from models.appeal import Appeal


# CRUD API Operations for Appeals
appeal_api_bp = Blueprint("appeal_api", __name__)


@appeal_api_bp.route("/api/appeals", methods=["POST"])
def create_appeal():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")
    if user_id is None or message is None:
        return jsonify({"message": "User ID and message are required"}), 400
    appeal = Appeal(user_id=user_id, message=message)
    db.session.add(appeal)
    db.session.commit()
    return jsonify({"message": "Appeal created successfully", "appeal_id": appeal.id})


@appeal_api_bp.route("/api/appeals", methods=["GET"])
def get_appeals():
    appeals = Appeal.query.all()
    return jsonify([{"id": a.id, "user_id": a.user_id, "message": a.message, "resolved": a.resolved} for a in appeals])


@appeal_api_bp.route("/api/appeals/<int:appeal_id>", methods=["GET"])
def get_appeal(appeal_id):
    appeal = Appeal.query.get(appeal_id)
    if appeal:
        return jsonify(
            {"id": appeal.id, "user_id": appeal.user_id, "message": appeal.message, "resolved": appeal.resolved}
        )
    else:
        return jsonify({"message": "Appeal not found"}), 404


@appeal_api_bp.route("/api/appeals/<int:appeal_id>", methods=["PUT"])
def update_appeal(appeal_id):
    appeal = Appeal.query.get(appeal_id)
    if appeal:
        data = request.get_json()
        user_id = data.get("user_id")
        message = data.get("message")
        resolved = data.get("resolved")
        if user_id is None or message is None or resolved is None:
            return jsonify({"message": "User ID, message, and resolved status are required"}), 400
        appeal.user_id = user_id
        appeal.message = message
        appeal.resolved = resolved
        db.session.commit()
        return jsonify({"message": "Appeal updated successfully"})
    else:
        return jsonify({"message": "Appeal not found"}), 404


@appeal_api_bp.route("/api/appeals/<int:appeal_id>", methods=["DELETE"])
def delete_appeal(appeal_id):
    appeal = Appeal.query.get(appeal_id)
    if appeal:
        db.session.delete(appeal)
        db.session.commit()
        return jsonify({"message": "Appeal deleted successfully"})
    else:
        return jsonify({"message": "Appeal not found"}), 404
