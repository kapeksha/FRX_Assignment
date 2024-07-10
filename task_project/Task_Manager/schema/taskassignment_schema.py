from flask_marshmallow import Marshmallow
from task_project.Task_Manager.models import TaskAssignment

ma = Marshmallow()


class TaskAssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskAssignment

    id = ma.auto_field()
    task_id = ma.auto_field()
    user_id = ma.auto_field()
