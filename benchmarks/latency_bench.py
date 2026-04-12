import sys
from unittest.mock import MagicMock

# Mock MCP
mcp_mock = MagicMock()
sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_mock.server
sys.modules["mcp.server.fastmcp"] = mcp_mock.server.fastmcp

import time
import socket
import json
import threading

# Mock Blender Addon Server
class MockBlenderAddon:
    def __init__(self, host='localhost', port=9877):
        self.host = host
        self.port = port
        self.running = False
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        while self.running:
            try:
                self.socket.settimeout(1.0)
                client, _ = self.socket.accept()
                while self.running:
                    try:
                        data = client.recv(8192)
                        if not data: break
                        cmd = json.loads(data)
                        response = {"status": "success", "result": {"enabled": True, "message": "ok"}}
                        client.sendall(json.dumps(response).encode('utf-8'))
                    except:
                        break
                client.close()
            except socket.timeout:
                continue
            except:
                break

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()

# Mocking parts of server.py for benchmarking
import src.blender_mcp.server as server

def bench_connection():
    addon = MockBlenderAddon()
    addon.start()
    time.sleep(0.5)

    # Inject mock port
    server._blender_connection = None

    conn = server.BlenderConnection(host='localhost', port=9877)
    conn.connect()
    server._blender_connection = conn

    # Warmup
    server.get_blender_connection()

    iterations = 1000
    start = time.time()
    for _ in range(iterations):
        server.get_blender_connection()
    end = time.time()

    avg_latency = (end - start) / iterations
    print(f"Average get_blender_connection latency (Optimized): {avg_latency*1000:.6f}ms")

    # Compare with a ping
    start = time.time()
    for _ in range(iterations):
        conn.send_command("get_polyhaven_status")
    end = time.time()
    avg_ping_latency = (end - start) / iterations
    print(f"Average ping latency: {avg_ping_latency*1000:.6f}ms")

    print(f"Estimated speedup for heartbeat check: {avg_ping_latency / avg_latency:.2f}x")

    addon.stop()

if __name__ == "__main__":
    bench_connection()
