
import time
import json
import socket
import logging

# Mocking enough of the environment to run the benchmark
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Benchmark")

class BlenderConnection:
    def __init__(self, host="localhost", port=9876):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self) -> bool:
        if self.sock:
            return True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            return True
        except Exception as e:
            return False

    def disconnect(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None

    def receive_full_response(self, sock, buffer_size=8192):
        chunks = []
        sock.settimeout(15.0)
        try:
            while True:
                chunk = sock.recv(buffer_size)
                if not chunk:
                    break
                chunks.append(chunk)
                if chunk.rstrip().endswith((b"}", b"]")):
                    try:
                        data = b"".join(chunks)
                        json.loads(data.decode("utf-8"))
                        return data
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            raise e
        if chunks:
            return b"".join(chunks)
        raise Exception("No data received")

    def send_command(self, command_type: str, params=None):
        if not self.sock and not self.connect():
            raise ConnectionError("Not connected")
        command = {"type": command_type, "params": params or {}}
        self.sock.sendall(json.dumps(command).encode("utf-8"))
        response_data = self.receive_full_response(self.sock)
        response = json.loads(response_data.decode("utf-8"))
        return response.get("result", {})

_blender_connection = None
_polyhaven_enabled = False

def get_blender_connection_original():
    global _blender_connection, _polyhaven_enabled
    if _blender_connection is not None:
        try:
            result = _blender_connection.send_command("get_polyhaven_status")
            _polyhaven_enabled = result.get("enabled", False)
            return _blender_connection
        except Exception:
            _blender_connection = None

    if _blender_connection is None:
        _blender_connection = BlenderConnection(host="localhost", port=9876)
        _blender_connection.connect()
    return _blender_connection

def get_blender_connection_optimized():
    global _blender_connection
    if _blender_connection is not None:
        return _blender_connection

    if _blender_connection is None:
        _blender_connection = BlenderConnection(host="localhost", port=9876)
        _blender_connection.connect()
    return _blender_connection

def main():
    # This requires the Blender addon to be running.
    # Since we are in a headless environment, we might need to mock the server if it's not running.
    # But wait, I can actually start a mock server to test the overhead.
    pass

if __name__ == "__main__":
    import threading

    def start_mock_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 9876))
        server.listen(1)
        while True:
            client, addr = server.accept()
            while True:
                data = client.recv(1024)
                if not data: break
                cmd = json.loads(data.decode())
                if cmd["type"] == "get_polyhaven_status":
                    resp = {"status": "success", "result": {"enabled": True}}
                else:
                    resp = {"status": "success", "result": {"data": "dummy"}}
                client.sendall(json.dumps(resp).encode())
            client.close()

    t = threading.Thread(target=start_mock_server, daemon=True)
    t.start()
    time.sleep(0.1) # Wait for server to start

    # Measure original
    start = time.time()
    for _ in range(100):
        conn = get_blender_connection_original()
        conn.send_command("get_scene_info")
    end = time.time()
    print(f"Original time for 100 calls: {end - start:.4f}s")

    # Reset connection
    _blender_connection.disconnect()
    _blender_connection = None

    # Measure optimized
    start = time.time()
    for _ in range(100):
        conn = get_blender_connection_optimized()
        conn.send_command("get_scene_info")
    end = time.time()
    print(f"Optimized time for 100 calls: {end - start:.4f}s")
