from flask import Blueprint, jsonify
from app.models import UserTask, UserHouse


user_task_blueprint = Blueprint("user_task", __name__)


@user_task_blueprint.route("/task/<int:identifier>/user_task/", \
                           methods=("GET",))
def get_task(identifier):
    user_task: UserTask = UserTask.query.get(identifier)

    if not user_task:
        return jsonify({"data": identifier, "status": "error", \
            "msg": "A user_task with that identifier does not exist."}), 403

    data = {}
    data["user_id"] = user_task.user_id
    data["task_id"] = user_task.task_id
    data["deadline"] = user_task.deadline

    # Get house id from UserHouse using user_id
    user_house: UserHouse = UserHouse.query.filter(UserHouse.user_id == \
                                                   user_task.user_id).first()
    data["house_id"] = user_house.house_id

    return jsonify(data=data, msg="", status="success"), 200
