import socket

def udp_server():
    # Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = "localhost"
    port = 9999
    server_socket.bind((host, port))
    server_socket.settimeout(3)  # Set timeout to catch KeyboardInterrupt

    print(f"UDP Server listening at {host}:{port}")

    try:
        while True:
            try:
                # Receiving data from the client
                data, addr = server_socket.recvfrom(1024)
                data = data.decode('utf-8')
                if not data:
                    continue  # Continue listening if no data is received
                print(f"Received from {addr}: {data}")

                # Calculate result using eval
                try:
                    # Evaluate the expression received
                    result = str(eval(data))  # eval is dangerous and not recommended for production
                except Exception as e:
                    result = f"Error!"

                # Sending result back to client
                server_socket.sendto(result.encode('utf-8'), addr)

            except socket.timeout:
                continue  # Continue in the loop and check for KeyboardInterrupt
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        # Close the server socket when the server is shutting down
        print("Socket closed.")
        server_socket.close()

if __name__ == "__main__":
    udp_server()
