from flask import Blueprint, jsonify, current_app
from app.models import House, User
import jwt
import time

house_blueprint = Blueprint("house", __name__, url_prefix="/house")


@house_blueprint.route("/house/<int:house_id>/user/invite/<string:identifier>")
def specific_email(house_id, identifier):
    house = House.query.get(house_id)
    user = house.users.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()
    if not user:
        return (
            jsonify(
                {"msg": "That user could not be found.", "status": "error", "data": ""}
            ),
            404,
        )
    if house:
        token = jwt.encode(
            {
                "token_type": "specific_join_house",
                "house_id": house.id,
                "user_id": user.id,
            },
            current_app.config["SECRET_KEY"],
        )
        return jsonify(
            {
                "msg": "Successfully created an invite link",
                "status": "success",
                "data": token,
            }
        )
    else:
        return (
            jsonify(
                status="error", msg="A house with that ID cannot be found", data=""
            ),
            404,
        )


@house_blueprint.route("/house/<int:house_id>/user/invite")
def generic_invite(house_id):
    house = House.query.get(house_id)
    if house:
        token = jwt.encode(
            {"token_type": "generic_join_house", house_id: house.id},
            current_app.config["SECRET_KEY"],
        )
        return jsonify(data=token, msg="", status="success")
    else:
        return (
            jsonify(
                status="error", msg="A house with that ID cannot be found.", data=""
            ),
            404,
        )
