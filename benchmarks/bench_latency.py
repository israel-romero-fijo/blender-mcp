import time
import socket

# Mock BlenderConnection for local bench
class MockConn:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def send_command(self, cmd):
        return {"enabled": True}

conn = MockConn()

def bench_ping():
    return conn.send_command("get_polyhaven_status")

def bench_fileno():
    if conn.sock is None or conn.sock.fileno() == -1:
        return False
    return True

# Measure overhead
start = time.time()
for _ in range(10000):
    bench_ping()
ping_time = time.time() - start

start = time.time()
for _ in range(10000):
    bench_fileno()
fileno_time = time.time() - start

print(f"Ping overhead (10k calls): {ping_time:.4f}s")
print(f"Fileno overhead (10k calls): {fileno_time:.4f}s")
print(f"Speedup: {ping_time / fileno_time:.2f}x")
