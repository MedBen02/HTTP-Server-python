import socket
import threading
import os
import mimetypes
import urllib.parse

HOST = 'localhost'
PORT = 9000
PUBLIC_DIR = 'public'
TEMPLATE_DIR = 'templates'

ROUTES_GET = {}
ROUTES_POST = {}

def route(path, method='GET'):
    def decorator(func):
        if method == 'POST':
            ROUTES_POST[path] = func
        else:
            ROUTES_GET[path] = func
        return func
    return decorator

@route('/')
def home():
    return serve_file('index.html')

@route('/contact')
def contact_form():
    return render_template('contact.html', {})

@route('/contact', method='POST')
def contact_submit(form_data):
    name = form_data.get('name', 'anonymous')
    message = form_data.get('message', '')
    context = {'name': name, 'message': message}
    return render_template('thankyou.html', context)

def serve_file(filename):
    filepath = os.path.join(PUBLIC_DIR, filename)
    if not os.path.exists(filepath):
        return not_found_response()
    with open(filepath, 'rb') as f:
        content = f.read()
    content_type, _ = mimetypes.guess_type(filepath)
    return http_response(200, content, content_type or 'application/octet-stream')

def render_template(template_name, context):
    filepath = os.path.join(TEMPLATE_DIR, template_name)
    if not os.path.exists(filepath):
        return not_found_response()
    with open(filepath, 'r') as f:
        content = f.read()
    for key, value in context.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return http_response(200, content.encode(), 'text/html')

def not_found_response():
    body = b"<h1>404 Not Found</h1><p>The page you requested does not exist.</p>"
    return http_response(404, body, "text/html")

def http_response(status_code, body_bytes, content_type):
    reason = {200: "OK", 404: "Not Found"}.get(status_code, "OK")
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
        return None, None, {}
    try:
        method, path, _ = lines[0].split()
        headers = {}
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        return method, path, headers
    except:
        return None, None, {}

def parse_form_data(body):
    return {k: v for k, v in urllib.parse.parse_qsl(body)}

def handle_client(sock, addr):
    try:
        raw_data = sock.recv(1024).decode()
        method, path, headers = parse_request(raw_data)

        print(f"[{addr}] {method} {path}")

        if method == 'GET':
            handler = ROUTES_GET.get(path, None)
            if handler:
                response = handler()
            elif path.startswith('/static/'):
                filename = path.replace('/static/', '')
                response = serve_file(filename)
            else:
                response = not_found_response()

        elif method == 'POST':
            body = raw_data.split("\r\n\r\n", 1)[1]
            form_data = parse_form_data(body)
            handler = ROUTES_POST.get(path, None)
            if handler:
                response = handler(form_data)
            else:
                response = not_found_response()
        else:
            response = not_found_response()

        sock.sendall(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"🚀 Server running at http://{HOST}:{PORT}")
    try:
        while True:
            client, addr = s.accept()
            threading.Thread(target=handle_client, args=(client, addr)).start()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server.")
        s.close()

if __name__ == '__main__':
    start_server()
