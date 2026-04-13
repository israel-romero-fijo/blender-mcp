import time
import socket
import json
import threading
import sys
import os
from unittest.mock import MagicMock

# Mock mcp
mcp_mock = MagicMock()
sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_mock
sys.modules["mcp.server.fastmcp"] = mcp_mock

# Add src to path to import BlenderConnection
sys.path.append(os.path.join(os.getcwd(), "src"))

import blender_mcp.server as server
from blender_mcp.server import BlenderConnection

class MockBlender:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.running = True

    def run(self):
        self.sock.settimeout(0.5)
        while self.running:
            try:
                conn, addr = self.sock.accept()
                with conn:
                    while self.running:
                        data = conn.recv(1024)
                        if not data:
                            break
                        cmd = json.loads(data.decode('utf-8'))
                        if cmd['type'] == 'get_polyhaven_status':
                            response = {"status": "success", "result": {"enabled": True}}
                            conn.sendall(json.dumps(response).encode('utf-8'))
                        else:
                            response = {"status": "success", "result": {}}
                            conn.sendall(json.dumps(response).encode('utf-8'))
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"MockBlender error: {e}")
                break

    def stop(self):
        self.running = False
        # Create a dummy connection to break the accept() call
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.close()
        except:
            pass
        self.sock.close()

def benchmark():
    mock = MockBlender()
    thread = threading.Thread(target=mock.run)
    thread.daemon = True
    thread.start()

    time.sleep(0.5) # Wait for server to start

    try:
        # Initial connection
        server.get_blender_connection()

        # Measure get_blender_connection overhead
        start_time = time.time()
        for _ in range(100):
            conn = server.get_blender_connection()
        end_time = time.time()

        avg_time = (end_time - start_time) / 100
        print(f"Average time for get_blender_connection (with ping): {avg_time*1000:.4f} ms")

        # Now let's mock the optimization
        # In a real scenario, we'd only ping once or use a heartbeat

        def optimized_get_blender_connection():
            if server._blender_connection is not None:
                try:
                    # Check if socket is still alive locally without network call
                    if server._blender_connection.sock.fileno() != -1:
                        return server._blender_connection
                except:
                    pass

            # Reconnect logic...
            server._blender_connection = BlenderConnection(host="localhost", port=9876)
            server._blender_connection.connect()
            return server._blender_connection

        start_time = time.time()
        for _ in range(100):
            conn = optimized_get_blender_connection()
        end_time = time.time()

        avg_time_opt = (end_time - start_time) / 100
        print(f"Average time for get_blender_connection (optimized): {avg_time_opt*1000:.4f} ms")
        print(f"Speedup: {avg_time / avg_time_opt:.2f}x")

    finally:
        mock.stop()
        # thread.join() # Don't join as we force closed the socket

if __name__ == "__main__":
    benchmark()
