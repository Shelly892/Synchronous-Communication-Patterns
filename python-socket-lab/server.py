import socket
import threading
import time

class SocketServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        
    def start(self):
        """start the server"""
        try:
            # create TCP/IP Socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Enable address reuse to prevent "Address already in use" errors
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
            # bind to localhost:8080
            self.server_socket.bind((self.host, self.port))
            
            # listen for connections
            self.server_socket.listen(5)
            self.running = True
            
            print(f"Server started successfully. Listening on {self.host}:{self.port}")
            print("waiting for client connection...")
            
            while self.running:
                try:
                    # accept client connection
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Built connection for new client: {client_address}")
                    
                    # create new thread for every client 
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"socket error: {e}")
                    break
                    
        except Exception as e:
            print(f"Failed to start the server: {e}")
        finally:
            self.stop()
            
    def handle_client(self, client_socket, client_address):
        """deal request from client"""
        try:
            while True:
                # receive data from the client
                data = client_socket.recv(1024)
                
                if not data:
                    print(f"Client {client_address} disconnected")
                    break
                
                # decode the received data
                message = data.decode('utf-8')
                print(f"Received message from {client_address}:{message}")
                
                # process the request 
                response = self.process_message(message, client_address)
                
                # send the response
                client_socket.send(response.encode('utf-8'))
                
                
        except ConnectionResetError:
            print(f"Client {client_address} forcibly closed the connection")
        except Exception as e:
            print(f"Error while handling client {client_address}: {e}")
        finally:
            client_socket.close()
            print(f"Closed connection with {client_address}v")
    
    def process_message(self, message, client_address):
        """business logic for processing messages - only uppercase conversion"""
        try:
            # Convert any input to uppercase and return directly
            result = message.upper()
            return result
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def stop(self):
        """stop server"""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
                print("Server stopped")
            except:
                pass

if __name__ == "__main__":
    server = SocketServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n Closing the server...")
        server.stop()