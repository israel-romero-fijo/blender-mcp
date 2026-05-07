
import json
import time

def receive_full_response_original(chunks):
    """Simulate the original receive_full_response logic"""
    accumulated_data = b''
    for chunk in chunks:
        accumulated_data += chunk
        try:
            json.loads(accumulated_data.decode('utf-8'))
            # Success
        except json.JSONDecodeError:
            continue
    return accumulated_data

def receive_full_response_optimized(chunks):
    """Simulate the optimized terminator-aware logic"""
    accumulated_chunks = []
    for chunk in chunks:
        accumulated_chunks.append(chunk)
        # Only try to parse if the last byte looks like a JSON terminator
        if chunk and chunk.strip()[-1:] in (b'}', b']'):
            try:
                data = b''.join(accumulated_chunks)
                json.loads(data.decode('utf-8'))
                # Success
            except json.JSONDecodeError:
                continue
    return b''.join(accumulated_chunks)

# Create a large JSON object
large_data = {"data": "x" * (1024 * 1024)} # 1MB
json_data = json.dumps(large_data).encode('utf-8')

# Break it into 8KB chunks
chunk_size = 8192
chunks = [json_data[i:i+chunk_size] for i in range(0, len(json_data), chunk_size)]

print(f"Number of chunks: {len(chunks)}")

start = time.time()
receive_full_response_original(chunks)
print(f"Original time: {time.time() - start:.4f}s")

start = time.time()
receive_full_response_optimized(chunks)
print(f"Optimized time: {time.time() - start:.4f}s")
