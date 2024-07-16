from flask import Flask
from auth_project.authentication.config import Config
from auth_project.authentication.db import db, ma
from flask_migrate import Migrate
from flask_restx import Api

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)


authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    app,
    title="Authentication API",
    version="1.0",
    description="A simple Authentication API",
    authorizations=authorizations,
    security="apikey",
)

from auth_project.authentication.apis.registration import auth_ns as registration_ns
from auth_project.authentication.apis.login import auth_ns as login_ns
from auth_project.authentication.apis.logout import auth_ns as logout_ns
from auth_project.authentication.apis.user_profile import auth_ns as profile_ns

api.add_namespace(registration_ns, path="/auth")
api.add_namespace(login_ns, path="/auth")
api.add_namespace(logout_ns, path="/auth")
api.add_namespace(profile_ns, path="/auth")
