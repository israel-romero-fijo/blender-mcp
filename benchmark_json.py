import json
import time
import io

def benchmark():
    # Create a large JSON object
    data = {"items": ["item" * 100 for _ in range(1000)]}
    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')

    chunk_size = 1024
    chunks = [json_bytes[i:i+chunk_size] for i in range(0, len(json_bytes), chunk_size)]

    print(f"Total size: {len(json_bytes)} bytes")
    print(f"Number of chunks: {len(chunks)}")

    # Current approach
    start_time = time.time()
    buffer = b''
    loads_count = 0
    for chunk in chunks:
        buffer += chunk
        loads_count += 1
        try:
            json.loads(buffer.decode('utf-8'))
            # Success!
            break
        except json.JSONDecodeError:
            pass
    current_duration = time.time() - start_time
    print(f"Current approach: {current_duration:.4f}s ({loads_count} loads)")

    # Optimized approach
    start_time = time.time()
    chunks_list = []
    loads_count = 0
    for chunk in chunks:
        chunks_list.append(chunk)
        # Only try to parse if it looks like a complete JSON object
        if chunk.rstrip().endswith((b'}', b']')):
            loads_count += 1
            try:
                data = b''.join(chunks_list)
                json.loads(data.decode('utf-8'))
                # Success!
                break
            except json.JSONDecodeError:
                pass
    optimized_duration = time.time() - start_time
    print(f"Optimized approach: {optimized_duration:.4f}s ({loads_count} loads)")

    if optimized_duration > 0:
        print(f"Speedup: {current_duration / optimized_duration:.1f}x")

if __name__ == "__main__":
    benchmark()
