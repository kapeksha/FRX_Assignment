from flask import Config
from flask_restx import Namespace, Resource, reqparse
import jwt
from auth_project.authentication.config import Config

auth_ns = Namespace("auth", description="Authentication operations")

parser = reqparse.RequestParser()
parser.add_argument("Authorization", location="headers")

blacklist = set() 

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        if auth_token in blacklist:
            return "Token blacklisted. Please log in again."
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."


def blacklist_token(auth_token):
    blacklist.add(auth_token)

@auth_ns.route("/logout")
class Logout(Resource):
    @auth_ns.doc(security="apikey")
    @auth_ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        auth_header = args["Authorization"]
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
                resp = decode_auth_token(auth_token)
                if isinstance(resp, str):
                    return {"message": resp}, 401
                blacklist_token(auth_token)
                return {"message": "Successfully logged out"}, 200
            except IndexError:
                return {"message": "Bearer token malformed"}, 401
        else:
            return {"message": "Provide a valid auth token"}, 403
