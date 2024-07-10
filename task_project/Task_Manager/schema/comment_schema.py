from flask_marshmallow import Marshmallow
from task_project.Task_Manager.models import Comment

ma = Marshmallow()


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        

    id = ma.auto_field()
    content = ma.auto_field()
    task_id = ma.auto_field()
    email = ma.auto_field()
    commenter_name = ma.auto_field()
    
