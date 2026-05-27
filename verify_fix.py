import os
import sys
from unittest.mock import MagicMock

# Mock bpy and other modules before importing addon
class MockOperator:
    def __init__(self, *args, **kwargs):
        pass
    def report(self, type, message):
        pass

bpy_mock = MagicMock()
bpy_mock.types.Operator = MockOperator

sys.modules['bpy'] = bpy_mock
sys.modules['mathutils'] = MagicMock()
sys.modules['bpy.props'] = MagicMock()
sys.modules['requests'] = MagicMock()

import bpy

def test_key_loading():
    print("Testing RODIN_FREE_TRIAL_KEY loading...")

    # Mock environment variable
    test_key = "test_key_123"
    os.environ["RODIN_FREE_TRIAL_KEY"] = test_key

    # Import or reload to pick up the change
    import addon
    import importlib
    importlib.reload(addon)

    if addon.RODIN_FREE_TRIAL_KEY == test_key:
        print("SUCCESS: RODIN_FREE_TRIAL_KEY loaded correctly from environment.")
    else:
        print(f"FAILURE: RODIN_FREE_TRIAL_KEY expected {test_key}, got {addon.RODIN_FREE_TRIAL_KEY}")
        return False
    return True

def test_operator_logic():
    print("Testing Operator logic...")
    import addon
    import importlib

    # 1. Test when key is missing
    os.environ["RODIN_FREE_TRIAL_KEY"] = ""
    importlib.reload(addon)

    operator = addon.BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey()
    context = MagicMock()

    result = operator.execute(context)
    if result == {'CANCELLED'}:
        print("SUCCESS: Operator correctly cancelled when key is missing.")
    else:
        print(f"FAILURE: Operator expected {{'CANCELLED'}}, got {result}")
        return False

    # 2. Test when key is present
    test_key = "present_key"
    os.environ["RODIN_FREE_TRIAL_KEY"] = test_key
    importlib.reload(addon)

    operator = addon.BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey()
    context = MagicMock()
    # Mock scene properties
    context.scene.blendermcp_hyper3d_api_key = ""

    result = operator.execute(context)
    if result == {'FINISHED'} and context.scene.blendermcp_hyper3d_api_key == test_key:
        print("SUCCESS: Operator correctly set the key when present.")
    else:
        print(f"FAILURE: Operator expected {{'FINISHED'}} and key {test_key}, got {result} and {context.scene.blendermcp_hyper3d_api_key}")
        return False

    return True

def test_status_logic():
    print("Testing get_hyper3d_status logic...")
    import addon
    import importlib

    # Mock server instance
    server = addon.BlenderMCPServer()

    # 1. Key set in env, and matches scene key
    test_key = "env_key"
    os.environ["RODIN_FREE_TRIAL_KEY"] = test_key
    importlib.reload(addon)

    bpy.context.scene.blendermcp_use_hyper3d = True
    bpy.context.scene.blendermcp_hyper3d_api_key = test_key
    bpy.context.scene.blendermcp_hyper3d_mode = "MAIN_SITE"

    status = server.get_hyper3d_status()
    if "free_trial" in status["message"]:
        print("SUCCESS: Correctly identified free_trial key.")
    else:
        print(f"FAILURE: Expected free_trial in message, got: {status['message']}")
        return False

    # 2. Key NOT set in env, scene has some key
    os.environ["RODIN_FREE_TRIAL_KEY"] = ""
    importlib.reload(addon)

    bpy.context.scene.blendermcp_hyper3d_api_key = "some_user_key"
    status = server.get_hyper3d_status()
    if "private" in status["message"]:
        print("SUCCESS: Correctly identified private key when env key is empty.")
    else:
        print(f"FAILURE: Expected private in message, got: {status['message']}")
        return False

    return True

if __name__ == "__main__":
    success = True
    success &= test_key_loading()
    success &= test_operator_logic()
    success &= test_status_logic()

    if success:
        print("\nALL VERIFICATION TESTS PASSED!")
        sys.exit(0)
    else:
        print("\nSOME VERIFICATION TESTS FAILED!")
        sys.exit(1)
