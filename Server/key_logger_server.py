import keyboard

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

def block_all_keys():
    # Danh sách các phím cần khóa
    
    
    # Khóa tất cả các phím trong danh sách normal_keys
    for key in normal_keys:
        keyboard.block_key(key)
        
    print("Bàn phím đã bị khóa. Nhấn 'Esc' để tắt chế độ bắt phím.")

def block_all_keys():
    # Khóa tất cả các phím trừ phím Esc để tắt chế độ bắt phím
    for key in keyboard.all_modifiers + normal_keys:
        keyboard.block_key(key)
    print("Bàn phím đã bị khóa. Nhấn 'Esc' để tắt chế độ bắt phím.")

def unblock_all_keys():
    # Mở khóa tất cả các phím từ danh sách normal_keys
    for key in normal_keys:
        keyboard.unblock_key(key)
    print("Bàn phím đã được mở khóa.")
