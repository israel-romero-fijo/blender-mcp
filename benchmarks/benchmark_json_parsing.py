import json
import time
import socket
import threading

def benchmark_json_parsing():
    # Create a large JSON object
    large_data = {"items": ["item" + str(i) for i in range(10000)], "status": "success"}
    json_str = json.dumps(large_data)
    json_bytes = json_str.encode('utf-8')

    # Simulate receiving in small chunks
    chunk_size = 1024
    chunks = [json_bytes[i:i+chunk_size] for i in range(0, len(json_bytes), chunk_size)]

    print(f"Total chunks: {len(chunks)}")
    print(f"Total size: {len(json_bytes)} bytes")

    # Current logic simulation
    start_time = time.time()
    received_chunks = []
    for chunk in chunks:
        received_chunks.append(chunk)
        try:
            data = b''.join(received_chunks)
            json.loads(data.decode('utf-8'))
        except json.JSONDecodeError:
            continue
    end_time = time.time()
    print(f"Current logic time: {end_time - start_time:.4f}s")

    # Optimized logic simulation
    start_time = time.time()
    received_chunks = []
    for chunk in chunks:
        received_chunks.append(chunk)
        # Only try to parse if it looks like it might be complete
        if chunk.rstrip().endswith((b'}', b']')):
            try:
                data = b''.join(received_chunks)
                json.loads(data.decode('utf-8'))
            except json.JSONDecodeError:
                continue
    end_time = time.time()
    print(f"Optimized logic time: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    benchmark_json_parsing()
