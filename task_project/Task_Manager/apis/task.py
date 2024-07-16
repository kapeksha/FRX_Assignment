from flask_restx import Resource, Namespace, fields
from task_project.Task_Manager.db import db
from task_project.Task_Manager.models import Task
from flask import request
from task_project.Task_Manager.schema.task_schema import TaskSchema
from task_project.Task_Manager.token_required import token_required
import logging

task_ns = Namespace("task", description="Task operations")
task_model = task_ns.model(
    "Task",
    {
        "id": fields.Integer(readonly=True, description="Task ID"),
        "name": fields.String(required=True, description="Task name"),
        "description": fields.String(description="Task description"),
        "status": fields.String(default="To-Do", description="Task status"),
        "priority": fields.String(description="Task priority"),
        "deadline": fields.Date(description="Task deadline"),
        "project_id": fields.Integer(required=True, description="Project ID"),
    },
)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@task_ns.route("/task")
class TaskList(Resource):
    """
    Shows a list of all tasks, and lets you POST to add new tasks
    """

    @task_ns.doc(security="apikey")
    @task_ns.expect(task_model)
    @task_ns.marshal_list_with(task_model)
    @token_required
    def get(self, user_id, valid):
        """
        List all tasks
        """
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

    @task_ns.doc(security="apikey")
    @task_ns.expect(task_model)
    @task_ns.marshal_with(task_model, code=201)
    @token_required
    def post(self, user_id, valid):
        """
        Create a new task
        """
        try:
            data = request.get_json()
            new_task = task_schema.load(data)
            db.session.add(new_task)
            db.session.commit()
            return task_schema.dump(new_task), 201
        except Exception as e:
            logging.error(f"Error creating task: {e}")
            return {"message": "An error occurred during task creation"}, 500

@task_ns.route("/task/<int:id>")
class TaskView(Resource):
    """
    Show a single task item and lets you delete them
    """

    @task_ns.doc(security="apikey")
    @task_ns.expect(task_model)
    @task_ns.marshal_with(task_model)
    @token_required
    def get(self, user_id, valid, id):
        """
        Fetch a given task
        """
        task = Task.query.get_or_404(id)
        return task_schema.dump(task)

    @task_ns.doc(security="apikey")
    @task_ns.expect(task_model)
    @token_required
    def delete(self, user_id, valid, id):
        """
        Delete a task given its identifier
        """
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully"}, 200

    @task_ns.doc(security="apikey")
    @task_ns.expect(task_model)
    @task_ns.marshal_with(task_model)
    @token_required
    def put(self, user_id, valid, id):
        """
        Update a task given its identifier
        """
        task = Task.query.get(id)
        if not task:
            task_ns.abort(404, "Task not found")

        try:
            data = request.get_json()
            task.name = data.get("name", task.name)
            task.description = data.get("description", task.description)
            task.status = data.get("status", task.status)
            task.priority = data.get("priority", task.priority)
            task.deadline = data.get("deadline", task.deadline)
            task.project_id = data.get("project_id", task.project_id)
            db.session.commit()
            return task_schema.dump(task), 200
        except Exception as e:
            logging.error(f"Error updating task: {e}")
            return {"message": "An error occurred during task update"}, 500
