import sys
import os
import json
import socket
import unittest
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.abspath("src"))

# Mock mcp.server.fastmcp before importing server
# We need mcp.tool() to act as a pass-through decorator
mock_mcp_instance = MagicMock()
def tool_decorator(*args, **kwargs):
    def wrapper(func):
        return func
    return wrapper
mock_mcp_instance.tool = tool_decorator

sys.modules["mcp"] = MagicMock()
sys.modules["mcp.server"] = MagicMock()
sys.modules["mcp.server.fastmcp"] = MagicMock()
# Inject our custom mock instance
with patch("mcp.server.fastmcp.FastMCP", return_value=mock_mcp_instance):
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

class TestServerLogic(unittest.TestCase):
    def setUp(self):
        server._blender_connection = None

    def test_receive_full_response_optimized(self):
        """Test that receive_full_response still correctly parses multi-chunk JSON"""
        data = {"status": "success", "result": "ok"}
        json_data = json.dumps(data).encode("utf-8")

        # Split into chunks that don't end with } except the last one
        chunks = [b'{"status": "', b'success", "res', b'ult": "ok"}']
        mock_sock = MockSocket(responses=chunks)

        blender_conn = server.BlenderConnection("localhost", 9876, mock_sock)
        result_raw = blender_conn.receive_full_response(mock_sock)

        self.assertEqual(json.loads(result_raw.decode("utf-8")), data)

    def test_get_blender_connection_caching(self):
        """Test that get_blender_connection only pings once and then caches"""
        mock_sock = MockSocket()
        ping_resp = json.dumps({"status": "success", "result": {"enabled": True}}).encode("utf-8")
        mock_sock.responses = [ping_resp]

        with patch("socket.socket", return_value=mock_sock):
            # 1st call
            conn1 = server.get_blender_connection()
            self.assertEqual(len(mock_sock.sent_data), 1)
            self.assertEqual(json.loads(mock_sock.sent_data[0].decode("utf-8"))["type"], "get_polyhaven_status")

            # 2nd call
            mock_sock.sent_data = []
            conn2 = server.get_blender_connection()
            self.assertEqual(conn1, conn2)
            self.assertEqual(len(mock_sock.sent_data), 0)

    def test_string_building_categories(self):
        """Verify optimized string building in get_polyhaven_categories"""
        with patch("blender_mcp.server.get_blender_connection") as mock_get_conn:
            mock_conn = MagicMock()
            mock_conn.send_command.return_value = {"categories": {"Rock": 10, "Sand": 5}}
            mock_get_conn.return_value = mock_conn

            # Set polyhaven_enabled to True for this test
            server._polyhaven_enabled = True

            result = server.get_polyhaven_categories(MagicMock(), "textures")
            self.assertIn("Categories for textures:", result)
            self.assertIn("- Rock: 10 assets", result)
            self.assertIn("- Sand: 5 assets", result)

if __name__ == "__main__":
    unittest.main()
