from flask import jsonify, render_template, Blueprint
from models.task import Task


task_bp = Blueprint("task", __name__)


@task_bp.route("/tasks", methods=["GET"])
def tasks():
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)


@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
def task(task_id):
    task = Task.query.get(task_id)
    if task:
        return render_template("task.html", task=task)
    else:
        return jsonify({"message": "task not found"}), 404
