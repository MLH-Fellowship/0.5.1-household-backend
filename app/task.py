from flask import Blueprint, request, jsonify
from app.models import Task


task_blueprint = Blueprint("task", __name__)

@task_blueprint.route("/task/<int:identifier>/", \
                           methods=("GET",))
def get_task(identifier):
    task: Task = Task.query.get(identifier)

    if not task:
        return jsonify({
            "data": identifier,
            "msg": "A task with that identifier does not exist",
            "status": "error",
        }), 403

    data = {}
    data["name"] = task.user_id
    data["id"] = task.task_id
    data["description"] = task.deadline
    data["frequency"] = task.frequency

    return jsonify(data=data, msg="", status="success"), 200


@task_blueprint.route("/task/<int:identifier>/update/", \
                           methods=("POST",))
def update_task(identifier):
    task: Task = Task.query.get(identifier)

    if not task:
        return jsonify({
            "data": identifier,
            "msg": "A task with that identifier does not exist",
            "status": "error",
        }), 403

    # Update database from POST values
    if "name" in request.form:
        task.name = request.form["name"]
    if "description" in request.form:
        task.description = request.form["description"]
    if "frequency" in request.form:
        task.frequency = request.form["frequency"]

    return jsonify(data=identifier, msg="Task updated", status="success"), 200

