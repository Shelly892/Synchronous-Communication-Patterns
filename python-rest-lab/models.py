import time
import uuid

class User:
    def __init__(self, name, email, user_id = None):
        self.id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.created_at = time.strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }
    
    def update(self, name=None, email=None):
        """Update user information"""
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
    
    def __repr__(self):
        return f"User(id='{self.id}', name='{self.name}', email='{self.email}')"

# User manager - simulate database operations
class UserManager:
    
    def __init__(self):
        self.users = {}
        
    def create_user(self, name, email):
        # Validate inputs   
        if not name or not name.strip():
            raise ValueError("Username cannot be empty")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
        if '@' not in email:
            raise ValueError("Invalid email format")
        
        # Check if email already exists
        for user in self.users.values():
            if user.email == email.strip().lower():
                raise ValueError(f"Email {email} is already used by another user")

        # Create the user
        user = User(name.strip(), email.strip().lower())
        self.users[user.id] = user
        
        print(f"Created user: {user}")
        return user
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_all_users(self):
        """Get all users"""
        return list(self.users.values())
    
    def update_user(self, user_id, name=None, email=None):
        """Update user information"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError(f"User ID {user_id} does not exist")
        
        # Validate update payload
        if name:
            name = name.strip()
            if not name:
                raise ValueError("Username cannot be empty")
        
        if email:
            email = email.strip().lower()
            if not email:
                raise ValueError("Email cannot be empty")
            if '@' not in email:
                raise ValueError("Invalid email format")
            
            # Ensure the email is not used by another user
            for uid, u in self.users.items():
                if uid != user_id and u.email == email:
                    raise ValueError(f"Email {email} is already used by another user")
        
        # Update user information
        old_info = f"{user.name} ({user.email})"
        user.update(name, email)
        new_info = f"{user.name} ({user.email})"
        
        print(f"Updated user {user_id}: {old_info} -> {new_info}")
        return user
    
    def delete_user(self, user_id):
        """Delete user"""
        user = self.users.get(user_id)
        if user_id not in self.users:
            raise ValueError(f"User ID {user_id} does not exist")
        
        user = self.users.pop(user_id)
        print(f"Deleted user: {user}")
        return True
    
    def search_users(self, query):
        """Search users by name or email"""
        query = query.lower().strip()
        if not query:
            return []
        
        results = []
        for user in self.users.values():
            if (query in user.name.lower() or 
                query in user.email.lower()):
                results.append(user)
        
        print(f"Search '{query}' found {len(results)} users")
        return results
    