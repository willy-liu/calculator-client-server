import socket

def tcp_server():
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = 9999
    server_socket.bind((host, port))
    server_socket.settimeout(3)

    # Start listening to requests
    server_socket.listen(5)
    print(f"TCP Server listening at {host}:{port}")

    try:
        while True:
            # Handling client connection
            try:
                client_socket, addr = server_socket.accept()
                print(f"Got a connection from {addr}")
            except socket.timeout:
                continue
            # Handle each client in a loop
            while True:
                # Receiving data from the client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    # if data is not received, break the inner loop to wait for another client
                    break
                print(f"from connected user: {data}")

                # Calculate result using eval
                try:
                    # Evaluate the expression received
                    result = str(eval(data))  # eval is dangerous and not recommended for production
                except Exception as e:
                    result = f"Error!"

                # Sending result back to client
                client_socket.send(result.encode('utf-8'))

            # Close the connection with the current client
            client_socket.close()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        # Close the server socket when the server is shutting down
        print("socket closed.")
        server_socket.close()

if __name__ == "__main__":
    tcp_server()
