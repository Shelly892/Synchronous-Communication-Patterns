import grpc
import sys
import time
import os

grpc_path = os.path.join(os.path.dirname(__file__), 'python-grpc-lab', 'generated')
sys.path.insert(0, grpc_path)
import user_service_pb2
import user_service_pb2_grpc

class GrpcTests:
    """gRPC test cases"""
    
    def __init__(self, host='localhost', port='50051'):
        self.address = f'{host}:{port}'
        self.channel = None
        self.stub = None
        self.test_user_id = None
    
    def connect(self):
        """Establish connection"""
        try:
            self.channel = grpc.insecure_channel(self.address)
            self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
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
    
    def close(self):
        """Close connection"""
        if self.channel:
            self.channel.close()
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*60)
        print("gRPC Test Suite")
        print("="*60)
        
        if not self.connect():
            print("Cannot connect to gRPC server")
            return False
        
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
        self.close()
        
        print("\n" + "="*60)
        print(f"Test Results: {passed}/{total} passed")
        print("="*60)
        
        return passed == total

if __name__ == '__main__':
    tester = GrpcTests()
    tester.run_all_tests()