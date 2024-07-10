from functools import wraps
from flask import request
from flask_restx import abort


SECRET_KEY = "taskauth"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from .proto.auth_client import authentication

        auth_header = request.headers.get("Authorization")
        print("1111", auth_header)

        if not auth_header:
            abort(401, description="Missing Authorization header!")

        token = auth_header.split()[1].strip()
        print(token)
        
        if not token:
            abort(401, description="Missing token")

        success, user_id = authentication(token)

        if not success:
            abort(401, description="Invalid token!")

        return f(*args, user_id=user_id, success=success, **kwargs)
    
    return decorated
