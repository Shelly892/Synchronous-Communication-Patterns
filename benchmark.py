# benchmark.py - Performance comparison of three communication methods
import time
import socket
import requests
import grpc
import sys
import json
import statistics

# Import gRPC generated code
try:
    # Try container path first
    sys.path.append('./generated')
    import user_service_pb2
    import user_service_pb2_grpc
except ImportError:
    # Fallback to local development path
    sys.path.append('./python-grpc-lab/generated')
    import user_service_pb2
    import user_service_pb2_grpc

def benchmark_socket(iterations=50):
    """Benchmark Socket performance"""
    print(f"\n{'='*50}")
    print(f"Socket Performance Test ({iterations} iterations)")
    print('='*50)
    
    times = []
    errors = 0
    
    for i in range(iterations):
        try:
            start = time.time()
            
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 8080))
            
            # Send simple text message (server converts to uppercase)
            message = 'performance test'
            sock.send(message.encode('utf-8'))
            
            # Receive response
            response = sock.recv(1024)
            
            # Close connection
            sock.close()
            
            end = time.time()
            elapsed = (end - start) * 1000  # Convert to milliseconds
            times.append(elapsed)
            
            if (i + 1) % 10 == 0:
                print(f"Completed: {i + 1}/{iterations}")
                
        except Exception as e:
            errors += 1
            print(f"Error #{errors}: {e}")
    
    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        
        print(f"\nSocket Results:")
        print(f"  Average response time: {avg_time:.2f}ms")
        print(f"  Min: {min_time:.2f}ms")
        print(f"  Max: {max_time:.2f}ms")
        print(f"  Standard deviation: {std_dev:.2f}ms")
        print(f"  Errors: {errors}")
        
        return avg_time
    
    return None

def benchmark_rest(iterations=50):
    """Benchmark REST API performance"""
    print(f"\n{'='*50}")
    print(f"REST API Performance Test ({iterations} iterations)")
    print('='*50)
    
    times = []
    errors = 0
    
    for i in range(iterations):
        try:
            start = time.time()
            
            # Make multiple REST API calls
            response = requests.get('http://localhost:5000/api/users')
            data = response.json()
            
            end = time.time()
            elapsed = (end - start) * 1000  # Convert to milliseconds
            times.append(elapsed)
            
            if (i + 1) % 10 == 0:
                print(f"Completed: {i + 1}/{iterations}")
                
        except Exception as e:
            errors += 1
            print(f"Error #{errors}: {e}")
    
    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        
        print(f"\nREST Results:")
        print(f"  Average response time: {avg_time:.2f}ms")
        print(f"  Min: {min_time:.2f}ms")
        print(f"  Max: {max_time:.2f}ms")
        print(f"  Standard deviation: {std_dev:.2f}ms")
        print(f"  Errors: {errors}")
        
        return avg_time
    
    return None

def benchmark_grpc(iterations=50):
    """Benchmark gRPC performance"""
    print(f"\n{'='*50}")
    print(f"gRPC Performance Test ({iterations} iterations)")
    print('='*50)
    
    times = []
    errors = 0
    
    try:
        # Create gRPC channel (reuse connection)
        channel = grpc.insecure_channel('localhost:50051')  
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        
        for i in range(iterations):
            try:
                start = time.time()
                
                # Make multiple gRPC calls
                response = stub.GetAllUsers(user_service_pb2.Empty())
                
                end = time.time()
                elapsed = (end - start) * 1000  # Convert to milliseconds
                times.append(elapsed)
                
                if (i + 1) % 10 == 0:
                    print(f"Completed: {i + 1}/{iterations}")
                    
            except grpc.RpcError as e:
                errors += 1
                print(f"RPC Error #{errors}: {e.code()}")
        
        channel.close()
        
    except Exception as e:
        print(f"Connection error: {e}")
        return None
    
    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        
        print(f"\ngRPC Results:")
        print(f"  Average response time: {avg_time:.2f}ms")
        print(f"  Min: {min_time:.2f}ms")
        print(f"  Max: {max_time:.2f}ms")
        print(f"  Standard deviation: {std_dev:.2f}ms")
        print(f"  Errors: {errors}")
        
        return avg_time
    
    return None

def compare_results(socket_time, rest_time, grpc_time):
    """Compare results from all three methods"""
    print(f"\n{'='*50}")
    print("Performance Comparison Summary")
    print('='*50)
    
    results = []
    if socket_time is not None:
        results.append(('Socket', socket_time))
    if rest_time is not None:
        results.append(('REST', rest_time))
    if grpc_time is not None:
        results.append(('gRPC', grpc_time))
    
    if not results:
        print("No valid test results to compare")
        return
    
    # Sort by response time (fastest first)
    results.sort(key=lambda x: x[1])
    
    print(f"\nRanking (by average response time):")
    print("-" * 40)
    
    for rank, (method, avg_time) in enumerate(results, 1):
        if rank == 1:
            print(f"{rank}. {method:<10} {avg_time:>8.2f}ms (fastest)")
        else:
            fastest_time = results[0][1]
            ratio = avg_time / fastest_time
            slower_percent = (ratio - 1) * 100
            print(f"{rank}. {method:<10} {avg_time:>8.2f}ms ({slower_percent:.0f}% slower)")


def main():
    """Main function to run all benchmarks"""
    print("Synchronization Communication Patterns - Performance Benchmark")
    print("="*60)
    print("\nPlease ensure all services are running:")
    print("  1. Socket Server: docker-compose up python-socket-service (port 8080)")
    print("  2. REST API: docker-compose up python-rest-service (port 5000)")
    print("  3. gRPC Server: docker-compose up python-grpc-service (port 50051)")
    print()
    print("Or start all services at once:")
    print("  docker-compose up --build -d")
    print()
    
    input("Press Enter to start benchmarking...")
    
    iterations = 50
    
    # Run benchmarks
    socket_time = benchmark_socket(iterations)
    time.sleep(1)  # Brief pause between tests
    
    rest_time = benchmark_rest(iterations)
    time.sleep(1)  # Brief pause between tests
    
    grpc_time = benchmark_grpc(iterations)
    
    # Compare results
    compare_results(socket_time, rest_time, grpc_time)

if __name__ == '__main__':
    main()