from flask import request, jsonify, Blueprint
from database import db
from models.task import Task


task_api_bp = Blueprint("task_api", __name__)


@task_api_bp.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    user_id = data.get("user_id")
    description = data.get("description")
    if user_id is None or description is None:
        return jsonify({"message": "User ID and description are required"}), 400
    task = Task(user_id=user_id, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created successfully", "task_id": task.id})


@task_api_bp.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify(
        [{"id": t.id, "user_id": t.user_id, "description": t.description, "completed": t.completed} for t in tasks]
    )


@task_api_bp.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify(
            {"id": task.id, "user_id": task.user_id, "description": task.description, "completed": task.completed}
        )
    else:
        return jsonify({"message": "Task not found"}), 404


@task_api_bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        data = request.get_json()
        user_id = data.get("user_id")
        description = data.get("description")
        completed = data.get("completed")
        if user_id is None or description is None or completed is None:
            return jsonify({"message": "User ID, description, and completed status are required"}), 400
        task.user_id = user_id
        task.description = description
        task.completed = completed
        db.session.commit()
        return jsonify({"message": "Task updated successfully"})
    else:
        return jsonify({"message": "Task not found"}), 404


@task_api_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})
    else:
        return jsonify({"message": "Task not found"}), 404
