
import time
import socket
import json
import threading
import sys
import os

# Mocking the server parts
def mock_blender_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', port))
    sock.listen(1)
    while True:
        try:
            conn, addr = sock.accept()
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Mock response for get_polyhaven_status
                cmd = json.loads(data.decode('utf-8'))
                if cmd['type'] == 'get_polyhaven_status':
                    response = json.dumps({"status": "success", "result": {"enabled": True, "message": "Enabled"}})
                    conn.sendall(response.encode('utf-8'))
                else:
                    response = json.dumps({"status": "success", "result": {}})
                    conn.sendall(response.encode('utf-8'))
        except:
            break

# Start mock server
port = 9878
threading.Thread(target=mock_blender_server, args=(port,), daemon=True).start()
time.sleep(0.1)

# Copy the relevant parts of server.py to test
from dataclasses import dataclass
from typing import Dict, Any
import logging

logger = logging.getLogger("Benchmark")

@dataclass
class BlenderConnection:
    host: str
    port: int
    sock: socket.socket = None

    def connect(self) -> bool:
        if self.sock: return True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            return True
        except:
            self.sock = None
            return False

    def receive_full_response(self, sock, buffer_size=8192):
        chunks = []
        sock.settimeout(5.0)
        while True:
            chunk = sock.recv(buffer_size)
            if not chunk: break
            chunks.append(chunk)
            if chunk.rstrip()[-1:] in (b'}', b']'):
                try:
                    data = b''.join(chunks)
                    json.loads(data)
                    return data
                except json.JSONDecodeError:
                    continue
        return b''.join(chunks)

    def send_command(self, command_type: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.sock and not self.connect():
            raise ConnectionError("Not connected")
        command = {"type": command_type, "params": params or {}}
        self.sock.sendall(json.dumps(command).encode('utf-8'))
        response_data = self.receive_full_response(self.sock)
        response = json.loads(response_data)
        return response.get("result", {})

_blender_connection = None
_polyhaven_enabled = False

def get_blender_connection():
    global _blender_connection, _polyhaven_enabled
    if _blender_connection is not None:
        try:
            # OPTIMIZED IMPLEMENTATION
            if _blender_connection.sock and _blender_connection.sock.fileno() != -1:
                return _blender_connection
            raise ConnectionError("Socket is closed")
        except Exception:
            _blender_connection = None

    if _blender_connection is None:
        _blender_connection = BlenderConnection(host="localhost", port=port)
        _blender_connection.connect()
        # Init polyhaven
        result = _blender_connection.send_command("get_polyhaven_status")
        _polyhaven_enabled = result.get("enabled", False)
    return _blender_connection

# Benchmark
print("Starting benchmark...")
start_time = time.time()
n = 100
for _ in range(n):
    conn = get_blender_connection()

end_time = time.time()
print(f"Time for {n} optimized get_blender_connection() calls: {end_time - start_time:.4f}s")
print(f"Average time per call: {(end_time - start_time)/n:.6f}s")
