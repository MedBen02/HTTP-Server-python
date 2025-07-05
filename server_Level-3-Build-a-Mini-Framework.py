import socket
import threading
import os
import mimetypes

HOST = 'localhost'
PORT = 9000
PUBLIC_DIR = 'public'

# === Router ===
ROUTES = {}

def route(path):
    def decorator(func):
        ROUTES[path] = func
        return func
    return decorator

# === Request Handlers ===
@route('/')
def home():
    return serve_file('index.html')

@route('/about')
def about():
    return serve_file('about.html')

def serve_file(filename):
    filepath = os.path.join(PUBLIC_DIR, filename)
    if not os.path.exists(filepath):
        return not_found_response()
    with open(filepath, 'rb') as f:
        content = f.read()
    content_type, _ = mimetypes.guess_type(filepath)
    return http_response(200, content, content_type or 'application/octet-stream')

def not_found_response():
    body = b"<h1>404 Not Found</h1>"
    return http_response(404, body, "text/html")

def http_response(status_code, body_bytes, content_type):
    reason = {200:"OK", 404:"Not Found"}.get(status_code, "OK")
    headers = (
        f"HTTP/1.1 {status_code} {reason}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode() + body_bytes

def parse_request(data):
    lines = data.splitlines()
    if not lines:
        return None, None
    try:
        method, path, _ = lines[0].split()
        return method, path
    except:
        return None, None
    
def handle_client(client_socket, client_address):
    try:
        data = client_socket.recv(1024).decode()
        method, path = parse_request(data)

        print(f"[{client_address}] {method} {path}")

        if path in ROUTES:
            response = ROUTES[path]()
        elif path.startswith('/static/'):
            filename = path.replace('/static/', '')
            response = serve_file(filename)
        else:
            response = not_found_response()

        client_socket.sendall(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"🚀 Server running at http://{HOST}:{PORT}")

    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_addr)).start()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        server_socket.close()

if __name__ == '__main__':
    start_server()