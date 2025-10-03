import grpc
from generated import user_service_pb2
from generated import user_service_pb2_grpc

class UserServiceClient:
    def __init__(self, server_address='localhost:50051'):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)
    
    def create_user(self, name, email):
        """Create user"""
        print(f"\n[Create User] Name: {name}, Email: {email}")
        try:
            request = user_service_pb2.CreateUserRequest(name=name, email=email)
            response = self.stub.CreateUser(request)
            
            if response.success:
                print(f"User created successfully: {response.message}")
                print(f"   User ID: {response.user.id}")
                print(f"   Name: {response.user.name}")
                print(f"   Email: {response.user.email}")
                print(f"   Created at: {response.user.created_at}")
                return response.user
            else:
                print(f" User creation failed: {response.message}")
                return None
        except grpc.RpcError as e:
            print(f"gRPC Error: {e.details()}")
            return None
    
    def get_user(self, user_id):
        """Get user"""
        print(f"\n[Get User] ID: {user_id}")
        try:
            request = user_service_pb2.UserRequest(id=user_id)
            response = self.stub.GetUser(request)
            
            if response.success:
                print(f"User retrieved successfully: {response.message}")
                print(f"   User ID: {response.user.id}")
                print(f"   Name: {response.user.name}")
                print(f"   Email: {response.user.email}")
                print(f"   Created at: {response.user.created_at}")
                return response.user
            else:
                print(f"User retrieval failed: {response.message}")
                return None
        except grpc.RpcError as e:
            print(f" gRPC Error: {e.details()}")
            return None
    
    def get_all_users(self):
        """Get all users"""
        print(f"\n[Get All Users]")
        try:
            request = user_service_pb2.Empty()
            response = self.stub.GetAllUsers(request)
            
            if response.success:
                print(f"User list retrieved successfully, {response.count} users:")
                for i, user in enumerate(response.users, 1):
                    print(f"   {i}. ID: {user.id}, Name: {user.name}, Email: {user.email}")
                return response.users
            else:
                print(f"Failed to retrieve user list")
                return []
        except grpc.RpcError as e:
            print(f"gRPC Error: {e.details()}")
            return []
    
    def update_user(self, user_id, name=None, email=None):
        """Update user"""
        print(f"\n[Update User] ID: {user_id}")
        if name:
            print(f"   New name: {name}")
        if email:
            print(f"   New email: {email}")
        
        try:
            request = user_service_pb2.UpdateUserRequest(
                id=user_id,
                name=name or "",
                email=email or ""
            )
            response = self.stub.UpdateUser(request)
            
            if response.success:
                print(f"User updated successfully: {response.message}")
                print(f"   User ID: {response.user.id}")
                print(f"   Name: {response.user.name}")
                print(f"   Email: {response.user.email}")
                return response.user
            else:
                print(f" User update failed: {response.message}")
                return None
        except grpc.RpcError as e:
            print(f" gRPC Error: {e.details()}")
            return None
    
    def delete_user(self, user_id):
        """Delete user"""
        print(f"\n[Delete User] ID: {user_id}")
        try:
            request = user_service_pb2.UserRequest(id=user_id)
            response = self.stub.DeleteUser(request)
            
            if response.success:
                print(f"User deleted successfully: {response.message}")
                return True
            else:
                print(f" User deletion failed: {response.message}")
                return False
        except grpc.RpcError as e:
            print(f" gRPC Error: {e.details()}")
            return False
    
    def close(self):
        """Close connection"""
        self.channel.close()

def interactive_mode():
    """Interactive mode"""
    client = UserServiceClient()
    
    print("\n=== gRPC User Service Interactive Mode ===")
    print("Available commands:")
    print("1. create <name> <email> - Create user")
    print("2. get <id> - Get user")
    print("3. list - Get all users")
    print("4. update <id> <name> <email> - Update user")
    print("5. delete <id> - Delete user")
    print("6. quit - Exit")
    print("=" * 30)
    
    try:
        while True:
            command = input("\nEnter command: ").strip().split()
            
            if not command:
                continue
                
            action = command[0].lower()
            
            if action == 'quit':
                break
            elif action == 'create' and len(command) > 2:
                client.create_user(command[1], command[2])
            elif action == 'get' and len(command) > 1:
                client.get_user(command[1])
            elif action == 'list':
                client.get_all_users()
            elif action == 'update' and len(command) > 3:
                client.update_user(command[1], command[2], command[3])
            elif action == 'delete' and len(command) > 1:
                client.delete_user(command[1])
            else:
                print("Invalid command or insufficient parameters, please try again")
                
    except KeyboardInterrupt:
        print("\n\nUser interrupted operation")
    except Exception as e:
        print(f"Command execution error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    interactive_mode()