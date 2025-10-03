import socket
import time

class SocketTests:
    """Socket implementation test cases"""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
    
    def test_connection_establishment(self):
        """Test connection establishment"""
        print("\n[Test 1] Connection establishment test")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            print("Connection established successfully")
            sock.close()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def test_message_sending_receiving(self):
        """Test message sending/receiving"""
        print("\n[Test 2] Message sending/receiving test")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            
            # Test simple text - server converts to uppercase
            message = "Hello Socket Server"
            sock.send(message.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            
            print(f"Sent: {message}")
            print(f"Received: {response}")
            
            # Verify response content (direct uppercase text)
            if response == message.upper():
                print("Message sending/receiving successful")
                sock.close()
                return True
            else:
                print("Response content error")
                print(f"Expected result: {message.upper()}")
                print(f"Actual result: {response}")
                sock.close()
                return False
                
        except Exception as e:
            print(f"Message sending/receiving failed: {e}")
            return False
    
    def test_uppercase_conversion(self):
        """Test uppercase conversion for various inputs"""
        print("\n[Test 3] Uppercase conversion test")
        try:
            # Test various input types
            test_cases = [
                'test message',
                'hello world',
                '12345',
                'mixed CASE text',
                'PyThOn SoCkEt'
            ]
            
            all_passed = True
            for i, test_input in enumerate(test_cases):
                print(f"\n  Sub-test {i+1}: '{test_input}'")
                
                # Create new connection for each test
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                
                sock.send(test_input.encode('utf-8'))
                response = sock.recv(1024).decode('utf-8')
                sock.close()
                
                print(f"Sent: {test_input}")
                print(f"Received: {response}")
                
                expected_result = test_input.upper()
                if response == expected_result:
                    print(f"Uppercase conversion test passed")
                else:
                    print(f"Uppercase conversion test failed")
                    print(f"Expected: {expected_result}")
                    print(f"Actual: {response}")
                    all_passed = False
            
            if all_passed:
                print("All uppercase conversion tests passed")
                return True
            else:
                print("Some uppercase conversion tests failed")
                return False
                
        except Exception as e:
            print(f"Uppercase conversion test failed: {e}")
            return False
    
    def test_error_handling_invalid_connection(self):
        """Test error handling: invalid connection"""
        print("\n[Test 4] Error handling test - invalid connection")
        
        # Test 1: Connect to wrong port
        print("Sub-test 1: Wrong port connection")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # Set 2 second timeout
            sock.connect((self.host, 9999))  # Wrong port
            print("Should have failed to connect but succeeded")
            sock.close()
            return False
        except socket.timeout:
            print("Correctly handled connection timeout")
        except ConnectionRefusedError:
            print("Correctly handled connection refused")
        except Exception as e:
            print(f"Correctly caught exception: {type(e).__name__}")
        
        # Test 2: Connect to wrong host
        print("  Sub-test 2: Wrong host connection")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect(('192.168.1.999', self.port))  # Invalid IP
            print("Should have failed to connect but succeeded")
            sock.close()
            return False
        except socket.timeout:
            print("Correctly handled connection timeout")
        except ConnectionRefusedError:
            print("Correctly handled connection refused")
        except OSError as e:
            print(f"Correctly handled OSError: {e}")
        except Exception as e:
            print(f"Correctly caught exception: {type(e).__name__}")
        
        return True
    
    def test_multiple_requests(self):
        """Test multiple requests"""
        print("\n[Test 5] Multiple requests test")
        try:
            success_count = 0
            total_requests = 5
            
            for i in range(total_requests):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                
                # Simple text requests - all converted to uppercase
                message = f"Request {i+1}"
                sock.send(message.encode('utf-8'))
                response = sock.recv(1024).decode('utf-8')
                
                expected_result = message.upper()
                if response == expected_result:
                    success_count += 1
                    print(f"  Request {i+1}: pass")
                else:
                    print(f"  Request {i+1}: fail")
                    print(f"    Expected: {expected_result}")
                    print(f"    Actual: {response}")
                
                sock.close()
                time.sleep(0.1)  # Small delay between requests
            
            print(f"\nSuccessful requests: {success_count}/{total_requests}")
            if success_count == total_requests:
                print("Multiple requests test passed")
                return True
            else:
                print("Some requests failed")
                return False
                
        except Exception as e:
            print(f"Multiple requests test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*60)
        print("Socket Implementation Test Suite")
        print("="*60)
        
        tests = [
            self.test_connection_establishment,
            self.test_message_sending_receiving,
            self.test_uppercase_conversion,
            self.test_error_handling_invalid_connection,
            self.test_multiple_requests
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(0.5)
        
        print("\n" + "="*60)
        print(f"Test Results: {passed}/{total} passed")
        print("="*60)
        
        return passed == total

if __name__ == '__main__':
    tester = SocketTests()
    tester.run_all_tests()