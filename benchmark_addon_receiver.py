import time

def benchmark_accumulation():
    # 16MB payload
    payload_size = 16 * 1024 * 1024
    chunk_size = 8192
    num_chunks = payload_size // chunk_size
    chunks = [b"a" * chunk_size for _ in range(num_chunks)]

    print(f"Benchmarking accumulation of {num_chunks} chunks ({payload_size} bytes)")

    # Quadratic concatenation
    start = time.time()
    buffer = b""
    for chunk in chunks:
        buffer += chunk
    end = time.time()
    concat_time = end - start
    print(f"Byte concatenation (buffer += data): {concat_time:.4f}s")

    # List accumulation
    start = time.time()
    received_chunks = []
    for chunk in chunks:
        received_chunks.append(chunk)
    result = b"".join(received_chunks)
    end = time.time()
    list_time = end - start
    print(f"List accumulation (chunks.append + join): {list_time:.4f}s")

    if list_time > 0:
        print(f"Speedup: {concat_time / list_time:.1f}x")

if __name__ == "__main__":
    benchmark_accumulation()
