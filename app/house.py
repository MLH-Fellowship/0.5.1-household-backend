from flask import Blueprint, jsonify, current_app, request, url_for
from app.models import House, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import error_missing_json_key
import jwt
from app import db

house_blueprint = Blueprint("house", __name__, url_prefix="/house")


@house_blueprint.route("/add", methods=("POST",))
@jwt_required
def add_house():
    try:
        name = request.json["name"]
        description = request.json["description"]
    except TypeError:
        return error_missing_json_key("name", "description")
    user = get_jwt_identity()
    db_user: User = User.query.get(user)
    house = House(name=name, description=description)
    db_user.houses.append(house)
    db.session.add(house)
    db.session.commit()
    db.session.refresh(house)
    return jsonify(
        msg="Created that house succesfully.", data=house.id, status="success"
    )


@house_blueprint.route("/user/join")
@jwt_required
def join_house():
    token = request.args["token"]
    user = get_jwt_identity()
    db_user: User = User.query.get(user)
    if not user:
        return (
            jsonify(msg="The supplied token was invalid.", status="error", data=""),
            400,
        )
    try:
        try:
            decoded_token = jwt.decode(token, current_app.config["SECRET_KEY"])
        except jwt.DecodeError:
            return (
                jsonify(msg="The supplied token was invalid.", status="error", data=""),
                400,
            )
        if decoded_token["token_type"] == "specific_join_house":
            if db_user.id == decoded_token["user_id"]:
                User.houses.append(House.query.get(decoded_token["house_id"]))
                db.session.commit()
                return jsonify(
                    {
                        "msg": "You are now in this house.",
                        "data": decoded_token["house_id"],
                        "status": "success",
                    }
                )
            else:
                return jsonify(
                    {
                        "msg": "You cannot use this token – it is for someone else.",
                        "status": "error",
                        "data": "",
                    }
                )
        elif decoded_token["token_type"] == "generic_join_house":
            db_user.houses.append(House.query.get(decoded_token["house_id"]))
            db.session.commit()
            return jsonify(
                {
                    "msg": "You are now in this house.",
                    "data": decoded_token["house_id"],
                    "status": "success",
                }
            )
    except jwt.DecodeError:
        return (
            jsonify(msg="The supplied token was invalid.", status="error", data=""),
            400,
        )


@house_blueprint.route("/<int:house_id>/user/invite/<string:identifier>")
def specific_email(house_id, identifier):
    house = House.query.get(house_id)
    if not house.users.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first():
        return jsonify(
            {
                "status": "error",
                "msg": "You don't have permission to do this",
                "data": "",
            }
        )
    user = User.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()
    if not user:
        return (
            jsonify(
                {"msg": "That user could not be found.", "status": "error", "data": ""}
            ),
            404,
        )
    if not house:
        return (
            jsonify(
                status="error", msg="A house with that ID cannot be found", data=""
            ),
            404,
        )
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


@house_blueprint.route("/user")
@jwt_required
def all_user_houses():
    user = get_jwt_identity()
    db_user: User = User.query.get(user)
    return jsonify(
        {
            "data": list(map(lambda x: x.id, db_user.houses)),
            "msg": "",
            "status": "success",
        }
    )


@house_blueprint.route("/<int:house_id>/user/invite")
def generic_invite(house_id):
    house = House.query.get(house_id)
    if house:
        token = url_for(
            "house.join_house",
            token=jwt.encode(
                {"token_type": "generic_join_house", "house_id": house.id},
                current_app.config["SECRET_KEY"],
            ),
        )
        return jsonify(data=token, msg="", status="success")
    return (
        jsonify(status="error", msg="A house with that ID cannot be found.", data=""),
        404,
    )
