import logging
import grpc
from concurrent import futures
import time
import auth_pb2_grpc
from token_verify import token_verification

SECRET_KEY = 'taskauth'
 
class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Authenticate(self, request, context):
        logging.info("Recieved authentication request")
        if request.token:
            print("token is:  ",request.token)
        
            success, user_id = token_verification(request.token)

 
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
 
if __name__ == '__main__':
    serve()