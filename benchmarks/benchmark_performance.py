
import json
import time
import sys
from unittest.mock import MagicMock

# Mock mcp before importing BlenderConnection
sys.modules['mcp'] = MagicMock()
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server.fastmcp'] = MagicMock()

import src.blender_mcp.server as server
from src.blender_mcp.server import BlenderConnection

def benchmark_json_parsing_logic(with_whitespace=False):
    case_name = "with trailing whitespace" if with_whitespace else "without whitespace"
    print(f"Benchmarking JSON parsing logic in optimized receive_full_response ({case_name})...")

    # Simulate a large JSON response
    large_dict = {"status": "success", "result": {"data": "x" * 1000000}}
    large_json = json.dumps(large_dict).encode('utf-8')
    if with_whitespace:
        large_json += b"\n"

    # We'll split it into many small chunks to simulate multiple recv calls
    chunk_size = 1024
    chunks = [large_json[i:i+chunk_size] for i in range(0, len(large_json), chunk_size)]

    def run_benchmark(optimized=False):
        received_chunks = []
        parse_attempts = 0
        start_time = time.time()

        # Mocking the optimized logic from server.py
        for chunk in chunks:
            received_chunks.append(chunk)

            if optimized:
                # Optimized logic in server.py (rstrip handles whitespace)
                if chunk.rstrip().endswith((b'}', b']')):
                    parse_attempts += 1
                    try:
                        data = b''.join(received_chunks)
                        json.loads(data.decode('utf-8'))
                    except json.JSONDecodeError:
                        pass
            else:
                # Original logic (expensive O(N^2) on every chunk)
                parse_attempts += 1
                try:
                    data = b''.join(received_chunks)
                    json.loads(data.decode('utf-8'))
                except json.JSONDecodeError:
                    pass

        end_time = time.time()
        return end_time - start_time, parse_attempts

    duration_orig, attempts_orig = run_benchmark(optimized=False)
    print(f"Original: {duration_orig:.4f}s, attempts: {attempts_orig}")

    duration_opt, attempts_opt = run_benchmark(optimized=True)
    print(f"Optimized: {duration_opt:.4f}s, attempts: {attempts_opt}")

    if duration_orig > 0:
        improvement = (duration_orig - duration_opt) / duration_orig * 100
        print(f"Improvement: {improvement:.2f}%")

def benchmark_get_connection_logic():
    print("\nBenchmarking get_blender_connection logic...")

    # Mock connection
    mock_conn = MagicMock()
    mock_conn.sock.fileno.return_value = 10
    # Simulate some work in send_command
    def mock_send_command(cmd):
        time.sleep(0.001) # Simulate 1ms network latency
        return {"enabled": True}
    mock_conn.send_command.side_effect = mock_send_command

    # Original logic (simulated)
    def original_get_conn():
        mock_conn.send_command("get_polyhaven_status")
        return mock_conn

    # Optimized logic (simulated)
    def optimized_get_conn():
        if mock_conn.sock and mock_conn.sock.fileno() != -1:
            return mock_conn
        return mock_conn

    start_time = time.time()
    for _ in range(100):
        original_get_conn()
    duration_orig = time.time() - start_time
    print(f"Original (100 calls): {duration_orig:.4f}s")

    start_time = time.time()
    for _ in range(100):
        optimized_get_conn()
    duration_opt = time.time() - start_time
    print(f"Optimized (100 calls): {duration_opt:.4f}s")

    if duration_orig > 0:
        improvement = (duration_orig - duration_opt) / duration_orig * 100
        print(f"Improvement: {improvement:.2f}%")

if __name__ == "__main__":
    benchmark_json_parsing_logic(with_whitespace=False)
    print()
    benchmark_json_parsing_logic(with_whitespace=True)
    benchmark_get_connection_logic()
