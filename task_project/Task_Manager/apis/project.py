from flask_restx import Resource, Namespace, fields
from task_project.Task_Manager.db import db
from task_project.Task_Manager.models import Project
from task_project.Task_Manager.schema.project_schema import ProjectSchema
from flask import logging, request
from task_project.Task_Manager.token_required import token_required


project_ns = Namespace("project", description="Project operations")
project_model = project_ns.model(
    "Project",
    {
        "id": fields.Integer(readonly=True, description="Project ID"),
        "name": fields.String(required=True, description="Project name"),
        "description": fields.String(description="Project description"),
        "start_date": fields.Date(required=True, description="Start Date"),
        "end_date": fields.Date(required=True, description="End Date")
    },
)

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

@project_ns.route("/project")
class ProjectList(Resource):
    """
    Shows a list of all projects, and lets you POST to add new projects
    """
    @project_ns.doc(security='apikey')
    @project_ns.marshal_list_with(project_model)
    @token_required
    def get(self, user_id, valid):
        """
        List all projects
        """
        projects = Project.query.all()
        return projects_schema.dump(projects)

    @project_ns.doc("apikey")
    @project_ns.expect(project_model)
    @project_ns.marshal_with(project_model)
    @token_required
    def post(self, user_id, valid):
        """
        Create a new project
        """
        try:
            data = request.get_json()
            new_project = project_schema.load(data)
            db.session.add(new_project)
            db.session.commit()
            return project_schema.dump(new_project), 201
        except Exception as e:
            return {"message": "An error occurred during project creation"}, 500


@project_ns.route("/project/<int:id>")
class ProjectView(Resource):
    """
    Show a single project item and lets you delete them
    """
    @project_ns.doc(security='apikey')
    @project_ns.expect(project_model)
    @project_ns.marshal_with(project_model)
    @token_required
    def get(self, user_id, valid, id):
        """
        Fetch a given project
        """
        project = Project.query.get_or_404(id)
        return project_schema.dump(project)

    @project_ns.doc(security='apikey')
    @project_ns.expect(project_model)
    @token_required
    def delete(self, user_id, valid, id):
        """
        Delete a project given its identifier
        """
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        return {"message": "Project deleted successfully"}, 200
        # project = Project.query.get_or_404(id)
        # if project:
        #     db.session.delete(project)
        #     db.session.commit()
        #     return {"message": "Project deleted validfully"}
        # else:
        #     return {"message": "Project with ID %d not found" % id}, 404

    @project_ns.doc(security='apikey')
    @project_ns.expect(project_model)
    @project_ns.marshal_with(project_model)
    @token_required
    def put(self, user_id, valid, id):
        """
        Update a project given its identifier
        """

        data = request.json
        project = Project.query.get(id)
        if not project:
            project_ns.abort(404, "Project not found")

        try:
            project.name = data.get("name", project.name)
            project.description = data.get("description", project.description)
            project.start_date = data.get("start_date", project.start_date)
            project.end_date = data.get("end_date", project.end_date)
            db.session.commit()
            return project_schema.dump(project), 200
        except Exception as e:
            logging.error(f"Error updating project: {e}")
            return {"message": "An error occurred during project update"}, 500

        # data = request.json
        # project = Project.query.get(id)
        # if not project:
        #     project_ns.abort(404, "Project not found")
        # project = project_schema.load(data)
        # db.session.commit()
        # return project_schema.dump(project), 200

