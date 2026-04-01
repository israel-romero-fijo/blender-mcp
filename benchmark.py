import json
import time
import socket
import threading

# Simulated data
# Create a moderately large JSON to see the effect of repeated parsing
large_json = {"status": "success", "result": {"objects": [{"name": f"Object_{i}", "type": "MESH", "location": [i*1.1, i*2.2, i*3.3]} for i in range(500)]}}
large_data = json.dumps(large_json).encode('utf-8')
# Split into many small chunks to simulate multiple network packets
chunk_size = 1024
chunks = [large_data[i:i+chunk_size] for i in range(0, len(large_data), chunk_size)]

print(f"Data size: {len(large_data)} bytes, Number of chunks: {len(chunks)}")

def original_receive(chunks_input):
    received_chunks = []
    parse_count = 0
    for chunk in chunks_input:
        received_chunks.append(chunk)
        parse_count += 1
        try:
            data = b''.join(received_chunks)
            json.loads(data.decode('utf-8'))
            return data, parse_count
        except json.JSONDecodeError:
            continue
    return None, parse_count

def optimized_receive(chunks_input):
    received_chunks = []
    parse_count = 0
    for chunk in chunks_input:
        received_chunks.append(chunk)
        # Only attempt to parse if the chunk ends with a potential JSON terminator
        if chunk.rstrip().endswith(b'}'):
            parse_count += 1
            try:
                data = b''.join(received_chunks)
                json.loads(data.decode('utf-8'))
                return data, parse_count
            except json.JSONDecodeError:
                continue
    return None, parse_count

# Benchmark JSON parsing
print("\n--- JSON Parsing Benchmark ---")
iterations = 1000

start = time.time()
total_parses = 0
for _ in range(iterations):
    _, p = original_receive(chunks)
    total_parses += p
duration = time.time() - start
print(f"Original receive: {duration:.4f}s (Total parses: {total_parses})")

start = time.time()
total_parses = 0
for _ in range(iterations):
    _, p = optimized_receive(chunks)
    total_parses += p
duration = time.time() - start
print(f"Optimized receive: {duration:.4f}s (Total parses: {total_parses})")


# Benchmark Redundant Ping (Conceptual)
print("\n--- Redundant Ping Impact (Calculated) ---")
# Assume a modest RTT of 5ms for local socket communication
rtt = 0.005
tool_calls = 100
print(f"Assumed RTT: {rtt*1000}ms")
print(f"Current approach (ping + command): {tool_calls * (rtt + rtt) * 1000:.1f}ms for {tool_calls} calls")
print(f"Optimized approach (command only): {tool_calls * rtt * 1000:.1f}ms for {tool_calls} calls")
print(f"Potential saving: 50% latency reduction per tool call")
