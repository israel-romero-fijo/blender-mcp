import json
import time
import io

def benchmark_json_parsing():
    # Create a large JSON payload (approx 1MB)
    payload_dict = {"data": "x" * (1024 * 1024)}
    payload_json = json.dumps(payload_dict).encode('utf-8')

    # Simulate receiving in 8KB chunks
    chunk_size = 8192
    chunks = [payload_json[i:i + chunk_size] for i in range(0, len(payload_json), chunk_size)]

    print(f"Payload size: {len(payload_json)} bytes")
    print(f"Number of chunks: {len(chunks)}")

    # 1. Current approach: json.loads on every chunk
    start_time = time.time()
    buffer = b''
    for chunk in chunks:
        buffer += chunk
        try:
            json.loads(buffer.decode('utf-8'))
        except json.JSONDecodeError:
            continue
    current_time = time.time() - start_time
    print(f"Current approach time: {current_time:.4f}s")

    # 2. Optimized approach: terminator-aware check
    start_time = time.time()
    chunks_list = []
    for chunk in chunks:
        chunks_list.append(chunk)
        # Only try to parse if it looks like a complete JSON object
        if chunk.rstrip().endswith((b'}', b']')):
            try:
                full_data = b''.join(chunks_list)
                json.loads(full_data.decode('utf-8'))
            except json.JSONDecodeError:
                continue
    optimized_time = time.time() - start_time
    print(f"Optimized approach time: {optimized_time:.4f}s")

    if optimized_time > 0:
        print(f"Speedup: {current_time / optimized_time:.2f}x")

if __name__ == "__main__":
    benchmark_json_parsing()
