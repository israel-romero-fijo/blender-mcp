
import json
import time
import socket
import threading
import sys
import os

# Add src to path so we can import blender_mcp
sys.path.append(os.path.join(os.getcwd(), "src"))

# Mock mcp and other dependencies for server.py
class MockMCP:
    def tool(self):
        return lambda f: f
    def prompt(self):
        return lambda f: f
    def run(self):
        pass

# Mocking the mcp module before importing server
import types
mcp_mock = types.ModuleType("mcp")
mcp_mock.server = types.ModuleType("mcp.server")
mcp_mock.server.fastmcp = types.ModuleType("mcp.server.fastmcp")
mcp_mock.server.fastmcp.FastMCP = lambda *args, **kwargs: MockMCP()
mcp_mock.server.fastmcp.Context = types.ModuleType("Context")
mcp_mock.server.fastmcp.Image = types.ModuleType("Image")
sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_mock.server
sys.modules["mcp.server.fastmcp"] = mcp_mock.server.fastmcp

import blender_mcp.server
from blender_mcp.server import BlenderConnection, get_blender_connection

def mock_blender_addon(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', port))
    sock.listen(5)

    while True:
        try:
            client, addr = sock.accept()
            # print(f"Mock server accepted connection from {addr}")
            while True:
                data = client.recv(1024)
                if not data:
                    break
                # print(f"Mock server received: {data}")
                cmd = json.loads(data.decode('utf-8'))
                if cmd['type'] == 'get_polyhaven_status':
                    resp = {"status": "success", "result": {"enabled": True, "message": "Enabled"}}
                elif cmd['type'] == 'ping':
                    resp = {"status": "success", "result": "pong"}
                else:
                    resp = {"status": "success", "result": "ok"}
                client.sendall(json.dumps(resp).encode('utf-8'))
            client.close()
        except Exception as e:
            # print(f"Mock server error: {e}")
            break
    sock.close()

def benchmark_connection():
    port = 9877 # Use a different port
    t = threading.Thread(target=mock_blender_addon, args=(port,), daemon=True)
    t.start()
    time.sleep(1) # Wait for server to start

    # We must patch the global port used in get_blender_connection or
    # manually initialize _blender_connection
    print("Benchmarking redundant pings...")

    # Manual initialization for the benchmark
    blender_mcp.server._blender_connection = BlenderConnection(host="localhost", port=port)
    if not blender_mcp.server._blender_connection.connect():
        print("Failed to connect in benchmark")
        return

    # Warm up and initial status fetch
    try:
        # In the new implementation, get_blender_connection will only call send_command
        # if _blender_connection is None.
        # But wait, our new implementation of get_blender_connection:
        # 1. If _blender_connection is NOT None, it checks fileno() and returns.
        # 2. If it IS None, it connects and calls get_polyhaven_status.

        # Reset to None to trigger the initial connection and status caching
        blender_mcp.server._blender_connection.disconnect()
        blender_mcp.server._blender_connection = None

        # We need to temporarily override the port in the module to make get_blender_connection use our mock port
        # Unfortunately it's hardcoded in the function. Let's patch BlenderConnection instead.

        original_BlenderConnection = blender_mcp.server.BlenderConnection
        class PatchedBlenderConnection(original_BlenderConnection):
            def __init__(self, host="localhost", port=9876):
                super().__init__(host=host, port=9877) # Force our port

        blender_mcp.server.BlenderConnection = PatchedBlenderConnection

        start_time = time.time()
        for i in range(100):
            get_blender_connection()
        end_time = time.time()

        print(f"Time for 100 get_blender_connection calls: {end_time - start_time:.4f}s")
        print(f"Average time per call: {(end_time - start_time)/100:.4f}s")

    finally:
        blender_mcp.server.BlenderConnection = original_BlenderConnection

def benchmark_json_parsing():
    conn = BlenderConnection(host="localhost", port=9877)

    # Mock socket to return chunks of a large JSON
    class MockSocket:
        def __init__(self, data_chunks):
            self.chunks = data_chunks
            self.idx = 0
            self.timeout = 15.0
        def recv(self, size):
            if self.idx < len(self.chunks):
                chunk = self.chunks[self.idx]
                self.idx += 1
                return chunk
            return b''
        def settimeout(self, t):
            self.timeout = t
        def rstrip(self): # dummy for chunk.rstrip()
            return self

    large_data = {"result": "x" * 100000} # ~100KB
    json_data = json.dumps(large_data).encode('utf-8')
    chunks = [json_data[i:i+1024] for i in range(0, len(json_data), 1024)]

    print(f"\nBenchmarking JSON parsing with {len(chunks)} chunks...")

    start_time = time.time()
    # We call it multiple times to see the effect
    for _ in range(10):
        mock_sock = MockSocket(chunks)
        conn.receive_full_response(mock_sock)
    end_time = time.time()
    print(f"Time for 10 iterations of receiving {len(json_data)/1024:.1f}KB in {len(chunks)} chunks: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_connection()
    benchmark_json_parsing()
