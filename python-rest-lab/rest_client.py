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
        interactive_mode()
