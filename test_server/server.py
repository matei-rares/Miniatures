import socket


def get_local_ip():
    """
    Get the local IP address of the computer.
    """
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to a known address, this triggers a local IP to be assigned
        s.connect(("8.8.8.8", 80))

        # Get the socket's local address which should be the local IP
        local_ip = s.getsockname()[0]

        # Close the socket
        s.close()

        return local_ip
    except Exception as e:
        print("Error getting local IP:", e)
        return None


def start_server(host, port):
    """
    Start a server that listens for incoming connections.
    """
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the host and port
        server_socket.bind((host, port))

        # Listen for incoming connections
        server_socket.listen(1)

        print(f"Server listening on {host}:{port}")

        while True:
            # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            while True:
                print(f"Connection from {client_address}")

                data = client_socket.recv(1024)
                print(f"Received data: {data.decode()}")

                response = "Message received!"
                client_socket.sendall(response.encode())


    except Exception as e:
        print("Error starting server:", e)
    finally:
        # Close the server socket
        server_socket.close()


if __name__ == "__main__":
    # Get local IP dynamically
    local_ip = get_local_ip()
    if not local_ip:
        print("Failed to retrieve local IP address. Exiting.")
        exit()
    print(local_ip)
    # Define host and port
    host = local_ip  # Use local IP dynamically obtained
    port = 12345  # Choose a port

    # Start the server
    start_server(host, port)
