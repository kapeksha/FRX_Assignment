import logging
import os
from .auth_pb2_grpc import AuthServiceServicer
from .auth_pb2 import AuthResponse
from token_verify import token_verification

"""
Create log directory
"""
project_directory = os.path.dirname(os.path.realpath(__file__))
directory_path = os.path.join(project_directory, "logs")
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

logging.basicConfig(
    filename=os.path.join(directory_path, "grpc_server.log"), level=logging.DEBUG
)

 
class AuthService(AuthServiceServicer):
    def Authenticate(self, request, context):
        logging.info("Recieved authentication request")
        if request.token:
            user_id, valid = token_verification(request.token)

            if valid:
                logging.info(f"Authentication successful with user id: {user_id}!")
            else:
                logging.warning(f"AUthentication unsuccessful valid : {valid}!")
        return AuthResponse(user_id=user_id, valid=valid)

 
