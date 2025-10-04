# Synchronous Communication Patterns

1. [Project Overview](#project-overview)
2. [Implementation Approaches](#implementation-approaches)
3. [Running Instructions](#running-instructions)
4. [Test Results](#test-results)
5. [Performance Comparison](#performance-comparison)
6. [Conclusion](#conclusion)
7. [References](#references)

---

## Project Overview

This project implements three different synchronous communication patterns for client-server communication in distributed systems:

- **Socket Communication**: Low-level network programming based on TCP
- **REST API**: RESTful Web services based on HTTP
- **gRPC**: High-performance RPC based on HTTP/2 and Protocol Buffers

All implementations are written in Python and include comprehensive test suites and performance comparison analysis.

### Project Structure

```
distributed-systems-lab/
├── python-socket-lab/          # Socket implementation
│   ├── server.py               # Socket server
│   ├── client.py               # Socket client(including tests)
│   └── Dockerfile
├── python-rest-lab/            # REST API implementation
│   ├── app.py                  # Flask application
│   ├── models.py               # Data models
│   ├── client.py               # REST client(including tests)
│   ├── requirements.txt
│   └── Dockerfile
├── python-grpc-lab/            # gRPC implementation
│   ├── proto/
│   │   └── user_service.proto  # Interface definition
│   ├── generated/              # Auto-generated code
│   ├── server.py               # gRPC server
│   ├── client.py               # gRPC client(including tests)
│   ├── requirements.txt
│   └── Dockerfile
├── benchmark.py                # Performance comparison
├── Dockerfile.benchmark        # dockerfile
├── docker-compose.yml          # Docker orchestration
└── README.md                   # This document
```

---

## Implementation Approaches

This project uses classic client-server architecture, with all three implementations following the same pattern:

```
Client                          Server
  |                               |
  |-----> 1. Send Request ----->  |
  |                               | 2. Process Request
  | (Blocking Wait)               |
  |<----- 3. Return Response <--- |
  |                               |
  | 4. Continue Execution         |
```

### 1. Socket Implementation

**Tech Stack**: Python socket library + TCP protocol

**Features:**

- Raw TCP Socket communication
- Custom JSON message format
- Multi-threaded concurrent connection handling

**Core Code Example:**

```python
# Server side
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

client_socket, address = server_socket.accept()  # Blocking wait
data = client_socket.recv(1024)  # Synchronous receive
response = process_message(data)
client_socket.send(response)  # Synchronous send

# Client side
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))  # Synchronous connection
sock.send(message)  # Send request
response = sock.recv(1024)  # Blocking wait for response
```

**Synchronous Characteristics:**

- `accept()` - Blocks waiting for client connection
- `recv()` - Blocks waiting for data reception
- `send()` - Synchronous data transmission

### 2. REST API Implementation

**Tech Stack**: Flask + HTTP/1.1 + JSON

**Features:**

- Standard HTTP protocol
- RESTful URL design
- JSON data exchange format

**API Interface Design:**

| Method | Path                   | Description       |
| ------ | ---------------------- | ----------------- |
| GET    | /api/users             | Get all users     |
| GET    | /api/users/{id}        | Get specific user |
| POST   | /api/users             | Create new user   |
| PUT    | /api/users/{id}        | Update user       |
| DELETE | /api/users/{id}        | Delete user       |
| GET    | /api/users/search?q=xx | Search users      |

**Core Code Example:**

```python
# Server side
@app.route('/api/users', methods=['GET'])
def get_users():
    users = user_manager.get_all_users()
    return jsonify({'status': 'success', 'data': users})

# Client side
response = requests.get('http://localhost:5000/api/users')  # Synchronous request
data = response.json()  # Parse response
```

**Synchronous Characteristics:**

- HTTP request-response is naturally synchronous
- `requests.get()` blocks waiting for server response
- Server returns result only after processing completes

### 3. gRPC Implementation

**Tech Stack**: gRPC + HTTP/2 + Protocol Buffers

**Features:**

- Interface definition using Protocol Buffers
- Binary serialization for excellent performance
- Strong type checking with compile-time validation
- Auto-generated client and server code

**Interface Definition (user_service.proto):**

```protobuf
service UserService {
    rpc GetAllUsers (Empty) returns (UserList);
    rpc GetUser (UserRequest) returns (UserResponse);
    rpc CreateUser (CreateUserRequest) returns (UserResponse);
    rpc UpdateUser (UpdateUserRequest) returns (UserResponse);
    rpc DeleteUser (UserRequest) returns (DeleteResponse);
}
```

**Core Code Example:**

```python
# Server side
class UserServiceImpl(user_service_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = user_service_pb2.User(id,name,email,created_at)
        return user_service_pb2.UserResponse(success=True, user=user)

# Client side
channel = grpc.insecure_channel('localhost:50051')
stub = user_service_pb2_grpc.UserServiceStub(channel)
response = stub.GetUser(id)  # Synchronous call
```

**Synchronous Characteristics:**

- gRPC uses synchronous calls by default
- `stub.GetUser()` blocks waiting for response
- Client continues only after server method returns result

---

## Running Instructions

### Requirements

- Python 3.9+
- pip (Python package manager)
- Docker (optional)

### Install Dependencies

```bash
# REST implementation
cd python-rest-lab
pip install -r requirements.txt

# gRPC implementation
cd python-grpc-lab
pip install -r requirements.txt
```

### Start Services

**Method 1: Using Docker Compose(Recommended)**
Start all three services (Socket, REST, gRPC) in the background with a single command.

```bash
docker-compose up --build -d
```

**Method 2: Manual Start**
Manually start each service in a separate terminal

```bash
# Terminal 1 - Socket server
cd python-socket-lab
python server.py

# Terminal 2 - REST API server
cd python-rest-lab
python app.py

# Terminal 3 - gRPC server
cd python-grpc-lab
python server.py
```

### Run Client Tests

**Method 1: Using Docker(Recommended)**
Run the client side as a container to interact with its corresponding server.
(**The testing and validation part is included as an option in the program**)

```bash
# Socket client
docker run -it --rm -e APP=client --network="host" socket-lab:latest
# REST client
docker run -it --rm -e RUN_MODE=client --network="host" rest-api-lab:latest
# gRPC client
docker run -it --rm -e RUN_MODE=client --network="host" grpc-lab:latest
```

**Method 2: Manual Start**
Run the client scripts directly on the host machine, connecting to the servers already running.

```bash
# Socket client
python python-socket-lab/client.py
# REST client
python python-rest-lab/client.py
# gRPC client
python python-grpc-lab/client.py
```

### Run Performance Benchmark

**Method 1: Docker Container (Recommended)**
Run benchmark in a dedicated container that connects to running services

```bash
# Start all services first
# skip this step if the services already running in background
docker-compose up -d

# Build and start the benchmark container
docker-compose --profile benchmark up -d benchmark

# Run benchmark inside the container
docker exec -it lab-benchmark python benchmark.py

# Clean up benchmark container when done
docker-compose down benchmark
```

**Method 2: Local Execution**
Run benchmark script directly on your host machine

```bash
# Ensure all services are running first
docker-compose up -d

# Run benchmark locally
python benchmark.py
```

---

## Test Results

### Testing Methodology

Comprehensive test cases were written for each implementation to verify:

1. **Functional Correctness**: Whether CRUD operations work properly
2. **Error Handling**: Whether exceptions are handled correctly
3. **Data Integrity**: Whether data transmission is accurate
4. **Protocol Compliance**: Whether implementation follows protocol standards

### Socket Test Results

```
==================================================
Socket Implementation Test Suite
==================================================

[Test 1] Connection establishment test
Connection successfully established

[Test 2] Message send/receiving test
Sent: Hello Socket Server
Received: HELLO SOCKET SERVER
Message sending/receiving successful

[Test 3] Uppercase conversion test
  Sub-test 1: 'test message'
Sent: test message
Received: TEST MESSAGE
Uppercase conversion test passed

  Sub-test 2: 'hello world'
Sent: hello world
Received: HELLO WORLD
Uppercase conversion test passed

  Sub-test 3: '12345'
Sent: 12345
Received: 12345
Uppercase conversion test passed

  Sub-test 4: 'mixed CASE text'
Sent: mixed CASE text
Received: MIXED CASE TEXT
Uppercase conversion test passed

  Sub-test 5: 'PyThOn SoCkEt'
Sent: PyThOn SoCkEt
Received: PYTHON SOCKET
Uppercase conversion test passed

All uppercase conversion tests passed

[Test 4] Error Handling Test - Invalid Connection
  Sub-test 1: Wrong port connection
Correctly handled connection timeout
  Sub-test 2: Wrong host connection
Correctly handled OSError: [Errno 11001] getaddrinfo failed

[Test 5] Multiple Requests Test
Successful requests: 5/5
Multiple requests test passed

==================================================
Test Results: 5/5 Passed
==================================================
```

**Conclusion**: Socket implementation is functionally complete with all tests passing.

### REST API Test Results

```
==================================================
REST API Test Suite
==================================================

[Test 1] CREATE - Create User
Request: POST /api/users
Status Code: 201
CREATE test passed

[Test 2] READ - Read Users
Request: GET /api/users
Retrieved 4 users
READ test passed

Request: GET /api/users/b28ef30c-4627-4d27-90fa-6eff99fefcaf
Status code: 200
User info: Test User (testuser@example.com)
READ test passed

[Test 3] UPDATE - Update User
Status Code: 200
UPDATE test passed

[Test 4] DELETE - Delete User
Request: DELETE /api/users/b28ef30c-4627-4d27-90fa-6eff99fefcaf
Status Code: 200
DELETE test passed

[Test 5] HTTP Status Code Validation
GET non-existent user: 404
POST empty data: 400
POST invalid email: 400
GET search without query: 400
GET all users: 200

Status code tests: 5/5 passed
HTTP status code validation passed

[Test 6] Request/Response Format Validation
Response Content-Type: application/json
Request/response format validation passed

==================================================
Test Results: 6/6 Passed
==================================================
```

**Conclusion**: REST API implementation follows RESTful conventions with all CRUD operations working properly.

### gRPC Test Results

```
==================================================
gRPC Test Suite
==================================================

[Test 1] Service Method Invocation Test
Call: GetAllUsers()
Returned user count: 2
Success status: True
Service method invocation successful

[Test 2] Data Serialization/Deserialization Test
Sent data:
  name: Serialization Test User
  email: serialization1759526723@test.com

Received data:
  id: 5
  name: Serialization Test User
  email: serialization1759526723@test.com
  created_at: 2025-10-03 21:25:23
Data serialization/deserialization correct

[Test 3] Error Handling Test
✓ Correctly handled NOT_FOUND error: User with ID nonexistent-id not found
✓ Correctly handled INVALID_ARGUMENT error: Name and email are required
✓ Correctly handled invalid email format: Invalid email format
✓ Correctly handled duplicate email error: Email already exists

Error handling tests: 4/4 passed
Error handling test passed
Cleaned up test user: 5
==================================================
Test Results: 3/3 Passed
==================================================
```

**Conclusion**: gRPC implementation is complete with correct Protocol Buffers serialization and comprehensive error handling.

---

## Performance Comparison

### Test Environment

- **Hardware**: Local development environment
- **Operating System**: Windows
- **Test Method**: Each method runs 50 identical operations, measuring response time

### Performance Test Results

```
==================================================
Socket Performance Test (50 iterations)
==================================================
Completed: 10/50
Completed: 20/50
Completed: 30/50
Completed: 40/50
Completed: 50/50

Socket Results:
  Average response time: 2.10ms
  Min: 1.00ms
  Max: 10.07ms
  Standard deviation: 1.22ms
  Errors: 0

==================================================
REST API Performance Test (50 iterations)
==================================================
Completed: 10/50
Completed: 20/50
Completed: 30/50
Completed: 40/50
Completed: 50/50

REST Results:
  Average response time: 4.65ms
  Min: 3.00ms
  Max: 11.01ms
  Standard deviation: 1.18ms
  Errors: 0

==================================================
gRPC Performance Test (50 iterations)
==================================================
Completed: 10/50
Completed: 20/50
Completed: 30/50
Completed: 40/50
Completed: 50/50

gRPC Results:
  Average response time: 1.27ms
  Min: 0.00ms
  Max: 10.85ms
  Standard deviation: 1.46ms
  Errors: 0

==================================================
Performance Comparison Summary
==================================================

Ranking (by average response time):
----------------------------------------
1. gRPC           1.27ms (fastest)
2. Socket         2.10ms (65% slower)
3. REST           4.65ms (265% slower)
```

### Performance Analysis

#### Socket - Fastest

**Performance Characteristics**

- Direct TCP connection without additional protocol overhead.
- Minimal data encapsulation, resulting in the lowest latency.
- No intermediate layers such as HTTP headers or serialization frameworks.

**Use Cases:**

- Latency-sensitive applications (e.g., real-time trading, live streaming).
- Custom communication protocols where developers want full control.
- High-performance game servers and real-time multiplayer environments.

#### gRPC - Balanced

**Performance Characteristics**

- HTTP/2 multiplexing: multiple requests share the same connection.
- Protocol Buffers binary serialization
- Connection reuse (no need to establish connection each time)
- Header compression reduces network overhead

**Use Cases:**

- Internal microservice communication in cloud-native systems.
- Systems with high throughput and structured data, e.g., large-scale distributed platforms.
- Cross-language service invocation, ensuring strong type safety.

#### REST - Slowest but Most Universal

**Performance Characteristic**

- Typically runs on HTTP/1.1, incurring more overhead.
- Human-readable format (JSON/XML), larger message size.
- Often creates new TCP connections per request (unless HTTP keep-alive is used).

**Use Cases:**

- Public Web APIs where accessibility and readability are critical.
- Browser-based clients (native support for HTTP/JSON).
- Third-party system integration, since REST is widely adopted and supported by virtually all platforms.

---

## Conclusion

This project successfully implemented three different levels of synchronous communication patterns:

- Socket offers the highest performance, but requires custom protocol design and is less interoperable.
- gRPC provides a balance between performance and usability, suitable for modern distributed microservices.
- REST is the slowest, but wins in universality and compatibility, making it the de facto standard for public APIs.

All implementations correctly embody the core characteristics of synchronous communication:

- Client blocks waiting after sending request
- Server returns response after processing completes
- Client continues execution after receiving response

### Technology Selection Recommendations

Based on performance testing and actual application scenarios:

| Scenario                            | Recommended Solution | Reason                              |
| ----------------------------------- | -------------------- | ----------------------------------- |
| Internal microservice communication | gRPC                 | High performance + Type safety      |
| Public Web API                      | REST                 | Standardization + Easy integration  |
| Real-time gaming/trading systems    | Socket               | Lowest latency                      |
| Mobile app backend                  | REST or gRPC         | Depends on performance requirements |
| IoT device communication            | Socket or gRPC       | Resource-constrained environments   |

---

## References

#### Official Documentation

- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Flask RESTful API](https://flask.palletsprojects.com/)
- [gRPC Python](https://grpc.io/docs/languages/python/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)

#### Technical Articles

- [REST API Design Best Practices](https://restfulapi.net/)
- [gRPC vs REST Performance Comparison](https://grpc.io/blog/grpc-web-ga/)
- [HTTP/2 Protocol Features](https://http2.github.io/)

#### Related Course Materials

- COMP 41720 Distributed Systems Course Notes
- Lab 1: Synchronous Communication Patterns
