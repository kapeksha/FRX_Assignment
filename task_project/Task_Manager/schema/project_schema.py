from task_project.Task_Manager.db import ma
from task_project.Task_Manager.models import Project

class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        include_fk = True 

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
