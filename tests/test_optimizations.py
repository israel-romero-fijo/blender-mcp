import sys
import unittest
from unittest.mock import MagicMock, patch
import json
import os

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Mock mcp before importing server
mock_mcp = MagicMock()
sys.modules['mcp'] = mock_mcp
sys.modules['mcp.server.fastmcp'] = mock_mcp

import blender_mcp.server as server

class TestServerOptimizations(unittest.TestCase):
    def test_receive_full_response_optimized(self):
        # Mock socket
        mock_sock = MagicMock()

        # Test case 1: Small complete JSON in one chunk
        data = json.dumps({"status": "success"}).encode('utf-8')
        mock_sock.recv.side_effect = [data, b'']

        conn = server.BlenderConnection("localhost", 9876)
        received = conn.receive_full_response(mock_sock)
        self.assertEqual(received, data)

        # Test case 2: Incomplete JSON, then complete JSON
        chunk1 = b'{"status":'
        chunk2 = b' "success"}'
        mock_sock.recv.side_effect = [chunk1, chunk2, b'']

        received = conn.receive_full_response(mock_sock)
        self.assertEqual(received, chunk1 + chunk2)

    def test_get_blender_connection_caching(self):
        with patch('blender_mcp.server.BlenderConnection') as MockConn:
            # Setup mock connection
            mock_conn_inst = MockConn.return_value
            mock_conn_inst.connect.return_value = True
            mock_conn_inst.sock.fileno.return_value = 10
            mock_conn_inst.send_command.return_value = {"enabled": True}

            # Reset globals
            server._blender_connection = None

            # First call should connect and fetch status
            conn1 = server.get_blender_connection()
            self.assertTrue(mock_conn_inst.connect.called)
            self.assertTrue(mock_conn_inst.send_command.called)

            # Second call should use fileno and NOT send_command
            mock_conn_inst.send_command.reset_mock()
            conn2 = server.get_blender_connection()
            self.assertEqual(conn1, conn2)
            self.assertFalse(mock_conn_inst.send_command.called)

    def test_network_error_invalidates_global_connection(self):
        # Setup mock connection
        mock_sock = MagicMock()
        mock_sock.fileno.return_value = 10

        conn = server.BlenderConnection("localhost", 9876)
        conn.sock = mock_sock
        server._blender_connection = conn

        # Verify it's currently connected
        self.assertEqual(server.get_blender_connection(), conn)

        # Simulate network error in send_command
        mock_sock.sendall.side_effect = ConnectionResetError("Lost")

        with self.assertRaises(Exception):
            conn.send_command("test")

        # Verify global connection is now None
        self.assertIsNone(server._blender_connection)

if __name__ == '__main__':
    unittest.main()
