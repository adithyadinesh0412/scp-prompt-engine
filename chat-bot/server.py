import socket
from brain.chat_gpt import get_chatgpt_response  # Import the ChatGPT function

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    port = 12345

    # Bind the socket to a public host and a port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Waiting for a connection...")

    # Accept a connection
    client_socket, addr = server_socket.accept()
    print(f"Got a connection from {addr}")

    while True:
        # Receive message from client
        message = client_socket.recv(1024).decode('utf-8')
        if message.lower() == 'exit':
            print("Client disconnected.")
            break
        print(f"Client: {message}")

        # Get ChatGPT's response to the client's message
        chatgpt_response = get_chatgpt_response(message)
        print(f"ChatGPT: {chatgpt_response}")

        # Send ChatGPT's response to the client
        client_socket.send(chatgpt_response.encode('utf-8'))
        if chatgpt_response.lower() == 'exit':
            print("Server closed the connection.")
            break

    # Close the connection
    client_socket.close()

if __name__ == '__main__':
    start_server()
