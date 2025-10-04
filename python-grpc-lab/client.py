import grpc
import time
from generated import user_service_pb2
from generated import user_service_pb2_grpc

class UserServiceClient:
    def __init__(self, server_address='localhost:50051'):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)
        self.test_user_id = None
    
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
    
    #########################################################
    # below is the test code
    def test_service_method_invocation(self):
        """Test service method invocation"""
        print("\n[Test 1] Service method invocation test")
        try:
            # Test GetAllUsers method
            response = self.stub.GetAllUsers(user_service_pb2.Empty())
            
            print(f"Call: GetAllUsers()")
            print(f"Returned user count: {response.count}")
            print(f"Success status: {response.success}")
            
            if response.success:
                print("Service method invocation successful")
                return True
            else:
                print("Service method invocation failed")
                return False
                
        except grpc.RpcError as e:
            print(f"RPC call failed: {e.code()} - {e.details()}")
            return False
    
    def test_data_serialization_deserialization(self):
        """Test data serialization/deserialization"""
        print("\n[Test 2] Data serialization/deserialization test")
        try:
            # Create user with complex data using timestamp to avoid duplicates
            timestamp = str(int(time.time()))
            request = user_service_pb2.CreateUserRequest(
                name='Serialization Test User',
                email=f'serialization{timestamp}@test.com'
            )
            
            print("Sent data:")
            print(f"  name: {request.name}")
            print(f"  email: {request.email}")
            
            response = self.stub.CreateUser(request)
            
            if response.success:
                print("\nReceived data:")
                print(f"  id: {response.user.id}")
                print(f"  name: {response.user.name}")
                print(f"  email: {response.user.email}")
                print(f"  created_at: {response.user.created_at}")
                
                # Verify data integrity
                if (response.user.name == request.name and 
                    response.user.email == request.email):
                    print("Data serialization/deserialization correct")
                    # Store user ID for cleanup
                    self.test_user_id = response.user.id
                    return True
                else:
                    print("Data inconsistency detected")
                    return False
            else:
                print("User creation failed")
                return False
                
        except grpc.RpcError as e:
            print(f"RPC call failed: {e.code()} - {e.details()}")
            return False
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n[Test 3] Error handling test")
        test_results = []
        
        # Test 1: Get non-existent user
        try:
            request = user_service_pb2.UserRequest(id='nonexistent-id')
            response = self.stub.GetUser(request)
            print("Should have thrown NOT_FOUND error")
            test_results.append(False)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                print(f"✓ Correctly handled NOT_FOUND error: {e.details()}")
                test_results.append(True)
            else:
                print(f"✗ Wrong error code: {e.code()}")
                test_results.append(False)
        
        # Test 2: Create user with empty data
        try:
            request = user_service_pb2.CreateUserRequest(name='', email='')
            response = self.stub.CreateUser(request)
            print("Should have thrown INVALID_ARGUMENT error")
            test_results.append(False)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                print(f"✓ Correctly handled INVALID_ARGUMENT error: {e.details()}")
                test_results.append(True)
            else:
                print(f"✗ Wrong error code: {e.code()}")
                test_results.append(False)
        
        # Test 3: Invalid email format
        try:
            request = user_service_pb2.CreateUserRequest(
                name='Test',
                email='invalid-email'
            )
            response = self.stub.CreateUser(request)
            print("Should have thrown INVALID_ARGUMENT error")
            test_results.append(False)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                print(f"✓ Correctly handled invalid email format: {e.details()}")
                test_results.append(True)
            else:
                print(f"✗ Wrong error code: {e.code()}")
                test_results.append(False)
        
        # Test 4: Duplicate email
        try:
            # First create a user with unique email
            timestamp = str(int(time.time()))
            duplicate_email = f'duplicate{timestamp}@example.com'
            
            request = user_service_pb2.CreateUserRequest(
                name='Test User',
                email=duplicate_email
            )
            response = self.stub.CreateUser(request)
            if response.success:
                # Try to create another user with same email
                request2 = user_service_pb2.CreateUserRequest(
                    name='Another User',
                    email=duplicate_email
                )
                response2 = self.stub.CreateUser(request2)
                print("Should have thrown INVALID_ARGUMENT error for duplicate email")
                test_results.append(False)
            else:
                print("Failed to create initial user for duplicate test")
                test_results.append(False)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                print(f"✓ Correctly handled duplicate email error: {e.details()}")
                test_results.append(True)
            else:
                print(f"✗ Wrong error code: {e.code()}")
                test_results.append(False)
        
        passed = sum(test_results)
        total = len(test_results)
        print(f"\nError handling tests: {passed}/{total} passed")
        
        if passed == total:
            print("Error handling test passed")
            return True
        else:
            print("Some error handling tests failed")
            return False
    
    def cleanup(self):
        """Clean up test data"""
        if self.test_user_id:
            try:
                request = user_service_pb2.UserRequest(id=self.test_user_id)
                self.stub.DeleteUser(request)
                print(f"Cleaned up test user: {self.test_user_id}")
            except Exception as e:
                print(f"Failed to cleanup test user: {e}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*50)
        print("gRPC Test Suite")
        print("="*50)
        
        # Initialize test user ID
        self.test_user_id = None
        
        tests = [
            ('Service Method Invocation', self.test_service_method_invocation),
            ('Data Serialization/Deserialization', self.test_data_serialization_deserialization),
            ('Error Handling', self.test_error_handling),
        ]
        
        passed = 0
        total = len(tests)
        
        for _, test_func in tests:
            if test_func():
                passed += 1
            time.sleep(0.5)
        
        # Clean up test data
        self.cleanup()
        
        print("\n" + "="*50)
        print(f"Test Results: {passed}/{total} passed")
        print("="*50)
        
        return passed == total

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
    print("=== gRPC Client ===")
    print("Choose mode:")
    print("1. Interactive Mode - Manual gRPC testing")
    print("2. Test Mode - Run all gRPC tests")
    print("="*50)
    
    while True:
        try:
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == '1':
                interactive_mode()
                break
            elif choice == '2':
                client = UserServiceClient()
                client.run_all_tests()
                client.close()
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break