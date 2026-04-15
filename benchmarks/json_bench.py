import json
import time
import io

def benchmark_optimized_vs_unoptimized():
    # Create a large JSON object (around 1MB)
    large_data = {"data": "x" * (1024 * 1024)}
    json_str = json.dumps(large_data)
    json_bytes = json_str.encode('utf-8')

    # Simulate receiving in 8KB chunks
    chunk_size = 8192
    chunks = [json_bytes[i:i+chunk_size] for i in range(0, len(json_bytes), chunk_size)]

    print(f"Number of chunks: {len(chunks)}")

    # Unoptimized: join, decode, and parse on every chunk
    start_time = time.time()
    buffer = b''
    parse_attempts = 0
    for chunk in chunks:
        buffer += chunk
        parse_attempts += 1
        try:
            json.loads(buffer.decode('utf-8'))
        except json.JSONDecodeError:
            pass
    unoptimized_time = time.time() - start_time
    print(f"Unoptimized time: {unoptimized_time:.4f}s (Attempts: {parse_attempts})")

    # Optimized: only join and parse if it ends with terminator
    start_time = time.time()
    chunks_list = []
    parse_attempts = 0
    for chunk in chunks:
        chunks_list.append(chunk)
        if chunk.rstrip().endswith((b'}', b']')):
            parse_attempts += 1
            try:
                full_data = b''.join(chunks_list)
                json.loads(full_data)
                # Success, but in benchmark we keep going if we wanted to simulate multiple messages
                # but here it's one message.
            except json.JSONDecodeError:
                pass
    optimized_time = time.time() - start_time
    print(f"Optimized time: {optimized_time:.4f}s (Attempts: {parse_attempts})")

    print(f"Speedup: {unoptimized_time / optimized_time:.2f}x")

if __name__ == "__main__":
    benchmark_optimized_vs_unoptimized()
