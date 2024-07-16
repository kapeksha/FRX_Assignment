import logging
import os
import grpc
from concurrent import futures
import time
from proto.auth_pb2 import AuthResponse
from proto.token_verify import token_verification
from proto import auth_pb2_grpc

project_directory = os.path.dirname(os.path.realpath(__file__))
directory_path = os.path.join(project_directory, "logs")
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

logging.basicConfig(
    filename=os.path.join(directory_path, "grpc_server.log"), level=logging.DEBUG
)

SECRET_KEY = 'taskauth'

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Authenticate(self, request, context):
        logging.info("Received authentication request")
        
        # Verify the token and extract user_id and valid status
        user_id, valid = token_verification(request.token)

        if valid:
            logging.info(f"Authentication successful with user_id: {user_id}")
        else:
            logging.error(f"Authentication unsuccessful valid: {valid}")
        
        # Assuming your token_verification function returns user_id and valid
        return AuthResponse(user_id=str(user_id),valid=valid)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()