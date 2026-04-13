import unittest
import sys
import os
import json
import socket
import threading
import time
from unittest.mock import MagicMock, patch

# Mock mcp before importing server
mcp_mock = MagicMock()
sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_mock
sys.modules["mcp.server.fastmcp"] = mcp_mock

# Mock bpy and other blender modules
sys.modules["bpy"] = MagicMock()
sys.modules["bpy.props"] = MagicMock()
sys.modules["bpy.app.timers"] = MagicMock()
sys.modules["bpy.types"] = MagicMock()
sys.modules["bpy.utils"] = MagicMock()
sys.modules["mathutils"] = MagicMock()

import bpy
# Set up some side effects for timers.register
def mock_register(func, first_interval=0.0):
    # Execute immediately in the test thread for simplicity
    func()
    return None
bpy.app.timers.register.side_effect = mock_register

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from blender_mcp.server import BlenderConnection
import addon

class TestOptimizations(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.port = 9878 # Use a different port
        self.server = addon.BlenderMCPServer(host=self.host, port=self.port)

        # Mock addon behavior
        def mock_execute_internal(command):
            if command.get("type") == "get_polyhaven_status":
                return {"status": "success", "result": {"enabled": True}}
            return {"status": "success", "result": {"echo": command.get("params")}}

        self.server._execute_command_internal = mock_execute_internal
        self.server.start()
        time.sleep(0.5)

    def tearDown(self):
        self.server.stop()
        time.sleep(0.5)

    def test_communication_flow(self):
        """Test that the optimized server and addon can still communicate"""
        conn = BlenderConnection(host=self.host, port=self.port)
        self.assertTrue(conn.connect())

        # Test a small command
        result = conn.send_command("get_polyhaven_status")
        self.assertTrue(result.get("enabled"))

        # Test a larger command (simulated)
        large_code = "print('hello world')\n" * 1000
        result = conn.send_command("execute_code", {"code": large_code})
        self.assertEqual(result.get("echo", {}).get("code"), large_code)

        conn.disconnect()

    def test_json_tail_heuristic(self):
        """Test the tail-byte heuristic explicitly"""
        conn = BlenderConnection(host=self.host, port=self.port)
        self.assertTrue(conn.connect())

        # Command that doesn't end with } or ] (should fail or timeout if logic is wrong)
        # But we send valid JSON, just checking if it processes correctly.
        result = conn.send_command("execute_code", {"code": "123"})
        self.assertEqual(result.get("echo", {}).get("code"), "123")

        conn.disconnect()

if __name__ == "__main__":
    unittest.main()
