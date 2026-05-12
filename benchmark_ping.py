import socket
import threading
import time
import json

def start_mock_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', port))
    server.listen(1)

    def handle_client(conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(json.dumps({"status": "success", "result": {"enabled": True}}).encode('utf-8'))
        conn.close()

    def run():
        try:
            while True:
                conn, addr = server.accept()
                t = threading.Thread(target=handle_client, args=(conn,))
                t.daemon = True
                t.start()
        except:
            pass
        finally:
            server.close()

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
    return server

def benchmark_ping():
    port = 9877
    server = start_mock_server(port)
    time.sleep(0.1)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', port))

    # Measure 100 pings
    n = 100
    start_time = time.time()
    for _ in range(n):
        client.sendall(json.dumps({"type": "get_polyhaven_status", "params": {}}).encode('utf-8'))
        data = client.recv(1024)
    end_time = time.time()

    avg_latency = (end_time - start_time) / n
    print(f"Average roundtrip latency: {avg_latency * 1000:.4f} ms")

    client.close()

if __name__ == "__main__":
    benchmark_ping()
