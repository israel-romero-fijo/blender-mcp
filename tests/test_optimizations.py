import sys
import json
from unittest.mock import MagicMock

# Mock requests
sys.modules['requests'] = MagicMock()

# Mock Blender modules
mock_bpy = MagicMock()
mock_mathutils = MagicMock()
sys.modules['bpy'] = mock_bpy
sys.modules['bpy.props'] = MagicMock()
sys.modules['bpy.app.timers'] = MagicMock()
sys.modules['bpy.types'] = MagicMock()
sys.modules['bpy.utils'] = MagicMock()
sys.modules['mathutils'] = mock_mathutils

# Mock mcp
mock_mcp_mod = MagicMock()
sys.modules['mcp'] = mock_mcp_mod
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server.fastmcp'] = MagicMock()

# Mock FastMCP decorator
def mock_tool():
    def decorator(f):
        return f
    return decorator
sys.modules['mcp.server.fastmcp'].FastMCP().tool = mock_tool

# Now import our modules
# Note: we need to mock server before it's imported in some cases, but here it's fine
import src.blender_mcp.server as server

def test_server_receive_full_response():
    # Setup
    conn = server.BlenderConnection("localhost", 9876)
    mock_sock = MagicMock()

    payload = b'{"status": "success", "result": {"key": "value"}}'
    # Return chunks: '{"status": "', 'success", "result": {"key": "value"}}'
    mock_sock.recv.side_effect = [payload[:15], payload[15:], b'']

    response = conn.receive_full_response(mock_sock)
    assert response == payload
    print("Server receive_full_response verified.")

if __name__ == "__main__":
    test_server_receive_full_response()
    print("All tests passed!")
