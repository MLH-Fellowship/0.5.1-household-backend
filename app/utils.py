from flask import jsonify
import json
import requests
import os


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
    return requests.request(
        data=json.dumps(
            {
                "personalizations": [
                    {
                        "to": [{"email": to}]
                        if isinstance(to, str)
                        else [{"email": email} for email in to]
                    },
                ],
                "subject": subject,
                "from": {"email": from_email},
                "content": [
                    {"type": "text/plain", "value": text},
                    {"type": "text/html", "value": html},
                ],
            }
        ),
        method="POST",
        url="https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": "Bearer {}".format(api_key),
            "Content-Type": "application/json",
        },
    )
