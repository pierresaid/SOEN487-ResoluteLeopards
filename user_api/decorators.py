from flask import request, jsonify, g
from functools import wraps
from helpers.user import hash_password


def filter_empty(d: dict):
    return {k: v for k, v in d.items() if v is not None}


def get_data():
    if request.is_json:
        return request.get_json()
    else:
        return request.form


def hash_password_field(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if ("data" in g) and ("password" in g.data):
            g.data["pwdhash"] = hash_password(g.data["password"])
            del g.data["password"]
        return f(*args, **kwargs)
    return wrapper


def accept_fields(*fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Setup data
                data = get_data()
                if "data" not in g:
                    g.data = dict()

                # Set data values for accepted fields
                for k, v in data.items():
                    if k in fields:
                        g.data[k] = v
            except Exception as e:
                print("error ", e)
                return jsonify({"code": 400, "msg": "Bad Request"}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator


def require_fields(*fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Setup data
                data = get_data()
                if "data" not in g:
                    g.data = dict()
                missing_fields = []

                # Set data values for required fields,
                # add to missing fields if the field was not in the request
                for field in fields:
                    if field not in data:
                        missing_fields.append(field)
                    else:
                        g.data[field] = data[field]

                # Raise an error if fields were missing
                if len(missing_fields) > 0:
                    return jsonify({"code": 400, "msg": f"Bad Request, missing required field{'s' if len(missing_fields) > 1 else ''}: {', '.join(missing_fields)}"}), 400
            except Exception as e:
                print(e)
                return jsonify({"code": 400, "msg": "Bad Request xD"}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator
