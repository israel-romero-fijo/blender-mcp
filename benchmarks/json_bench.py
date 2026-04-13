import time
import json
import io

def benchmark_json_loads():
    # Create a large-ish JSON object
    large_data = {"data": "x" * (5 * 1024 * 1024)} # 5MB
    json_str = json.dumps(large_data)
    json_bytes = json_str.encode('utf-8')

    chunk_size = 8192
    chunks = [json_bytes[i:i+chunk_size] for i in range(0, len(json_bytes), chunk_size)]

    # Baseline: Current approach
    start_time = time.time()
    current_buffer = []
    for chunk in chunks:
        current_buffer.append(chunk)
        try:
            full_data = b''.join(current_buffer)
            json.loads(full_data.decode('utf-8'))
        except json.JSONDecodeError:
            pass
    end_time = time.time()
    print(f"Current approach (repeated json.loads): {end_time - start_time:.4f} seconds")

    # Optimized approach: Heuristic check before json.loads
    start_time = time.time()
    current_buffer = []
    for chunk in chunks:
        current_buffer.append(chunk)
        # Fast heuristic: only try parsing if the chunk ends with } or ]
        if chunk.rstrip()[-1:] in (b'}', b']'):
            try:
                full_data = b''.join(current_buffer)
                json.loads(full_data.decode('utf-8'))
            except json.JSONDecodeError:
                pass
    end_time = time.time()
    print(f"Optimized approach (with heuristic): {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_json_loads()
