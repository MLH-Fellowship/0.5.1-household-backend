from flask import jsonify


def error_missing_json_key(*args):
    if args.count() == 1:
        return jsonify({"msg": "Missing key `{}`".format(args[0])}), 400
    else:
        return jsonify({"msg": "Missing one of " + map(lambda x: "`{}`".format(x),
                                                       args[:1]
                                                       ) + "or `{}`".format(args[-1])
                        })
