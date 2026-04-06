import json
import time
import io

def unoptimized_parse(chunks):
    buffer = b''
    start_time = time.time()
    for chunk in chunks:
        buffer += chunk
        try:
            json.loads(buffer.decode('utf-8'))
            break
        except json.JSONDecodeError:
            continue
    return time.time() - start_time

def optimized_parse(chunks):
    buffer_list = []
    start_time = time.time()
    for chunk in chunks:
        buffer_list.append(chunk)
        if chunk.rstrip().endswith((b'}', b']')):
            try:
                data = b''.join(buffer_list)
                json.loads(data.decode('utf-8'))
                break
            except json.JSONDecodeError:
                continue
    return time.time() - start_time

def main():
    # Create a large JSON object
    large_data = {"data": "x" * (1024 * 1024)} # 1MB
    json_str = json.dumps(large_data)
    json_bytes = json_str.encode('utf-8')

    # Split into 8KB chunks
    chunk_size = 8192
    chunks = [json_bytes[i:i+chunk_size] for i in range(0, len(json_bytes), chunk_size)]

    print(f"Number of chunks: {len(chunks)}")

    t1 = unoptimized_parse(chunks)
    print(f"Unoptimized time: {t1:.4f}s")

    t2 = optimized_parse(chunks)
    print(f"Optimized time: {t2:.4f}s")

    if t2 > 0:
        print(f"Improvement: {(t1-t2)/t1*100:.2f}%")

if __name__ == "__main__":
    main()
