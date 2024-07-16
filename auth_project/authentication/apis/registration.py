from flask_restx import Namespace, Resource, fields
from flask import request
from auth_project.authentication.db import db
from auth_project.authentication.models import User

auth_ns = Namespace('auth', description='Authentication operations')

user_model = auth_ns.model('User', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})
 
@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.get_json()
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201



    
