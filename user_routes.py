from flask import request, jsonify, render_template, Blueprint
from database import db
from models.user import User


user_bp = Blueprint("user", __name__)


# Registration
@user_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    if name is None:
        return jsonify({"message": "Name is required"}), 400
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify({"message": "Username already exists"}), 409
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})


# Login
@user_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    if name is None:
        return jsonify({"message": "Name is required"}), 400
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@user_bp.route("/users", methods=["GET"])
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def user(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template("user.html", user=user)
    else:
        return jsonify({"message": "User not found"}), 404
