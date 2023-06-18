from flask import request, jsonify, Blueprint
from database import db
from models.user import User


user_api_bp = Blueprint("user_api", __name__)


# Create a User
@user_api_bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    if name is None:
        return jsonify({"message": "User name is required"}), 400
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user_id": user.id})


# Read all Users
@user_api_bp.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])


# Read a specific User
@user_api_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name})
    else:
        return jsonify({"message": "User not found"}), 404


# Update a User
@user_api_bp.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        name = data.get("name")
        if name is None:
            return jsonify({"message": "User name is required"}), 400
        user.name = name
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"message": "User not found"}), 404


# Delete a User
@user_api_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"message": "User not found"}), 404
