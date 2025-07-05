import socket
import threading

HOST = 'localhost'
PORT = 9000

def handle_request(path):
    if path == "/":
        return html_response("<h1>Welcome to the home page</h1>")
    elif path == "/about":
        return html_response("<h1>About</h1><p>This is a threaded Python HTTP server.</p>")
    elif path.startswith("/hello"):
        name = "friend"
        if "?" in path and "name=" in path:
            query = path.split("?")[1]
            params = dict(pair.split("=") for pair in query.split("&") if "=" in pair)
            name = params.get("name", "friend")
        return html_response(f"<h1>Hello, {name.capitalize()}!</h1>")
    else:
        return not_found_response()

def html_response(body):
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )

def not_found_response():
    body = "<h1>404 Not Found</h1><p>The page you requested does not exist.</p>"
    return (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )

def parse_request(request_data):
    lines = request_data.splitlines()
    if not lines:
        return None, None
    try:
        method, full_path, _ = lines[0].split()
        return method, full_path
    except ValueError:
        return None, None
    
def handle_client(client_socket, client_address):
    try:
        request_data = client_socket.recv(1024).decode()
        method, path = parse_request(request_data)

        if method and path:
            print(f"[{client_address}] {method} {path}")
            response = handle_request(path)
        else:
            response = not_found_response()

        client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"🚀 Server is running on http://{HOST}:{PORT} (Ctrl+C to stop)")

    try:
        while True:
            client_connection, client_address = server_socket.accept()
            thread = threading.Thread(target = handle_client, args=(client_connection, client_address))
            thread.start()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down the server...")
        server_socket.close()

if __name__ == "__main__":
    start_server()
