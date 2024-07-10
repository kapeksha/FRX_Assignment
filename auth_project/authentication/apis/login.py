from flask_restx import Namespace, Resource, fields
from flask import request
from auth_project.authentication.models import User
from auth_project.authentication.jwt import encode_auth_token


auth_ns = Namespace('auth', description='Authentication operations')

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc(security='apikey')
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and data['password']:
            token = encode_auth_token(user.id)
            return {'message': 'Login successful', 'token': token}, 200
        return {'message': 'Invalid credentials'}, 401

