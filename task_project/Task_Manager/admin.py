from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from models import Project, Task, TaskAssignment, Comment

admin = Admin(app, name="Task Manager Admin", template_mode="bootstrap3")

admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Task, db.session))
admin.add_view(ModelView(TaskAssignment, db.session))
admin.add_view(ModelView(Comment, db.session))
