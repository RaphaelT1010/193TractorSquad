import socket

def intepretData(command):
    print(command + " received")


def listenForRemoteController():
    host = ""
    port = 12345

    # Create a socket object
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    receiver_socket.bind((host, port))

    # Listen for incoming connections
    receiver_socket.listen(1)

    print("Receiver is listening...")

    # Accept a connection
    conn, addr = receiver_socket.accept()
    print(f"Connection from {addr}")

    while True:
        # Receive data
        data = conn.recv(1024).decode()
        if not data:
            break  # Exit the loop if no data is received or connection is closed
        intepretData(data)

# Close the connection and socket
    conn.close()
    receiver_socket.close()
    


if __name__ == "__main__":
    listenForRemoteController()