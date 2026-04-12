import sys
import unittest
import json
from unittest.mock import MagicMock, patch

# Mock mcp modules
mcp_mock = MagicMock()
sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_mock.server
sys.modules["mcp.server.fastmcp"] = mcp_mock.server.fastmcp

# Mock blender modules
sys.modules["bpy"] = MagicMock()
sys.modules["bpy.props"] = MagicMock()
sys.modules["bpy.app"] = MagicMock()
sys.modules["bpy.app.timers"] = MagicMock()
sys.modules["bpy.types"] = MagicMock()
sys.modules["bpy.utils"] = MagicMock()
sys.modules["mathutils"] = MagicMock()

# Mock requests
sys.modules["requests"] = MagicMock()

import src.blender_mcp.server as server
import addon

class TestOptimizations(unittest.TestCase):
    def test_server_receive_full_response_optimized(self):
        """Test that server properly handles fragmented JSON with the optimization"""
        mock_sock = MagicMock()
        large_dict = {"test": "x" * 10000}
        full_json = json.dumps(large_dict).encode('utf-8')

        # Split into chunks that don't end in }
        chunks = [full_json[:5000], full_json[5000:]]
        mock_sock.recv.side_effect = chunks + [b'']

        conn = server.BlenderConnection("localhost", 9876)
        result = conn.receive_full_response(mock_sock)

        self.assertEqual(result, full_json)
        self.assertEqual(json.loads(result), large_dict)

    def test_addon_handle_client_optimized(self):
        """Test that addon properly handles fragmented JSON with the optimization"""
        mock_client = MagicMock()
        large_cmd = {"type": "test", "params": {"data": "y" * 10000}}
        full_json = json.dumps(large_cmd).encode('utf-8')

        # Fragmentation:
        # Chunk 1: half of json (doesn't end with })
        # Chunk 2: other half (ends with })
        chunks = [full_json[:5000], full_json[5000:]]
        mock_client.recv.side_effect = chunks + [b'']

        s = addon.BlenderMCPServer()
        s.running = True

        processed_commands = []
        with patch.object(s, 'execute_command') as mock_exec:
            def side_effect(cmd):
                processed_commands.append(cmd)
                return {"status": "success"}
            mock_exec.side_effect = side_effect

            with patch('addon.bpy.app.timers.register') as mock_timer:
                def timer_side_effect(func, first_interval=0.0):
                    func() # Execute immediately
                mock_timer.side_effect = timer_side_effect

                s._handle_client(mock_client)

        self.assertEqual(len(processed_commands), 1)
        self.assertEqual(processed_commands[0], large_cmd)

    def test_connection_caching(self):
        """Test that get_blender_connection caches the connection and doesn't ping every time"""
        server._blender_connection = None

        mock_conn = MagicMock(spec=server.BlenderConnection)
        mock_conn.sock.fileno.return_value = 10

        with patch('src.blender_mcp.server.BlenderConnection', return_value=mock_conn):
            # First call - should connect and ping
            c1 = server.get_blender_connection()
            self.assertEqual(mock_conn.connect.call_count, 1)
            self.assertEqual(mock_conn.send_command.call_count, 1) # Initial status fetch

            # Second call - should use cache and NOT ping
            c2 = server.get_blender_connection()
            self.assertEqual(c1, c2)
            self.assertEqual(mock_conn.connect.call_count, 1)
            self.assertEqual(mock_conn.send_command.call_count, 1) # Still 1

if __name__ == "__main__":
    unittest.main()
