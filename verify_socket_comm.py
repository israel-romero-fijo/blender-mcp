import json
import socket
import threading
import time

def mock_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 9877))
    server_sock.listen(1)

    conn, addr = server_sock.accept()
    chunks = []
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            chunks.append(data)
            if data.rstrip().endswith((b'}', b']')):
                try:
                    full_data = b''.join(chunks)
                    json.loads(full_data)
                    # Send success response
                    conn.sendall(json.dumps({"status": "success"}).encode('utf-8'))
                    chunks = []
                except json.JSONDecodeError:
                    pass
    finally:
        conn.close()
        server_sock.close()

def verify():
    # Start mock server
    server_thread = threading.Thread(target=mock_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)

    # Client (simulating the MCP server or addon)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('localhost', 9877))

    # Send a fragmented JSON
    large_data = {"type": "test", "params": {"large": "x" * 5000}}
    json_str = json.dumps(large_data)
    json_bytes = json_str.encode('utf-8')

    # Send in chunks, ensuring the last chunk ends with }
    chunk1 = json_bytes[:2500]
    chunk2 = json_bytes[2500:]

    print(f"Sending chunk 1 ({len(chunk1)} bytes)...")
    client_sock.sendall(chunk1)
    time.sleep(0.1)

    print(f"Sending chunk 2 ({len(chunk2)} bytes)...")
    client_sock.sendall(chunk2)

    # Wait for response
    client_sock.settimeout(2.0)
    response = client_sock.recv(1024)
    print(f"Received response: {response.decode('utf-8')}")

    assert json.loads(response.decode('utf-8'))["status"] == "success"
    print("Verification successful!")

    client_sock.close()

if __name__ == "__main__":
    verify()
