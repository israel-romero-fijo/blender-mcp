import json
import time

def benchmark_json_parsing(data_size, chunk_size):
    # Create a large JSON object
    large_data = {"data": "x" * data_size}
    json_str = json.dumps(large_data).encode('utf-8')

    # Simulate receiving in chunks
    chunks = [json_str[i:i+chunk_size] for i in range(0, len(json_str), chunk_size)]

    # Original way
    start_time = time.time()
    accumulated_chunks = []
    original_parse_count = 0
    for chunk in chunks:
        accumulated_chunks.append(chunk)
        original_parse_count += 1
        try:
            data = b''.join(accumulated_chunks)
            json.loads(data.decode('utf-8'))
        except json.JSONDecodeError:
            continue
    original_duration = time.time() - start_time

    # Optimized way
    start_time = time.time()
    accumulated_chunks = []
    optimized_parse_count = 0
    for chunk in chunks:
        accumulated_chunks.append(chunk)
        if chunk.rstrip().endswith((b'}', b']')):
            optimized_parse_count += 1
            try:
                data = b''.join(accumulated_chunks)
                json.loads(data.decode('utf-8'))
            except json.JSONDecodeError:
                pass
    optimized_duration = time.time() - start_time

    print(f"Data size: {len(json_str) / 1024:.2f} KB")
    print(f"Chunks: {len(chunks)}")
    print(f"Original duration: {original_duration:.6f} s (Parses: {original_parse_count})")
    print(f"Optimized duration: {optimized_duration:.6f} s (Parses: {optimized_parse_count})")
    if original_duration > 0:
        print(f"Improvement: {(original_duration - optimized_duration) / original_duration * 100:.2f}%")

if __name__ == "__main__":
    print("Benchmarking with 1MB data...")
    benchmark_json_parsing(1024 * 1024, 1024)
