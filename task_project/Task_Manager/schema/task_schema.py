from flask_marshmallow import Marshmallow
from task_project.Task_Manager.models import Task

ma = Marshmallow()

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    status = ma.auto_field()
    priority = ma.auto_field()
    deadline = ma.auto_field()
    project_id = ma.auto_field()
