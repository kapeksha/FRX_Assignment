from flask_restx import Resource, Namespace, fields
from task_project.Task_Manager.db import db
from task_project.Task_Manager.models import Comment
from task_project.Task_Manager.schema.comment_schema import CommentSchema
from flask import request
from task_project.Task_Manager.token_required import token_required


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
    @comment_ns.expect(comment_model)
    @comment_ns.marshal_list_with(comment_model)
    @token_required
    def get(self, user_id, success):
        """
        List all comments
        """
        comments = Comment.query.all()
        return comments_schema.dump(comments)

    @comment_ns.doc('apikey')
    @comment_ns.expect(comment_model)
    @comment_ns.marshal_with(comment_model)
    @token_required
    def post(self, user_id, success):
        """
        Create a new comment
        """
        try:
            data = request.get_json()
            new_comment = comment_schema.load(data)
            db.session.add(new_comment)
            db.session.commit()
            return comment_schema.dump(new_comment), 201
        except Exception as e:
            return {"message": "An error occurred during comment creation"}, 500


@comment_ns.route("/comment/<int:id>")
class CommentView(Resource):
    """
    Show a single comment item and lets you delete them
    """
    @comment_ns.doc(security='apikey')
    @comment_ns.expect(comment_model)
    @comment_ns.marshal_with(comment_model)
    @token_required
    def get(self, user_id, success, id):
        """
        Fetch a given comment
        """
        comment = Comment.query.get_or_404(id)
        return comment_schema.dump(comment)

    @comment_ns.doc(security='apikey')
    @comment_ns.expect(comment_model)
    @token_required
    def delete(self, user_id, success, id):
        """
        Delete a comment given its identifier
        """
        comment = Comment.query.get_or_404(id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return {"message": "Comment deleted successfully"}
        else:
            return {"message": "Comment with ID %d not found" % id}, 404

    @comment_ns.doc(security='apikey')
    @comment_ns.expect(comment_model)
    @comment_ns.marshal_with(comment_model)
    @token_required
    def put(self, user_id, success, id):
        """
        Update a comment given its identifier
        """
        data = request.json
        comment = Comment.query.get(id)
        if not comment:
            comment_ns.abort(404, "Comment not found")
        comment = comment_schema.load(data)
        db.session.commit()
        return comment_schema.dump(comment), 200
        

