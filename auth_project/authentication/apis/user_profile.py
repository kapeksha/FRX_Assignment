from flask_jwt_extended import get_jwt_identity
from flask_restx import Namespace, Resource
# from .decorators import token_required
auth_ns = Namespace('auth', description='Authentication operations')

@auth_ns.route('/profile')
class UserProfile(Resource):
    @auth_ns.doc(security='apikey')
    # @token_required
    def get(self):
        current_user = get_jwt_identity()

