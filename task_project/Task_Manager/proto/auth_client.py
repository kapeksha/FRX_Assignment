import os
import grpc
import logging
from ..proto import auth_pb2
from ..proto import auth_pb2_grpc


project_directory = os.path.dirname(os.path.realpath(__file__))
directory_path = os.path.join(project_directory, "logs")
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

logging.basicConfig(
    filename=os.path.join(directory_path, "grpc_client.log"), level=logging.DEBUG
)

def authentication(token):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        request = auth_pb2.AuthRequest(token = token)
        try:
            logging.info("Sending authentication request with token: %s", token) 
            response = stub.Authenticate(request)
            logging.info(f"Authentication response received: user_id: {response.user_id}, valid: {response.valid}")
            return  response.user_id, response.valid
        except grpc.RpcError as e:
            logging.error(f"gRPC error during authentication: {e}")
            raise