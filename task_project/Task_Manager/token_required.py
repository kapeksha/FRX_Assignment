from functools import wraps
from flask import request
from flask_restx import abort


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from .proto.auth_client import authentication

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            abort(401, description="Missing Authorization header!")

        token = auth_header.split()[1].strip()
        
        if not token:
            abort(401, description="Missing token")

        user_id, valid = authentication(token)

        if not valid:
            abort(401, description="Invalid token!")

        return f(*args, user_id=user_id, valid=valid, **kwargs)
    
    return decorated


