from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from task_project.Task_Manager.models import Project


ma = Marshmallow()

class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
