import requests
import json
import time
import shlex
from typing import Dict, Any, Optional

class RestApiClient:
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = 30
        self.test_user_id = None
        
    def _make_request(self, method, endpoint, **kwargs) :
        """Execute HTTP request - synchronous waiting for response"""
        url = f"{self.base_url}{endpoint}"
        
        print(f"\n[HTTP Request] {method.upper()} {url}")
        if 'json' in kwargs:
            print(f"[Request Data] {json.dumps(kwargs['json'], ensure_ascii=False, indent=2)}")
        
        start_time = time.time()
        
        try:
            # Synchronous HTTP request - client blocks waiting for response
            response = self.session.request(
                method=method,
                url=url, 
                timeout=self.timeout,
                **kwargs
            )
            
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)
            
            print(f"[Response Status] {response.status_code} ({response_time}ms)")
            
            # Parse JSON response
            if response.headers.get('content-type', '').startswith('application/json'):
                response_data = response.json()
                print(f"[Response Data] {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                return response_data
            else:
                print(f"[Response Content] {response.text}")
                return {'status': 'error', 'message': 'Non-JSON response'}
                
        except requests.exceptions.Timeout:
            print(f"[Error] Request timeout (>{self.timeout}s)")
            return {'status': 'error', 'message': 'Request timeout'}
        except requests.exceptions.ConnectionError:
            print(f"[Error] Cannot connect to server {self.base_url}")
            return {'status': 'error', 'message': 'Connection error'}
        except requests.exceptions.RequestException as e:
            print(f"[Error] Request exception: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_users(self):
        return self._make_request('GET', '/api/users')
    
    def get_user(self, user_id) :
        return self._make_request('GET', f'/api/users/{user_id}')
    
    def create_user(self, name, email):
        data = {
            'name': name,
            'email': email
        }
        return self._make_request('POST', '/api/users', json=data)
    
    def update_user(self, user_id: str, name: str = None, email: str = None) -> Dict[str, Any]:
        data = {}
        if name is not None:
            data['name'] = name
        if email is not None:
            data['email'] = email
        
        return self._make_request('PUT', f'/api/users/{user_id}', json=data)
    
    def delete_user(self, user_id: str) -> Dict[str, Any]:
        return self._make_request('DELETE', f'/api/users/{user_id}')
    
    def search_users(self, query: str) -> Dict[str, Any]:
        return self._make_request('GET', f'/api/users/search?q={query}')
    
    #########################################################
    # below is the test code
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
            print(f"UPDATE test failed: {e}")
            return False
    
    def test_crud_delete(self):
        """Test DELETE operation"""
        print("\n[Test 4] DELETE - Delete user")
        if not self.test_user_id:
            print("Skipping DELETE test (no test user ID)")
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
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*50)
        print("REST API Test Suite")
        print("="*50)
        
        # Initialize test user ID
        self.test_user_id = None
        
        tests = [
            ('CRUD - CREATE', self.test_crud_create),
            ('CRUD - READ', self.test_crud_read),
            ('CRUD - UPDATE', self.test_crud_update),
            ('CRUD - DELETE', self.test_crud_delete),
            ('HTTP Status Codes', self.test_http_status_codes),
            ('Request/Response Format', self.test_request_response_format),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if test_func():
                passed += 1
            time.sleep(0.5)
        
        print("\n" + "="*50)
        print(f"Test Results: {passed}/{total} passed")
        print("="*50)
        
        return passed == total


def interactive_mode():
    client = RestApiClient()
    
    print("REST API Interactive commands:")
    print("1. list      - List all users")
    print("2. get <id>  - Get specific user")
    print("3. create <name> <email> - Create user")
    print("4. update <id> <name> <email> - Update user")
    print("5. delete <id> - Delete user")
    print("6. search <query> - Search users")
    print("7. quit      - Exit")
    print("="*30)
    
    while True:
        try:
            user_input = input("\nEnter command: ").strip()
            
            if not user_input:
                continue
            
            # Parse command with proper quote handling
            command = shlex.split(user_input)
                
            action = command[0].lower()
            
            if action == 'quit':
                break
            elif action == 'list':
                client.get_users()
            elif action == 'get' and len(command) > 1:
                client.get_user(command[1])
            elif action == 'create' and len(command) > 2:
                name = command[1]
                email = command[2]
                client.create_user(name, email)
            elif action == 'update' and len(command) > 3:
                user_id = command[1]
                name = command[2]
                email = command[3]
                client.update_user(user_id, name, email)
            elif action == 'delete' and len(command) > 1:
                client.delete_user(command[1])
            elif action == 'search' and len(command) > 1:
                query = ' '.join(command[1:])
                client.search_users(query)
            else:
                print("Invalid command or insufficient parameters, please try again")
                
        except KeyboardInterrupt:
            print("\n\nUser interrupted operation")
            break
        except Exception as e:
            print(f"Command execution error: {e}")


if __name__ == "__main__":
    print("=== REST API Client ===")
    print("Choose mode:")
    print("1. Interactive Mode - Manual API testing")
    print("2. Test Mode - Run all REST API tests")
    print("="*50)
    
    while True:
        try:
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == '1':
                interactive_mode()
                break
            elif choice == '2':
                client = RestApiClient()
                client.run_all_tests()
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
