import json
import time

def simulate_receiving(data_bytes, chunk_size=8192):
    buffer = b''
    parse_count = 0
    start_time = time.time()
    for i in range(0, len(data_bytes), chunk_size):
        chunk = data_bytes[i:i+chunk_size]
        buffer += chunk
        parse_count += 1
        try:
            # Current implementation
            json.loads(buffer.decode('utf-8'))
            break
        except json.JSONDecodeError:
            pass
    end_time = time.time()
    return end_time - start_time, parse_count

def simulate_receiving_optimized(data_bytes, chunk_size=8192):
    chunks = []
    parse_count = 0
    start_time = time.time()
    for i in range(0, len(data_bytes), chunk_size):
        chunk = data_bytes[i:i+chunk_size]
        chunks.append(chunk)
        # Optimization: only attempt to parse if it looks like the end of a JSON object
        if chunk.rstrip().endswith((b'}', b']')):
            parse_count += 1
            try:
                # Optimized implementation
                # Use b''.join only when necessary
                data = b''.join(chunks)
                json.loads(data) # no decode
                break
            except json.JSONDecodeError:
                pass
    end_time = time.time()
    return end_time - start_time, parse_count

large_data = {"data": "x" * (1024 * 1024 * 5)} # 5MB
json_bytes = json.dumps(large_data).encode('utf-8')

print(f"Testing with {len(json_bytes)/1024/1024:.2f} MB payload")

t1, c1 = simulate_receiving(json_bytes)
print(f"Original: {t1:.4f}s, parses: {c1}")

t2, c2 = simulate_receiving_optimized(json_bytes)
print(f"Optimized: {t2:.4f}s, parses: {c2}")

if t2 > 0:
    print(f"Improvement: {t1/t2:.1f}x faster")
else:
    print("Optimized is too fast to measure")
