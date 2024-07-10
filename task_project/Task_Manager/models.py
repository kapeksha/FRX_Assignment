from task_project.Task_Manager.db import db


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    tasks = db.relationship("Task", backref="project", lazy=True)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default="To-Do")
    priority = db.Column(db.String(20))
    deadline = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    assignments = db.relationship("TaskAssignment", backref="task", lazy=True)
    comments = db.relationship("Comment", backref="task", lazy=True)


class TaskAssignment(db.Model):
    __tablename__ = "taskassignment"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    commenter_name = db.Column(db.String(80), nullable=False)
