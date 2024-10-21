import socket

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Use localhost or 127.0.0.1 as the host if server and client are on the same machine
    host = "127.0.0.1"
    port = 12345

    # Connect to the server
    client_socket.connect((host, port))

    while True:
        # Send a message to the server
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))
        if message.lower() == 'exit':
            print("Disconnected from the server.")
            break

        # Receive a response from the server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"ChatGPT: {response}")
        if response.lower() == 'exit':
            print("Server closed the connection.")
            break

    # Close the socket connection
    client_socket.close()

if __name__ == '__main__':
    start_client()
