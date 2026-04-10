import time
import socket
import json
import threading

def mock_blender_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 9877))
    sock.listen(1)
    while True:
        try:
            client, _ = sock.accept()
            while True:
                data = client.recv(8192)
                if not data: break
                cmd = json.loads(data.decode('utf-8'))
                if cmd['type'] == 'get_polyhaven_status':
                    response = {"status": "success", "result": {"enabled": True}}
                else:
                    response = {"status": "success", "result": {}}
                client.sendall(json.dumps(response).encode('utf-8'))
            client.close()
        except:
            break

def benchmark_ping():
    # Start mock server
    t = threading.Thread(target=mock_blender_server, daemon=True)
    t.start()
    time.sleep(0.5)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9877))

    # Benchmark with ping
    start = time.time()
    for _ in range(100):
        # Simulate get_blender_connection with ping
        sock.sendall(json.dumps({"type": "get_polyhaven_status"}).encode('utf-8'))
        json.loads(sock.recv(8192).decode('utf-8'))

        # Actual tool call
        sock.sendall(json.dumps({"type": "get_scene_info"}).encode('utf-8'))
        json.loads(sock.recv(8192).decode('utf-8'))
    end = time.time()
    print(f"With redundant ping: {end-start:.4f}s")

    # Benchmark without ping
    start = time.time()
    for _ in range(100):
        # Actual tool call only
        sock.sendall(json.dumps({"type": "get_scene_info"}).encode('utf-8'))
        json.loads(sock.recv(8192).decode('utf-8'))
    end = time.time()
    print(f"Without redundant ping: {end-start:.4f}s")

benchmark_ping()
