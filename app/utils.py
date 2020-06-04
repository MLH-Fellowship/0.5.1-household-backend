from flask import jsonify, current_app
import json
import requests
import os
import enum
from flask_mail import Message
from app import mail


# TODO: refactor to use this in creating JWTs
class CustomJWTTypes(enum.Enum):
    EMAIL_VERIFY = 1
    PASSWORD_RESET = 2
    GENERIC_HOUSE_INVITE = 3
    SPECIFIC_HOUSE_INVITE = 4


def error_missing_json_key(*args):
    if len(args) == 1:
        return (
            jsonify({"msg": "Missing key `{}`".format(args[0]), "status": "error"}),
            400,
        )
    return jsonify(
        {
            "msg": "Missing a JSON key of name "
            + ", ".join(map(lambda x: "`{}`".format(x), args[:-1]))
            + " or `{}`".format(args[-1]),
            "status": "error",
        },
    )


def send_email(
    to,
    subject,
    html,
    text,
    from_email="bureaucrat@hackathon-household-app.herokuapp.com/",
    api_key=os.environ.get("SENDGRID_API_KEY"),
):
    msg = Message(subject, sender=from_email, recipients=[to])
    msg.body = text
    msg.html = html
    try:
        mail.send(msg)
    except Exception as e:
        print(e)
