from flask import Flask, jsonify, request
from models import User, UserManager
import time

app = Flask(__name__)

user_manager = UserManager()


@app.route('/api/users', methods=['GET'])
def get_users():
    """return all users"""
    try:
        users = user_manager.get_all_users()
        users_data = [user.to_dict() for user in users]
        
        return jsonify({
            'status': 'success',
            'data': users_data,
            'count': len(users_data),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }),200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/api/users/<id>', methods=['GET'])
def get_user(id):
    """return a specific user by ID"""
    try:
        user = user_manager.get_user(id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'User ID {id} does not exist',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }), 404
            
        return jsonify({
            'status': 'success',
            'data': user.to_dict(),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }),200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """create new user from request data"""
    try:
        # Validate request payload
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request body must be JSON',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        data = request.get_json()
        
        required_fields = ['name', 'email']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        # Create user
        user = user_manager.create_user(data['name'], data['email'])
        
        return jsonify({
            'status': 'success',
            'message': 'User created successfully',
            'data': user.to_dict(),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 201
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    """update existing user from request data"""
    try:
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request body must be JSON',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        data = request.get_json()
        
        # Check if user exists
        if not user_manager.get_user(id):
            return jsonify({
                'status': 'error',
                'message': f'User ID {id} does not exist',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }), 404
        
        
        updated_user = user_manager.update_user(id, data.get('name'), data.get('email'))
        
        return jsonify({
            'status': 'success',
            'message': 'User updated successfully',
            'data': updated_user.to_dict(),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }),200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    """delete existing user"""
    try:
        # Check if user exists
        user = user_manager.get_user(id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'User ID {id} does not exist',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }), 404
  
        user_manager.delete_user(id)
        
        return jsonify({
            'status': 'success',
            'message': f'User {user.name} (ID: {id}) deleted successfully',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/api/users/search', methods=['GET'])
def search_users():
    """search users by query"""
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query parameter "q" is required',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }), 400
            
        users = user_manager.search_users(query)
        users_data = [user.to_dict() for user in users]

        return jsonify({
            'status': 'success',
            'data': users_data,
            'count': len(users_data),
            'query': query,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({
        'status': 'error',
        'message': 'The requested resource does not exist',
        'path': request.path,
        'method': request.method,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """405 error handler"""
    return jsonify({
        'status': 'error',
        'message': f'Method {request.method} is not allowed',
        'path': request.path,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }), 500

if __name__ == '__main__':
    print("Starting Flask REST API server...")
    print("API Endpoints:")
    print("GET    /api/users               - Get all users")
    print("GET    /api/users/<id>          - Get a specific user")
    print("POST   /api/users               - Create a new user")
    print("PUT    /api/users/<id>          - Update a user")
    print("DELETE /api/users/<id>          - Delete a user")
    print("GET    /api/users/search?q=xxx  - Search users")
    print("="*50)

    # Seed some sample data
    user_manager.create_user("Lucy", "lucy@example.com")
    user_manager.create_user("David", "david@example.com")
    user_manager.create_user("Kevin", "kevin@example.com")

    app.run(host='0.0.0.0', port=5000, debug=True)