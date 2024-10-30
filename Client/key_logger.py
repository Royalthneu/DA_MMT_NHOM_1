import socket

def receive_key_loggers(client_socket):
    """Nhận và ghi lại các phím được nhấn."""
    while True:
        data = client_socket.recv(1024).decode()  # Nhận dữ liệu từ server
        if not data:  # Kiểm tra nếu không còn dữ liệu
            break
        print(f"Received keys: {data}")  # In ra các phím đã nhận

# Đặt danh sách các phím hợp lệ
normal_keys = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'space', 'enter', 'tab', 'backspace', 'shift',
    'ctrl', 'alt', 'esc', 'capslock', 'numlock',
    'left', 'right', 'up', 'down', 'home', 'end',
    'page up', 'page down', 'insert', 'delete'
]
