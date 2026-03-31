import sys
import os
import json
import time
import socket
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.abspath("src"))

# Mock mcp.server.fastmcp before importing server
sys.modules["mcp"] = MagicMock()
sys.modules["mcp.server"] = MagicMock()
sys.modules["mcp.server.fastmcp"] = MagicMock()

import blender_mcp.server as server

class MockSocket:
    def __init__(self, responses=None):
        self.sent_data = []
        self.responses = responses or []
        self.is_connected = True
        self.timeout = None
        self._fileno = 10

    def connect(self, addr):
        self.is_connected = True

    def sendall(self, data):
        self.sent_data.append(data)

    def recv(self, bufsize):
        if not self.responses:
            return b""
        resp = self.responses.pop(0)
        return resp

    def settimeout(self, t):
        self.timeout = t

    def close(self):
        self.is_connected = False
        self._fileno = -1

    def fileno(self):
        return self._fileno

def benchmark():
    print("--- Starting Benchmark ---")

    # 1. Test get_blender_connection round-trips
    mock_sock = MockSocket()

    ping_resp = json.dumps({"status": "success", "result": {"enabled": True}}).encode("utf-8")
    scene_resp = json.dumps({"status": "success", "result": {"name": "Scene", "objects": []}}).encode("utf-8")

    mock_sock.responses = [ping_resp, scene_resp]

    with patch("socket.socket", return_value=mock_sock):
        server._blender_connection = None
        # 1st call: should connect and ping
        server.get_blender_connection()
        print(f"Initial connection commands: {len(mock_sock.sent_data)}")

        mock_sock.sent_data = []
        # 2nd call (simulated by tool): should NOT ping
        start_time = time.time()
        server.get_scene_info(MagicMock())
        end_time = time.time()

        print(f"Tool call (get_scene_info) took: {(end_time - start_time)*1000:.2f}ms")
        print(f"Tool call commands sent: {len(mock_sock.sent_data)}")
        for i, data in enumerate(mock_sock.sent_data):
            print(f"  Command {i+1}: {data.decode('utf-8')}")

    # 2. Test large response handling (receive_full_response)
    large_data = {"status": "success", "result": {"assets": {f"asset_{i}": {"name": f"Asset {i}", "desc": "a"*100} for i in range(1000)}}}
    large_json = json.dumps(large_data).encode("utf-8")
    chunks = [large_json[i:i+100] for i in range(0, len(large_json), 100)]

    mock_sock = MockSocket(responses=list(chunks))
    blender_conn = server.BlenderConnection("localhost", 9876, mock_sock)

    start_time = time.time()
    result = blender_conn.receive_full_response(mock_sock)
    end_time = time.time()

    print(f"Receiving {len(large_json)} bytes in {len(chunks)} chunks took: {(end_time - start_time)*1000:.2f}ms")

    # 3. Test string building performance
    large_assets = {f"id_{i}": {"name": f"Asset {i}", "type": 1, "categories": ["cat1", "cat2"], "download_count": i} for i in range(2000)}

    with patch("blender_mcp.server.get_blender_connection") as mock_get_conn:
        mock_conn = MagicMock()
        mock_conn.send_command.return_value = {
            "assets": large_assets,
            "total_count": 2000,
            "returned_count": 2000
        }
        mock_get_conn.return_value = mock_conn

        start_time = time.time()
        server.search_polyhaven_assets(MagicMock())
        end_time = time.time()
        print(f"search_polyhaven_assets (2000 assets) took: {(end_time - start_time)*1000:.2f}ms")

if __name__ == "__main__":
    benchmark()
