# task_project/Task_Manager/apis/task_assignment.py

from flask_restx import Resource, Namespace, fields
from auth_project.authentication.models import User
from task_project.Task_Manager.db import db
from task_project.Task_Manager.models import TaskAssignment
from task_project.Task_Manager.schema.taskassignment_schema import TaskAssignmentSchema
from task_project.Task_Manager.token_required import token_required
from flask import request

task_assignment_ns = Namespace("task_assignment", description="Task assignment operations")

task_assignment_model = task_assignment_ns.model(
    "TaskAssignment",
    {
        "id": fields.Integer(readonly=True, description="TaskAssignment ID"),
        "task_id": fields.Integer(required=True, description="Task ID"),
        "user_id": fields.Integer(required=True, description="User ID"),
    },
)

task_assignment_schema = TaskAssignmentSchema()
task_assignments_schema = TaskAssignmentSchema(many=True)

@task_assignment_ns.route("/task_assignment")
class TaskAssignmentList(Resource):
    """
    Shows a list of all task assignments, and lets you POST to add new task assignments
    """

    @task_assignment_ns.doc(security="apikey")
    @task_assignment_ns.expect(task_assignment_model)
    @task_assignment_ns.marshal_list_with(task_assignment_model)
    @token_required
    def get(self, user_id, valid):
        """
        List all task assignments
        """
        task_assignments = TaskAssignment.query.all()
        return task_assignments_schema.dump(task_assignments)

    @task_assignment_ns.doc(security="apikey")
    @task_assignment_ns.expect(task_assignment_model)
    @task_assignment_ns.marshal_with(task_assignment_model, code=201)
    @token_required
    def post(self, user_id, valid):
        """
        Create a new task assignment
        """
        try:
            data = request.get_json()
            task_id = data.get("task_id")
            user_id = data.get("user_id")

            # Check if both task_id and user_id exist
            if not task_id or not user_id:
                return {"message": "Task ID and User ID are required"}, 400

            # Check if the user exists
            user = User.query.get(user_id)
            if not user:
                return {"message": f"User with ID {user_id} not found"}, 404

            new_task_assignment = TaskAssignment(task_id=task_id, user_id=user_id)
            db.session.add(new_task_assignment)
            db.session.commit()

            return task_assignment_schema.dump(new_task_assignment), 201

        except Exception as e:
            return {"message": "An error occurred during task assignment creation"}, 500

@task_assignment_ns.route("/task_assignment/<int:id>")
class TaskAssignmentView(Resource):
    """
    Show a single task assignment item and lets you delete them
    """

    @task_assignment_ns.doc(security="apikey")
    @task_assignment_ns.marshal_with(task_assignment_model)
    @token_required
    def get(self, user_id, valid, id):
        """
        Fetch a given task assignment
        """
        task_assignment = TaskAssignment.query.get_or_404(id)
        return task_assignment_schema.dump(task_assignment)

    @task_assignment_ns.doc(security="apikey")
    @task_assignment_ns.expect(task_assignment_model)
    @token_required
    def delete(self, user_id, valid, id):
        """
        Delete a task assignment given its identifier
        """
        task_assignment = TaskAssignment.query.get_or_404(id)
        if task_assignment:
            db.session.delete(task_assignment)
            db.session.commit()
            return {"message": "Task Assignment deleted successfully"}
        else:
            return {"message": f"Task Assignment with ID {id} not found"}, 404

    @task_assignment_ns.doc(security="apikey")
    @task_assignment_ns.expect(task_assignment_model)
    @task_assignment_ns.marshal_with(task_assignment_model)
    @token_required
    def put(self, user_id, valid, id):
        """
        Update a task assignment given its identifier
        """
        data = request.json
        task_assignment = TaskAssignment.query.get(id)
        if not task_assignment:
            task_assignment_ns.abort(404, "Task Assignment not found")
        
        task_assignment.task_id = data.get('task_id', task_assignment.task_id)
        task_assignment.user_id = data.get('user_id', task_assignment.user_id)

        db.session.commit()
        return task_assignment_schema.dump(task_assignment), 200
