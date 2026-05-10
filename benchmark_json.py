import json
import time

def receive_full_response_OLD(chunks):
    received_chunks = []
    for chunk in chunks:
        received_chunks.append(chunk)
        try:
            data = b''.join(received_chunks)
            json.loads(data.decode('utf-8'))
            # return data # In real code it returns here
        except json.JSONDecodeError:
            continue
    return b''.join(received_chunks)

def receive_full_response_NEW(chunks):
    received_chunks = []
    for chunk in chunks:
        received_chunks.append(chunk)
        # Quick check for JSON terminator
        if chunk.rstrip().endswith((b'}', b']')):
            try:
                data = b''.join(received_chunks)
                json.loads(data.decode('utf-8'))
                return data
            except json.JSONDecodeError:
                continue
    return b''.join(received_chunks)

# Generate a large JSON payload in chunks
large_data = {"data": "x" * (1024 * 1024)} # 1MB
json_str = json.dumps(large_data).encode('utf-8')
chunk_size = 1024 # Smaller chunks to amplify the effect
chunks = [json_str[i:i+chunk_size] for i in range(0, len(json_str), chunk_size)]

print(f"Number of chunks: {len(chunks)}")

# Warmup
receive_full_response_OLD(chunks[:10])
receive_full_response_NEW(chunks[:10])

start = time.time()
receive_full_response_OLD(chunks)
print(f"OLD time: {time.time() - start:.4f}s")

start = time.time()
receive_full_response_NEW(chunks)
print(f"NEW time: {time.time() - start:.4f}s")
