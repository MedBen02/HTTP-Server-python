from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
try :
    server_socket.bind(('localhost',9000))
    server_socket.listen(50)
    while(1):
        (client_connection, address) = server_socket.accept()
        request = client_connection.recv(5000).decode()
        print("\n--- Request Received ---")
        print(request)

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content_Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>Hello from scratch!</h1></body></html>"        
            )
        client_connection.sendall(response.encode())
        client_connection.close()
except KeyboardInterrupt:
    print("\nShutting down the server...")
    server_socket.close()
        