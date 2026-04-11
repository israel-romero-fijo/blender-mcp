import time
import socket
import threading
import json

def start_mock_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', port))
    sock.listen(1)

    def handle():
        while True:
            try:
                client, addr = sock.accept()
                while True:
                    data = client.recv(1024)
                    if not data: break
                    client.sendall(json.dumps({"status": "success", "result": {"enabled": True}}).encode('utf-8'))
                client.close()
            except:
                break

    t = threading.Thread(target=handle, daemon=True)
    t.start()
    return sock

port = 9877
mock_server = start_mock_server(port)

# Connect
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('localhost', port))

# Measure ping time
n = 100
start = time.time()
for _ in range(n):
    conn.sendall(json.dumps({"type": "get_polyhaven_status"}).encode('utf-8'))
    data = conn.recv(1024)
end = time.time()
print(f"Time for {n} pings: {end - start:.4f}s ({(end - start)/n:.6f}s per ping)")

# Measure fileno check time
start = time.time()
for _ in range(n):
    assert conn.fileno() != -1
end = time.time()
print(f"Time for {n} fileno checks: {end - start:.4f}s ({(end - start)/n:.6f}s per check)")

conn.close()
mock_server.close()
