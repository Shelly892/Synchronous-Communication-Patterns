import socket
import time

class SocketClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self):
        """Connect to the server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Successfully connected to server {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
    
    def send_message(self, message):
        """Send a message and wait for the response"""
        try:
            if not self.socket:
                print("Not connected to the server")
                return None
                
            # send the message
            self.socket.sendall(message.encode('utf-8'))
            print(f"Sent message: {message}")
            
            # wait for and receive the response
            response = self.socket.recv(1024)
            response_text = response.decode('utf-8')
            print(f"Received response: {response_text}")
            
            return response_text
            
        except Exception as e:
            print(f"Failed to send message: {e}")
            return None
    
    
    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            print("The connection to the server has been closed.")
    
    def interactive_mode(self):
        if not self.connect():
            return
            
        print("\n=== Socket Client: Interactive Mode ===")
        print("Type any text — the server will convert it to UPPERCASE")
        print("Type 'quit' to exit")
        print("="*40)
        
        try:
            while True:
                user_input = input("\nEnter message: ").strip()
                
                if user_input.lower() == 'quit':
                    break
                
                if not user_input:
                    continue
                
                # send plain text - server will convert to uppercase
                response = self.send_message(user_input)
                if response:
                    print(f"Result: {response}")
                            
        except KeyboardInterrupt:
            print("\n\nUser cancelled")
        finally:
            self.disconnect()


if __name__ == "__main__":
        client = SocketClient()
        client.interactive_mode()