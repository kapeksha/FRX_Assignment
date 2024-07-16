from flask import Flask
from task_project.Task_Manager.config import Config
from flask_migrate import Migrate
from flask_restx import Api
from task_project.Task_Manager.db import db,ma

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)


authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    app,
    title="Task Manager API",
    version="1.0",
    description="Task Manager",    
    authorizations=authorizations,
    security="apikey",
)

from .Task_Manager.apis.comment import comment_ns
from .Task_Manager.apis.project import project_ns
from .Task_Manager.apis.task import task_ns
from .Task_Manager.apis.task_assignment import task_assignment_ns

api.add_namespace(comment_ns)
api.add_namespace(project_ns)
api.add_namespace(task_assignment_ns)
api.add_namespace(task_ns)

