import socket

def handle_request(path):
    if path == "/":
        return html_response("<h1>Welcome to the home page</h1>")
    elif path == "/about":
        return html_response("<h1>About this server</h1><p>Built from scratch in Python!</p>")
    elif path.startswith("/hello"):
        name = "friend"
        if "?" in path and "name=" in path:
            query = path.split("?")[1]
            params = dict(pair.split("=") for pair in query.split("&") if "=" in pair)
            name = params.get("name","friend")
        return html_response(f"<h1>Hello, {name.capitalize()}!</h1>")
    else:
        return not_found_response()
    

def html_response(body_html):
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body_html)}\r\n"
        "\r\n"
        f"{body_html}"
    )
    return response


def not_found_response():
    body = "<h1>404 Not Found</h1><p>The page you requested does not exist.</p>"
    response = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )
    return response

# ==== Server Setup ====

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost',9000))
server_socket.listen(1)
print("Server is listening on http://localhost:9000")

try:
    while True:
        client_connection, client_address = server_socket.accept()
        request_data = client_connection.recv(1024).decode()

        # Extract path from request line (first line)
        request_lines = request_data.splitlines()
        if request_lines:
            request_line = request_lines[0]
            method, full_path, _ = request_line.split()
            print(f"[{method}] Request for: {full_path}")

            response = handle_request(full_path)
            client_connection.sendall(response.encode())
        client_connection.close()
except KeyboardInterrupt:
    print("\nShutting down server.")
    server_socket.close()  