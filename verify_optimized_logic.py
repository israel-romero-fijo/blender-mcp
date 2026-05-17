import json
import io

def test_optimized_logic():
    # Simulate the logic in src/blender_mcp/server.py
    def receive_full_response_logic(chunks_received):
        chunks = []
        for chunk in chunks_received:
            chunks.append(chunk)
            if chunk.rstrip().endswith((b"}", b"]")):
                try:
                    data = b"".join(chunks)
                    json.loads(data)
                    return data
                except json.JSONDecodeError:
                    continue
        return None

    # Simulate the logic in addon.py
    def addon_handle_client_logic(chunks_received):
        chunks = []
        for data in chunks_received:
            chunks.append(data)
            if data.rstrip().endswith((b"}", b"]")):
                try:
                    full_data = b"".join(chunks)
                    command = json.loads(full_data.decode("utf-8"))
                    return command
                except json.JSONDecodeError:
                    continue
        return None

    # Test case 1: Complete JSON in one chunk
    payload = {"test": "data"}
    payload_bytes = json.dumps(payload).encode('utf-8')
    assert receive_full_response_logic([payload_bytes]) == payload_bytes
    assert addon_handle_client_logic([payload_bytes]) == payload

    # Test case 2: Fragmented JSON
    payload = {"large": "x" * 10000}
    payload_bytes = json.dumps(payload).encode('utf-8')
    fragment1 = payload_bytes[:5000]
    fragment2 = payload_bytes[5000:]

    # fragmented and doesn't end with } in first chunk
    assert receive_full_response_logic([fragment1]) is None
    assert receive_full_response_logic([fragment1, fragment2]) == payload_bytes

    assert addon_handle_client_logic([fragment1]) is None
    assert addon_handle_client_logic([fragment1, fragment2]) == payload

    # Test case 3: JSON with trailing whitespace
    payload = {"test": "whitespace"}
    payload_bytes = json.dumps(payload).encode('utf-8') + b"  \n "
    assert receive_full_response_logic([payload_bytes]) == payload_bytes
    assert addon_handle_client_logic([payload_bytes]) == payload

    print("All logic verification tests passed!")

if __name__ == "__main__":
    test_optimized_logic()
