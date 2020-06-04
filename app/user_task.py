from flask import Blueprint, jsonify
from app.models import Task, User, House
from flask_jwt_extended import get_jwt_identity, jwt_required


user_task_blueprint = Blueprint("user_task", __name__)


@user_task_blueprint.route("/task/<int:task_id>/user_task/", methods=("GET",))
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
