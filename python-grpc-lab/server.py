from cmath import polar
import time
import grpc
from concurrent import futures
from generated import user_service_pb2
from generated import user_service_pb2_grpc
from grpc_interceptor.exceptions import NotFound,InvalidArgument
from grpc_interceptor import ExceptionToStatusInterceptor
# realize the service
class UserService(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    
    def CreateUser(self, request, context):
        # create new user
        print(f"Creating user: (name: {request.name}, email: {request.email})")
        # validate request
        if not request.name or not request.email:
            raise InvalidArgument("Name and email are required")
        
        if '@' not in request.email:
            raise InvalidArgument("Invalid email format")
        
        for user in self.users.values():
            if user['email'].lower() == request.email.lower():
                raise InvalidArgument("Email already exists")
                
        try:  
            user_id = str(self.next_id)
            self.next_id += 1
            
            # store user data
            self.users[user_id] = {
                'id': user_id,
                'name': request.name,
                'email': request.email,
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')  
            }
            
            # return created user
            user = user_service_pb2.User(
                id=user_id,
                name=request.name,
                email=request.email,
                created_at=self.users[user_id]['created_at']
            )
            
            return user_service_pb2.UserResponse(
                success=True,
                message="User created successfully",
                user=user
            )
        except Exception as e:
            return user_service_pb2.UserResponse(
                success=False,
                message=f"Failed to create user: {str(e)}",
                user=None,
             
            )
    def GetUser(self, request, context):
        # request is the UserRequest from the client
        # here should return a UserResponse
        print(f"Fetching user: (id: {request.id})")
        user_id = request.id
        if user_id not in self.users:
            raise NotFound(f"User with ID {user_id} not found")
        
        user = self.users[user_id]
        print(f"User fetched successfully: {user}")
        
        # return the user
        user_obj = user_service_pb2.User(
            id=user['id'],
            name=user['name'],
            email=user['email'],
            created_at=user['created_at']
        )
        
        return user_service_pb2.UserResponse(
            success=True,
            message="User fetched successfully",
            user=user_obj
        )

    def GetAllUsers(self, request, context):
        # here should return a UserList
        print(f"Fetching all users")
        try:
            user_list = []
            for user_id, user_data in self.users.items():
                user_obj = user_service_pb2.User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    created_at=user_data['created_at']
                )
                user_list.append(user_obj)
            
            return user_service_pb2.UserList(
                success=True,
                users=user_list,
                count=len(user_list)
            )
        except Exception as e:
            return user_service_pb2.UserList(
                success=False,
                users=[],
                count=0
            )
    
    def UpdateUser(self, request, context):
        print(f"Updating user: (id: {request.id})")
        try:
            user_id = request.id
            if user_id not in self.users:
                raise NotFound(f"User with ID {user_id} not found")
            
            # update user information
            if request.name:
                self.users[user_id]['name'] = request.name
            if request.email:
                self.users[user_id]['email'] = request.email
            
            user_data = self.users[user_id]
            user_obj = user_service_pb2.User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                created_at=user_data['created_at']
            )
            
            return user_service_pb2.UserResponse(
                success=True,
                message="User updated successfully",
                user=user_obj
            )
        except Exception as e:
            return user_service_pb2.UserResponse(
                success=False,
                message=f"Failed to update user: {str(e)}",
                user=None
            )
    
    def DeleteUser(self, request, context):
        print(f"Deleting user: (id: {request.id})")
        user_id = request.id
        if user_id not in self.users:
            raise NotFound(f"User with ID {user_id} not found")
        
        # Delete the user
        deleted_user = self.users.pop(user_id)
        print(f"User deleted successfully: {deleted_user}")
        
        return user_service_pb2.DeleteResonse(
            success=True,
            message="User deleted successfully"
        )

# start the server
def serve():
    interceptors = [
        ExceptionToStatusInterceptor()
    ]
    port = 50051
    # create a server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),interceptors=interceptors)
    # add the service to the server
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    # add the port to the server
    server.add_insecure_port(f'[::]:{port}')  
    server.start()
    print(f"Server started successfully. Listening on [::]:{port}")
    server.wait_for_termination() # wait for the server to terminate

if __name__ == '__main__':
    serve()