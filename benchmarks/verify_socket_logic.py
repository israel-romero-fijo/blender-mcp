import json

def verify_optimized_logic(payload_str):
    payload_bytes = payload_str.encode('utf-8')
    # Simulate various chunking
    for chunk_size in [1, 5, 10, 100, 1000]:
        chunks = [payload_bytes[i:i+chunk_size] for i in range(0, len(payload_bytes), chunk_size)]

        received_chunks = []
        parsed_data = None
        for chunk in chunks:
            received_chunks.append(chunk)
            # Optimized logic check
            if chunk.rstrip().endswith((b'}', b']')):
                try:
                    data = b''.join(received_chunks)
                    parsed_data = json.loads(data.decode('utf-8'))
                    break
                except json.JSONDecodeError:
                    continue

        expected_data = json.loads(payload_str)
        assert parsed_data == expected_data, f"Failed for chunk_size {chunk_size}"

def main():
    test_cases = [
        '{"status": "success", "result": {"key": "value"}}',
        '[1, 2, 3, 4, 5]',
        '{"nested": {"list": [1, 2, 3]}}',
        '{"space": "at end"}   ',
        '{"newline": "at end"}\n',
    ]

    for tc in test_cases:
        try:
            verify_optimized_logic(tc)
            print(f"Passed: {tc[:50]}...")
        except Exception as e:
            print(f"Failed: {tc[:50]}... Error: {e}")

if __name__ == "__main__":
    main()
