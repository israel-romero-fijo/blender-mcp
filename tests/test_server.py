import sys
from unittest.mock import MagicMock, patch

# Mock mcp module before importing the server
mcp_mock = MagicMock()
sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_mock.server
sys.modules["mcp.server.fastmcp"] = mcp_mock.server.fastmcp

import unittest
import json
import socket
import pytest
import os

# We need to mock the decorators and classes used at module level
class MockFastMCP:
    def __init__(self, *args, **kwargs):
        pass
    def tool(self, *args, **kwargs):
        return lambda x: x
    def resource(self, *args, **kwargs):
        return lambda x: x
    def prompt(self, *args, **kwargs):
        return lambda x: x
    def run(self, *args, **kwargs):
        pass

mcp_mock.server.fastmcp.FastMCP = MockFastMCP
mcp_mock.server.fastmcp.Context = MagicMock()
mcp_mock.server.fastmcp.Image = MagicMock()

from blender_mcp.server import (
    BlenderConnection,
    _process_bbox,
    get_blender_connection,
    get_scene_info,
    get_object_info
)

class TestProcessBBox(unittest.TestCase):
    def test_none_input(self):
        assert _process_bbox(None) is None

    def test_all_ints(self):
        input_bbox = [10, 20, 30]
        assert _process_bbox(input_bbox) == input_bbox

    def test_floats_normalization(self):
        input_bbox = [0.5, 1.0, 2.0]
        # max is 2.0. [0.5/2.0 * 100, 1.0/2.0 * 100, 2.0/2.0 * 100] = [25, 50, 100]
        assert _process_bbox(input_bbox) == [25, 50, 100]

    def test_invalid_range(self):
        with pytest.raises(ValueError, match="Incorrect number range"):
            _process_bbox([-1.0, 1.0, 1.0])

class TestBlenderConnection(unittest.TestCase):
    def setUp(self):
        self.conn = BlenderConnection(host="localhost", port=9876)

    @patch("socket.socket")
    def test_connect_success(self, mock_socket):
        mock_sock_inst = MagicMock()
        mock_socket.return_value = mock_sock_inst

        assert self.conn.connect() is True
        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_sock_inst.connect.assert_called_with(("localhost", 9876))
        assert self.conn.sock == mock_sock_inst

    @patch("socket.socket")
    def test_connect_failure(self, mock_socket):
        mock_sock_inst = MagicMock()
        mock_sock_inst.connect.side_effect = Exception("Connection refused")
        mock_socket.return_value = mock_sock_inst

        assert self.conn.connect() is False
        assert self.conn.sock is None

    def test_disconnect(self):
        mock_sock = MagicMock()
        self.conn.sock = mock_sock
        self.conn.disconnect()
        mock_sock.close.assert_called_once()
        assert self.conn.sock is None

    def test_receive_full_response_success(self):
        mock_sock = MagicMock()
        # Mocking recv to return chunks that form a valid JSON
        mock_sock.recv.side_effect = [b'{"status": "ok", ', b'"result": {"foo": "bar"}}', b'']

        data = self.conn.receive_full_response(mock_sock)
        assert json.loads(data.decode('utf-8')) == {"status": "ok", "result": {"foo": "bar"}}

    @patch.object(BlenderConnection, "connect")
    @patch.object(BlenderConnection, "receive_full_response")
    def test_send_command_success(self, mock_receive, mock_connect):
        mock_sock = MagicMock()
        self.conn.sock = mock_sock
        mock_receive.return_value = json.dumps({"status": "success", "result": {"data": 123}}).encode('utf-8')

        result = self.conn.send_command("test_cmd", {"p": 1})

        assert result == {"data": 123}
        mock_sock.sendall.assert_called_once()
        sent_data = json.loads(mock_sock.sendall.call_args[0][0].decode('utf-8'))
        assert sent_data == {"type": "test_cmd", "params": {"p": 1}}

class TestGlobalConnection(unittest.TestCase):
    @patch("blender_mcp.server.BlenderConnection")
    def test_get_blender_connection_new(self, mock_conn_cls):
        # Reset global state for test
        with patch("blender_mcp.server._blender_connection", None):
            mock_inst = mock_conn_cls.return_value
            mock_inst.connect.return_value = True

            conn = get_blender_connection()

            assert conn == mock_inst
            mock_conn_cls.assert_called_once_with(host="localhost", port=9876)

    def test_get_blender_connection_existing_valid(self):
        mock_conn = MagicMock()
        mock_conn.send_command.return_value = {"enabled": True}

        with patch("blender_mcp.server._blender_connection", mock_conn):
            conn = get_blender_connection()
            assert conn == mock_conn
            mock_conn.send_command.assert_called_with("get_polyhaven_status")

class TestTools(unittest.TestCase):
    @patch("blender_mcp.server.get_blender_connection")
    def test_get_scene_info(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.send_command.return_value = {"scene": "main"}

        ctx = MagicMock()
        result = get_scene_info(ctx)

        assert json.loads(result) == {"scene": "main"}
        mock_conn.send_command.assert_called_with("get_scene_info")

    @patch("blender_mcp.server.get_blender_connection")
    def test_get_object_info(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.send_command.return_value = {"name": "Cube", "type": "MESH"}

        ctx = MagicMock()
        result = get_object_info(ctx, "Cube")

        assert json.loads(result) == {"name": "Cube", "type": "MESH"}
        mock_conn.send_command.assert_called_with("get_object_info", {"name": "Cube"})
