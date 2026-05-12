import json
import time

def benchmark():
    payload = {"data": "x" * (1024 * 1024)} # 1MB
    payload_bytes = json.dumps(payload).encode('utf-8')
    chunk_size = 8192
    chunks = [payload_bytes[i:i+chunk_size] for i in range(0, len(payload_bytes), chunk_size)]

    print(f"Payload size: {len(payload_bytes) / 1024 / 1024:.2f} MB")
    print(f"Number of chunks: {len(chunks)}")

    # Inefficient way (current)
    start_time = time.time()
    buffer = b''
    parse_count = 0
    for chunk in chunks:
        buffer += chunk
        parse_count += 1
        try:
            json.loads(buffer.decode('utf-8'))
        except json.JSONDecodeError:
            pass
    end_time = time.time()
    print(f"Inefficient: {end_time - start_time:.4f}s (tried parsing {parse_count} times)")

    # Efficient way (terminator-aware)
    start_time = time.time()
    accumulated_chunks = []
    parse_count = 0
    for chunk in chunks:
        accumulated_chunks.append(chunk)
        if chunk.rstrip().endswith((b'}', b']')):
            parse_count += 1
            try:
                full_data = b''.join(accumulated_chunks)
                json.loads(full_data.decode('utf-8'))
            except json.JSONDecodeError:
                pass
    end_time = time.time()
    print(f"Efficient: {end_time - start_time:.4f}s (tried parsing {parse_count} times)")

if __name__ == "__main__":
    benchmark()
