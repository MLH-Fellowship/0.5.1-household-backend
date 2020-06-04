from flask import Blueprint, request, jsonify
from app.models import Task


task_blueprint = Blueprint("task", __name__, url_prefix="/task")

@task_blueprint.route("/<int:identifier>/", methods=("GET",))
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


@task_blueprint.route("/<int:identifier>/update/", methods=("POST","UPDATE",))
def update_task(identifier):
    task: Task = Task.query.get(identifier)

    if not task:
        return jsonify({
            "data": identifier,
            "msg": "A task with that identifier does not exist",
            "status": "error",
        }), 403

    # Update database from POST values
    if "name" in request.json:
        task.name = request.json["name"]
    if "description" in request.json:
        task.description = request.json["description"]
    if "frequency" in request.json:
        task.frequency = request.json["frequency"]

    return jsonify(data=identifier, msg="Updated successfully!", status="success"), 200

