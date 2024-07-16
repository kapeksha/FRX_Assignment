from flask_restx import Resource, Namespace, fields
from task_project.Task_Manager.db import db
from task_project.Task_Manager.models import Comment
from task_project.Task_Manager.schema.comment_schema import CommentSchema
from flask import request
from task_project.Task_Manager.token_required import token_required
import logging

comment_ns = Namespace("comment", description="Comment operations")
comment_model = comment_ns.model(
    "Comment",
    {
        "id": fields.Integer(readonly=True, description="Comment ID"),
        "content": fields.String(required=True, description="Comment content"),
        "task_id": fields.Integer(required=True, description="Task ID"),
        "email": fields.String(required=True, description="Email"),
        "commenter_name": fields.String(required=True, description="Commenter name"),
    },
)

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

@comment_ns.route("/comment")
class CommentList(Resource):
    """
    Shows a list of all comments, and lets you POST to add new comments
    """

    @comment_ns.doc(security='apikey')
    @comment_ns.marshal_list_with(comment_model)
    @token_required
    def get(self, user_id, valid):
        """
        List all comments
        """
        comments = Comment.query.all()
        return comments_schema.dump(comments)

    @comment_ns.doc('apikey')
    @comment_ns.expect(comment_model)
    @comment_ns.marshal_with(comment_model, code=201)
    @token_required
    def post(self, user_id, valid):
        """
        Create a new comment
        """
        try:
            data = request.get_json()
            email = data.get("email")

            # Check if email already exists
            existing_comment = Comment.query.filter_by(email=email).first()
            if existing_comment:
                return {"message": "A comment with this email already exists."}, 400

            new_comment = comment_schema.load(data)
            db.session.add(new_comment)
            db.session.commit()
            return comment_schema.dump(new_comment), 201
        except Exception as e:
            logging.error(f"Error creating comment: {e}")
            return {"message": "An error occurred during comment creation"}, 500

@comment_ns.route("/comment/<int:id>")
class CommentView(Resource):
    """
    Show a single comment item and lets you delete them
    """

    @comment_ns.doc(security='apikey')
    @comment_ns.marshal_with(comment_model)
    @token_required
    def get(self, user_id, valid, id):
        """
        Fetch a given comment
        """
        comment = Comment.query.get_or_404(id)
        return comment_schema.dump(comment)

    @comment_ns.doc(security='apikey')
    @comment_ns.expect(comment_model)
    @token_required
    def delete(self, user_id, valid, id):
        """
        Delete a comment given its identifier
        """
        comment = Comment.query.get_or_404(id)
        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted successfully"}, 200

    @comment_ns.doc(security='apikey')
    @comment_ns.expect(comment_model)
    @comment_ns.marshal_with(comment_model)
    @token_required
    def put(self, user_id, valid, id):
        """
        Update a comment given its identifier
        """
        try:
            data = request.get_json()
            comment = Comment.query.get(id)
            if not comment:
                comment_ns.abort(404, "Comment not found")

            comment.content = data.get("content", comment.content)
            comment.task_id = data.get("task_id", comment.task_id)
            comment.email = data.get("email", comment.email)
            comment.commenter_name = data.get("commenter_name", comment.commenter_name)

            db.session.commit()
            return comment_schema.dump(comment), 200
        except Exception as e:
            logging.error(f"Error updating comment: {e}")
            return {"message": "An error occurred during comment update"}, 500
