import requests
import time

class RestApiTests:
    """REST API test cases"""
    
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.test_user_id = None
    
    def test_crud_create(self):
        """Test CREATE operation"""
        print("\n[Test 1] CREATE - Create user")
        try:
            data = {
                'name': 'Test User',
                'email': 'testuser@example.com'
            }
            
            response = requests.post(f'{self.base_url}/api/users', json=data)
            
            print(f"Request: POST /api/users")
            print(f"Data: {data}")
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                self.test_user_id = result['data']['id']
                print(f"Response: {result}")
                print(f"CREATE test passed (User ID: {self.test_user_id})")
                return True
            else:
                print(f"CREATE failed, expected 201, got {response.status_code}")
                return False
                
        except Exception as e:
            print(f"CREATE test failed: {e}")
            return False
    
    def test_crud_read(self):
        """Test READ operation"""
        print("\n[Test 2] READ - Read users")
        try:
            # Test get all users
            response = requests.get(f'{self.base_url}/api/users')
            print(f"Request: GET /api/users")
            print(f"Status code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"READ failed, expected 200, got {response.status_code}")
                return False
            
            result = response.json()
            print(f"Retrieved {result['count']} users")
            
            # Test get specific user
            if self.test_user_id:
                response = requests.get(f'{self.base_url}/api/users/{self.test_user_id}')
                print(f"\nRequest: GET /api/users/{self.test_user_id}")
                print(f"Status code: {response.status_code}")
                
                if response.status_code == 200:
                    user_data = response.json()['data']
                    print(f"User info: {user_data['name']} ({user_data['email']})")
                    print("READ test passed")
                    return True
                else:
                    print(f"READ specific user failed")
                    return False
            else:
                print("READ test passed")
                return True
                
        except Exception as e:
            print(f"READ test failed: {e}")
            return False
    
    def test_crud_update(self):
        """Test UPDATE operation"""
        print("\n[Test 3] UPDATE - Update user")
        if not self.test_user_id:
            print("Skipping UPDATE test (no test user ID)")
            return True
        
        try:
            data = {
                'name': 'Updated User',
                'email': 'updated@example.com'
            }
            
            response = requests.put(
                f'{self.base_url}/api/users/{self.test_user_id}',
                json=data
            )
            
            print(f"Request: PUT /api/users/{self.test_user_id}")
            print(f"Data: {data}")
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result}")
                print("UPDATE test passed")
                return True
            else:
                print(f"UPDATE failed, expected 200, got {response.status_code}")
                return False
                
        except Exception as e:
            print(f" UPDATE test failed: {e}")
            return False
    
    def test_crud_delete(self):
        """Test DELETE operation"""
        print("\n[Test 4] DELETE - Delete user")
        if not self.test_user_id:
            print(" Skipping DELETE test (no test user ID)")
            return True
        
        try:
            response = requests.delete(f'{self.base_url}/api/users/{self.test_user_id}')
            
            print(f"Request: DELETE /api/users/{self.test_user_id}")
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result}")
                print("DELETE test passed")
                return True
            else:
                print(f"DELETE failed, expected 200, got {response.status_code}")
                return False
                
        except Exception as e:
            print(f"DELETE test failed: {e}")
            return False
    
    def test_http_status_codes(self):
        """Test HTTP status code validation"""
        print("\n[Test 5] HTTP status code validation")
        test_cases = []
        
        try:
            # Test 404 - Non-existent resource
            response = requests.get(f'{self.base_url}/api/users/nonexistent-id')
            print(f"GET non-existent user: {response.status_code}")
            test_cases.append(('404 test', response.status_code == 404))
            
            # Test 400 - Missing required fields
            response = requests.post(f'{self.base_url}/api/users', json={})
            print(f"POST empty data: {response.status_code}")
            test_cases.append(('400 test (missing fields)', response.status_code == 400))
            
            # Test 400 - Invalid email format
            response = requests.post(f'{self.base_url}/api/users', json={'name': 'Test', 'email': 'invalid-email'})
            print(f"POST invalid email: {response.status_code}")
            test_cases.append(('400 test (invalid email)', response.status_code == 400))
            
            # Test 400 - Search without query parameter
            response = requests.get(f'{self.base_url}/api/users/search')
            print(f"GET search without query: {response.status_code}")
            test_cases.append(('400 test (missing query)', response.status_code == 400))
            
            # Test 200 - Successful request
            response = requests.get(f'{self.base_url}/api/users')
            print(f"GET all users: {response.status_code}")
            test_cases.append(('200 test', response.status_code == 200))
            
            passed = sum(1 for _, result in test_cases if result)
            print(f"\nStatus code tests: {passed}/{len(test_cases)} passed")
            
            if passed == len(test_cases):
                print("HTTP status code validation passed")
                return True
            else:
                print("Some status code tests failed")
                return False
                
        except Exception as e:
            print(f"Status code test failed: {e}")
            return False
    
    def test_request_response_format(self):
        """Test request/response format validation"""
        print("\n[Test 6] Request/response format validation")
        try:
            # Test JSON request
            data = {'name': 'Format Test', 'email': 'format@test.com'}
            response = requests.post(f'{self.base_url}/api/users', json=data)
            
            # Verify response is JSON format
            content_type = response.headers.get('Content-Type', '')
            print(f"Response Content-Type: {content_type}")
            
            if 'application/json' not in content_type:
                print("Response is not JSON format")
                return False
            
            # Verify response structure for successful creation
            result = response.json()
            required_fields = ['status', 'message', 'data', 'timestamp']
            
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                print(f"Missing fields: {missing_fields}")
                return False
            
            # Verify data structure
            if 'data' in result:
                user_data = result['data']
                user_required_fields = ['id', 'name', 'email', 'created_at']
                missing_user_fields = [field for field in user_required_fields if field not in user_data]
                if missing_user_fields:
                    print(f"Missing user data fields: {missing_user_fields}")
                    return False
            
            print(f"Response structure: {list(result.keys())}")
            print(f"User data structure: {list(result['data'].keys()) if 'data' in result else 'N/A'}")
            print("Request/response format validation passed")
            
            # Clean up test data
            if 'data' in result and 'id' in result['data']:
                requests.delete(f'{self.base_url}/api/users/{result["data"]["id"]}')
            
            return True
            
        except Exception as e:
            print(f"Format validation failed: {e}")
            return False
    

    def test_data_validation(self):
        """Test data validation"""
        print("\n[Test 7] Data validation test")
        test_cases = []
        
        try:
            # Test 1: Empty name
            response = requests.post(f'{self.base_url}/api/users', json={'name': '', 'email': 'test@example.com'})
            test_cases.append(('Empty name', response.status_code == 400))
            print(f"Empty name: {response.status_code}")
            
            # Test 2: Empty email
            response = requests.post(f'{self.base_url}/api/users', json={'name': 'Test', 'email': ''})
            test_cases.append(('Empty email', response.status_code == 400))
            print(f"Empty email: {response.status_code}")
            
            # Test 3: Invalid email format
            response = requests.post(f'{self.base_url}/api/users', json={'name': 'Test', 'email': 'not-an-email'})
            test_cases.append(('Invalid email format', response.status_code == 400))
            print(f"Invalid email format: {response.status_code}")
            
            # Test 4: Duplicate email
            # First create a user
            response = requests.post(f'{self.base_url}/api/users', json={'name': 'Test User', 'email': 'duplicate@example.com'})
            if response.status_code == 201:
                # Try to create another user with same email
                response = requests.post(f'{self.base_url}/api/users', json={'name': 'Another User', 'email': 'duplicate@example.com'})
                test_cases.append(('Duplicate email', response.status_code == 400))
                print(f"Duplicate email: {response.status_code}")
                
                # Clean up
                user_id = response.json().get('data', {}).get('id') if response.status_code == 201 else None
                if not user_id:
                    # Get the first user's ID from the successful creation
                    first_response = requests.post(f'{self.base_url}/api/users', json={'name': 'Test User', 'email': 'duplicate@example.com'})
                    if first_response.status_code == 201:
                        user_id = first_response.json()['data']['id']
                if user_id:
                    requests.delete(f'{self.base_url}/api/users/{user_id}')
            else:
                test_cases.append(('Duplicate email', False))
                print("Failed to create initial user for duplicate test")
            
            passed = sum(1 for _, result in test_cases if result)
            print(f"\nData validation tests: {passed}/{len(test_cases)} passed")
            
            if passed == len(test_cases):
                print("Data validation test passed")
                return True
            else:
                print("Some data validation tests failed")
                return False
                
        except Exception as e:
            print(f" Data validation test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*60)
        print("REST API Test Suite")
        print("="*60)
        
        tests = [
            ('CRUD - CREATE', self.test_crud_create),
            ('CRUD - READ', self.test_crud_read),
            ('CRUD - UPDATE', self.test_crud_update),
            ('CRUD - DELETE', self.test_crud_delete),
            ('HTTP Status Codes', self.test_http_status_codes),
            ('Request/Response Format', self.test_request_response_format),
            ('Data Validation', self.test_data_validation),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if test_func():
                passed += 1
            time.sleep(0.5)
        
        print("\n" + "="*60)
        print(f"Test Results: {passed}/{total} passed")
        print("="*60)
        
        return passed == total

if __name__ == '__main__':
    tester = RestApiTests()
    tester.run_all_tests()