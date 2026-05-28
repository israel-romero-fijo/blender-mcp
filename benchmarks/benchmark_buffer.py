
import time

def benchmark_buffer_accumulation():
    data_size = 10 * 1024 * 1024 # 10MB
    chunk_size = 8 * 1024 # 8KB
    chunks = [b"a" * chunk_size] * (data_size // chunk_size)

    # Current method: buffer += data
    start = time.time()
    buffer = b""
    for chunk in chunks:
        buffer += chunk
    end = time.time()
    print(f"buffer += data time: {end - start:.4f}s")

    # Optimized method: list append and join
    start = time.time()
    buffer_list = []
    for chunk in chunks:
        buffer_list.append(chunk)
    result = b"".join(buffer_list)
    end = time.time()
    print(f"list append and join time: {end - start:.4f}s")

if __name__ == "__main__":
    benchmark_buffer_accumulation()
