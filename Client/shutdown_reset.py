import socket

def shutdown_server(client_socket):
    client_socket.sendall("SHUTDOWN_SERVER".encode())
    response = client_socket.recv(1024).decode()
    print(response)

def reset_server(client_socket):
    client_socket.sendall("RESET_SERVER".encode())
    response = client_socket.recv(1024).decode()
    print(response)
