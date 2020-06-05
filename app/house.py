from flask import Blueprint, jsonify, current_app, request, url_for
from app.models import House, User, Task, WorkerTask
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import error_missing_json_key
import jwt
from app import db
import sqlalchemy.exc as exc

import datetime

house_blueprint = Blueprint("house", __name__, url_prefix="/house")


@house_blueprint.route("/<int:house_id>/get")
@jwt_required
def get_house(house_id):
    house = House.query.get(house_id)
    user: User = User.query.get(get_jwt_identity())
    if not user:
        return jsonify(status="error", msg="The supplied token is invalid.", data="")
    if not house in user.houses:
        return jsonify(
            status="error", msg="You don't have permission to do that", data=""
        )
    return jsonify(
        data={
            "house_id": house.id,
            "name": house.name,
            "description": house.description,
        },
        status="success",
        msg="",
    )


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
        decoded_token = jwt.decode(token, current_app.config["SECRET_KEY"])
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
    house = House.query.get(house_id)
    if not house:
        return (
            jsonify(
                status="error", msg="A house with that ID cannot be found", data=""
            ),
            404,
        )
    if not house in user.houses:
        return jsonify(
            {
                "status": "error",
                "msg": "You don't have permission to do this",
                "data": "",
            }
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
    user = User.query.get(get_jwt_identity())
    return jsonify(
        msg="",
        status="success",
        data=list(
            map(
                lambda x: {
                    "house_id": x.id,
                    "name": x.name,
                    "description": x.description,
                },
                user.houses,
            )
        ),
    )


@house_blueprint.route("/<int:house_id>/task/all")
@jwt_required
def get_house_tasks(house_id):
    user: User = User.query.get(get_jwt_identity())
    if not user:
        return (
            jsonify(status="error", msg="The provided token is invalid.", data=""),
            400,
        )
    house: House = House.query.get(house_id)
    if not house:
        return (
            jsonify(
                status="error",
                msg="A house with those details cannot be found.",
                data="",
            ),
            404,
        )
    if not house in user.houses:
        return jsonify(
            msg="You don't have permission to do that.", status="error", data=""
        )
    return jsonify(
        msg="",
        status="success",
        data=list(
            map(
                lambda x: {
                    "task_id": x.id,
                    "description": x.description,
                    "frequency": x.frequency,
                    "name": x.name,
                },
                house.tasks,
            )
        ),
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


@house_blueprint.route("/update", methods=("POST", "UPDATE"))
@jwt_required
def update_house():
    try:
        house_id = request.json["house_id"]
    except TypeError:
        return jsonify(error_missing_json_key("house_id"))
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify(msg="The token supplied is not valid.", data="", status="error")
    house: House = House.query.get(house_id)
    if house not in user.houses:
        return jsonify(
            msg="You don't have permission to do that.", data="", status="error"
        )
    try:
        house.name = request.json["name"]
    except KeyError:
        pass
    try:
        house.value = request.json["description"]
    except KeyError:
        pass
    db.session.commit()
    return jsonify(
        {"msg": "Updated successfully!", "status": "success", "data": house.id}
    )


@house_blueprint.route("<int:house_id>/task/add", methods=("PUT", "POST"))
@jwt_required
def add_house_task(house_id):
    try:
        name = request.json["name"]
        description = request.json["description"]
        frequency = request.json["frequency"]
    except TypeError:
        return error_missing_json_key("name", "description", "frequency"), 400
    user: User = User.query.get(get_jwt_identity())
    if not user:
        return (
            jsonify(status="error", msg="The supplied token is invalid.", data=""),
            400,
        )
    house: House = House.query.get(house_id)
    if not house:
        return (
            jsonify(
                status="error", msg="The requested house could not be found", data=""
            ),
            404,
        )
    if not house in user.houses:
        return (
            jsonify(
                status="error", msg="You don't have permission to do that.", data=""
            ),
            403,
        )
    new_task = Task(
        name=name, description=description, house_id=house_id, frequency=frequency
    )
    try:
        db.session.add(new_task)
        db.session.commit()
        db.session.refresh(new_task)
    except exc.DatabaseError:
        return (
            jsonify(
                msg="Error adding that task to the database", status="error", data=""
            ),
            500,
        )
    try:
        wt = WorkerTask(
            complete_at=datetime.datetime.now() + new_task.frequency,
            context="{},{}".format(house.id, new_task.id),
            task_type=1,
        )
        db.session.add(wt)
        db.session.commit()
    except:
        pass
    return jsonify(msg="Created a new task!", status="success", data=new_task.id)
