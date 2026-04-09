
import time
import json
import os

def benchmark_json_parsing(payload_size_mb=1):
    print(f"Benchmarking JSON parsing for {payload_size_mb}MB payload...")

    # Create a large JSON payload
    data = {"items": ["item" * 100 for _ in range(payload_size_mb * 1000)]}
    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')

    # Simulating receiving in chunks
    chunk_size = 8192
    chunks = [json_bytes[i:i+chunk_size] for i in range(0, len(json_bytes), chunk_size)]

    # Current implementation style: try json.loads on every chunk
    start_time = time.time()
    accumulated = b''
    parse_attempts = 0
    for chunk in chunks:
        accumulated += chunk
        parse_attempts += 1
        try:
            json.loads(accumulated.decode('utf-8'))
            # print(f"Parsed successfully at attempt {parse_attempts}")
        except json.JSONDecodeError:
            pass
    end_time = time.time()
    current_time = end_time - start_time
    print(f"Current implementation: {current_time:.4f}s ({parse_attempts} parse attempts)")

    # Optimized implementation: only try if ends with } or ]
    start_time = time.time()
    accumulated = b''
    parse_attempts = 0
    terminators = {ord('}'), ord(']')}
    for chunk in chunks:
        accumulated += chunk
        if accumulated and accumulated[-1] in terminators:
            parse_attempts += 1
            try:
                json.loads(accumulated.decode('utf-8'))
            except json.JSONDecodeError:
                pass
    end_time = time.time()
    optimized_time = end_time - start_time
    print(f"Optimized implementation: {optimized_time:.4f}s ({parse_attempts} parse attempts)")

    if optimized_time < current_time:
        improvement = (current_time - optimized_time) / current_time * 100
        print(f"Improvement: {improvement:.2f}%")
    else:
        print("No improvement detected in this local test.")

if __name__ == "__main__":
    benchmark_json_parsing(1)
