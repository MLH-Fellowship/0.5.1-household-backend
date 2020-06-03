from flask import jsonify


def error_missing_json_key(*args):
    if len(args) == 1:
        return jsonify({"msg": "Missing key `{}`".format(args[0]), "status": "error"}), 400
    return jsonify({"msg": "Missing a JSON key of name " + ", ".join(map(lambda x: "`{}`".format(x),
                                                                         args[:-1]
                                                                         )) + " or `{}`".format(args[-1]),
                    "status": "error"}, )
