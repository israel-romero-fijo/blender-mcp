import json
import time
import io

def receive_full_response_unoptimized(chunks_in):
    chunks = []
    for chunk in chunks_in:
        chunks.append(chunk)
        try:
            data = b''.join(chunks)
            json.loads(data.decode('utf-8'))
            return data
        except json.JSONDecodeError:
            continue
    return None

def receive_full_response_optimized(chunks_in):
    chunks = []
    for chunk in chunks_in:
        chunks.append(chunk)
        # Bolt Optimization: Only attempt JSON parse if it looks complete
        if not chunk.rstrip().endswith((b'}', b']')):
            continue

        try:
            data = b''.join(chunks)
            json.loads(data) # Optimized: json.loads can handle bytes
            return data
        except json.JSONDecodeError:
            continue
    return None

# Generate a large JSON object
large_data = {"data": "x" * (1024 * 1024 * 5)} # 5MB
json_str = json.dumps(large_data).encode('utf-8')

# Split into chunks
chunk_size = 8192
chunks = [json_str[i:i+chunk_size] for i in range(0, len(json_str), chunk_size)]

print(f"Number of chunks: {len(chunks)}")

start = time.time()
receive_full_response_unoptimized(chunks)
unoptimized_time = time.time() - start
print(f"Unoptimized time: {unoptimized_time:.4f}s")

start = time.time()
receive_full_response_optimized(chunks)
optimized_time = time.time() - start
print(f"Optimized time: {optimized_time:.4f}s")

if optimized_time > 0:
    print(f"Speedup: {unoptimized_time / optimized_time:.2f}x")
