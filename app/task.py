from flask import Blueprint, jsonify, request
from app.models import Task, User, House
from flask_jwt_extended import get_jwt_identity, jwt_required


task_blueprint = Blueprint("user_task", __name__, url_prefix="/task")


@task_blueprint.route("/<int:task_id>/user_task/", methods=("GET",))
@jwt_required
def get_task(task_id):
    task: Task = Task.query.get(task_id)
    user: User = User.query.get(get_jwt_identity())
    if not task:
        return (
            jsonify(
                {"msg": "That task cannot be found", "status": "error", "data": ""}
            ),
            404,
        )

    house = House.query.get(task.house_id)

    if house not in user.houses:
        return jsonify(
            msg="You don't have permission to view this task's assignments.",
            status="error",
            data="",
        )

    return jsonify(
        data=list(
            map(
                lambda t: {
                    "task_id": t.id,
                    "deadline": t.deadline.timestamp(),
                    "done": t.done,
                    "user_id": t.user_id,
                },
                task.user_tasks,
            )
        ),
        status="success",
        msg="",
    )


@task_blueprint.route("/<int:task_id>")
@jwt_required
def find_task_blueprint(task_id):
    user: User = User.query.get(get_jwt_identity())
    task: Task = Task.query.get(task_id)
    if not task:
        return jsonify(msg="Could not find that task.", status="error", data=""), 404
    house: House = Task.query.get(task.house_id)
    if not house in user.houses:
        return (
            jsonify(
                msg="You don't have permission to do that.", status="error", data=""
            ),
            403,
        )
    return jsonify(
        data={
            "task_id": task.id,
            "description": task.description,
            "frequency": task.frequency,
            "name": task.name,
        },
        msg="",
        status="success",
    )


@task_blueprint.route("/<int:task_id>/update", methods=("POST", "UPDATE"))
@jwt_required
def update_task(task_id):
    user: User = User.query.get(get_jwt_identity())
    task: Task = Task.query.get(task_id)
    if not task:
        return jsonify(msg="Could not find that task", status="error", data=""), 404
    house: House = House.query.get(task.house_id)
    if not house in user.houses:
        return (
            jsonify(
                msg="You don't have permission to do that.", status="error", data=""
            ),
            403,
        )
    try:
        task.name = request.json["name"]
    except TypeError:
        pass
    try:
        task.description = request.json["description"]
    except TypeError:
        pass
    try:
        task.frequency = request.json["description"]
    except TypeError:
        pass
    db.session.commit()
    return jsonify(data=task.id, status="success", msg="Updated that task.")

