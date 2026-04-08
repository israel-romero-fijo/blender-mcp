import time
import json
import socket
import threading
import logging

# Mock logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Benchmark")

class BlenderConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        return True

    def receive_full_response(self, sock, buffer_size=8192):
        chunks = []
        sock.settimeout(5.0)
        while True:
            try:
                chunk = sock.recv(buffer_size)
                if not chunk: break
                chunks.append(chunk)
                try:
                    data = b''.join(chunks)
                    json.loads(data.decode('utf-8'))
                    return data
                except json.JSONDecodeError:
                    continue
            except Exception as e:
                break
        return b''.join(chunks)

    def send_command(self, command_type, params=None):
        if not self.sock: self.connect()
        command = {"type": command_type, "params": params or {}}
        self.sock.sendall(json.dumps(command).encode('utf-8'))
        response_data = self.receive_full_response(self.sock)
        return json.loads(response_data.decode('utf-8'))

def get_blender_connection_original():
    global _blender_connection
    if _blender_connection is not None:
        try:
            # Ping every time
            _blender_connection.send_command("get_polyhaven_status")
            return _blender_connection
        except:
            _blender_connection = None

    _blender_connection = BlenderConnection("localhost", 9876)
    _blender_connection.connect()
    return _blender_connection

_blender_connection = None

def mock_blender_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 9876))
    server.listen(1)

    while True:
        client, addr = server.accept()
        try:
            while True:
                data = client.recv(1024)
                if not data: break
                # Just respond with success
                response = {"status": "success", "result": {"enabled": True}}
                client.sendall(json.dumps(response).encode('utf-8'))
        except:
            pass
        finally:
            client.close()

if __name__ == "__main__":
    # Start mock server in thread
    t = threading.Thread(target=mock_blender_server, daemon=True)
    t.start()
    time.sleep(0.1)

    print("Benchmarking original get_blender_connection (with ping)...")
    start = time.time()
    for _ in range(100):
        conn = get_blender_connection_original()
        conn.send_command("get_scene_info")
    end = time.time()
    print(f"Original took: {end - start:.4f}s for 100 tool calls")

    # Reset
    _blender_connection = None

    def get_blender_connection_optimized():
        global _blender_connection
        if _blender_connection is not None and _blender_connection.sock is not None:
            # Check if socket is still open without sending data
            # This is a very basic check. fileno() > 0 usually means it's not closed locally.
            if _blender_connection.sock.fileno() != -1:
                return _blender_connection

        _blender_connection = BlenderConnection("localhost", 9876)
        _blender_connection.connect()
        return _blender_connection

    print("\nBenchmarking optimized get_blender_connection (no ping)...")
    start = time.time()
    for _ in range(100):
        conn = get_blender_connection_optimized()
        conn.send_command("get_scene_info")
    end = time.time()
    print(f"Optimized took: {end - start:.4f}s for 100 tool calls")
