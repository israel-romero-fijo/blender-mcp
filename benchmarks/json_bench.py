import json
import time
import io

def simulate_receive_quadratic(data, chunk_size=8192):
    chunks = []
    total_parse_time = 0
    start_total = time.time()

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        chunks.append(chunk)
        full_buffer = b''.join(chunks)

        start_parse = time.time()
        try:
            json.loads(full_buffer.decode('utf-8'))
        except json.JSONDecodeError:
            pass
        total_parse_time += time.time() - start_parse

    end_total = time.time()
    return end_total - start_total, total_parse_time

def simulate_receive_optimized(data, chunk_size=8192):
    chunks = []
    total_parse_time = 0
    start_total = time.time()

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        chunks.append(chunk)

        # Optimization: only try parsing if it looks like the end of a JSON
        if chunk.rstrip().endswith((b'}', b']')):
            full_buffer = b''.join(chunks)
            start_parse = time.time()
            try:
                json.loads(full_buffer) # Use bytes directly
                # success
            except json.JSONDecodeError:
                pass
            total_parse_time += time.time() - start_parse

    end_total = time.time()
    return end_total - start_total, total_parse_time

# Create a large JSON payload (approx 2MB)
large_data = {"data": "x" * (2 * 1024 * 1024)}
json_bytes = json.dumps(large_data).encode('utf-8')

print(f"Payload size: {len(json_bytes) / 1024 / 1024:.2f} MB")

t_total_q, t_parse_q = simulate_receive_quadratic(json_bytes)
print(f"Quadratic: Total time: {t_total_q:.4f}s, Parse time: {t_parse_q:.4f}s")

t_total_o, t_parse_o = simulate_receive_optimized(json_bytes)
print(f"Optimized: Total time: {t_total_o:.4f}s, Parse time: {t_parse_o:.4f}s")

if t_total_o < t_total_q:
    print(f"Speedup: {t_total_q / t_total_o:.2f}x")
