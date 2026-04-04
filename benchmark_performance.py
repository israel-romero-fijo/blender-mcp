import sys
import time
import json
import socket
import threading
from unittest.mock import MagicMock

# Mock mcp before importing server
mock_mcp = MagicMock()
sys.modules["mcp"] = mock_mcp
sys.modules["mcp.server"] = mock_mcp
sys.modules["mcp.server.fastmcp"] = mock_mcp

# Now we can import BlenderConnection
# We need to make sure src is in path
sys.path.append("src")
from blender_mcp.server import BlenderConnection

def mock_blender_server(port, response_data, chunks=1):
    """A simple mock server that returns JSON in chunks"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', port))
        s.listen(1)
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if not data:
                        break

                    # Split response_data into chunks
                    chunk_size = len(response_data) // chunks
                    if chunk_size == 0: chunk_size = 1

                    for i in range(0, len(response_data), chunk_size):
                        conn.sendall(response_data[i:i+chunk_size])
                        time.sleep(0.001) # Small delay to ensure they are separate chunks
            except:
                break

def benchmark_json_parsing():
    print("--- Benchmarking JSON Parsing ---")
    port = 9877
    # Large JSON response
    large_dict = {"status": "success", "result": {"data": "x" * 1000000}} # 1MB data
    response_data = json.dumps(large_dict).encode('utf-8')

    # Run mock server in background
    server_thread = threading.Thread(target=mock_blender_server, args=(port, response_data, 100))
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5) # Wait for server to start

    conn = BlenderConnection(host="localhost", port=port)

    start_time = time.perf_counter()
    result = conn.send_command("test")
    end_time = time.perf_counter()

    print(f"Time taken for 1MB response in 100 chunks: {end_time - start_time:.4f}s")
    conn.disconnect()

if __name__ == "__main__":
    benchmark_json_parsing()
