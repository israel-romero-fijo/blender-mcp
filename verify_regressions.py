import sys
from unittest.mock import MagicMock

# Mock modules
sys.modules['mcp'] = MagicMock()
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server.fastmcp'] = MagicMock()
sys.modules['bpy'] = MagicMock()
sys.modules['mathutils'] = MagicMock()
sys.modules['bpy.props'] = MagicMock()
sys.modules['bpy.app.timers'] = MagicMock()
sys.modules['bpy.types'] = MagicMock()
sys.modules['bpy.utils'] = MagicMock()
sys.modules['requests'] = MagicMock()

def test_imports():
    try:
        import src.blender_mcp.server as server
        import addon
        print("Successfully imported server and addon with mocks")

        # Basic check of optimized get_blender_connection
        server._blender_connection = MagicMock()
        server._blender_connection.sock.fileno.return_value = 1
        conn = server.get_blender_connection()
        assert conn == server._blender_connection
        # In our optimized version, it shouldn't call send_command if fileno is valid
        # Actually it calls send_command(get_polyhaven_status) only on initial connect/reconnect
        server._blender_connection.send_command.assert_not_called()
        print("get_blender_connection optimized check passed")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Verification failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_imports()
