import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9000))

# Send HTTP request
http_request = (
    "GET / HTTP/1.1\r\n"
    "Host: localhost:9000\r\n"
    "Connection: close\r\n"
    "\r\n"
)
client_socket.sendall(http_request.encode())

# Receive the response
response = b""
while True:
    data = client_socket.recv(5000)
    if not data:
        break
    response += data

# Decode and print the response
print("--- Response from server ---")
print(response.decode(),end='')

client_socket.close()