from task_project.Task_Manager.db import ma
from task_project.Task_Manager.models import Comment

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        include_fk = True  

    id = ma.auto_field()
    task_id = ma.auto_field()
    content = ma.auto_field()
    email = ma.auto_field()
    commenter_name = ma.auto_field()
