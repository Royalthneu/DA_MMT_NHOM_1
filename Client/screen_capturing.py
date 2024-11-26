import os
import platform
import tkinter as tk
from tkinter import messagebox
import uuid

def screen_capturing(client_socket):
    client_socket.sendall("SCREEN_CAPTURING".encode())

    try:
        image_size_bytes = client_socket.recv(4)
        if not image_size_bytes:
            print("No size information received. Exiting...")
            return
        
        image_size = int.from_bytes(image_size_bytes, byteorder='big')
        print(f"Expected image size: {image_size} bytes")
    except Exception as e:
        print(f"Failed to receive image size: {e}")
        input("Press Enter to exit...")
        return

    try:
        image_data = client_socket.recv(image_size)
        if image_size > 20000000:
            messagebox.showwarning("Warning", "Image size is too large. Exiting...")
            return
        
    except Exception as e:
        print(f"Error while receiving image data: {e}")
        input("Press Enter to exit...")
        return
    
    screenshot_filename = f"screenshot_{uuid.uuid4()}.png"

    if platform.system() == "Windows":
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', screenshot_filename)
    elif platform.system() == "Darwin":  # macOS
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop', screenshot_filename)
    else:  # Assuming Linux
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop', screenshot_filename)
    
    with open(desktop_path, 'wb') as img_file:
            img_file.write(image_data)

    messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {screenshot_filename} on Desktop.")

def screen_capture(client_socket):
    root = tk.Tk()
    root.title("Screen Capture")
    root.geometry("300x200")

    capture_btn = tk.Button(root, text="Capture Screen", command=lambda: screen_capturing(client_socket))
    capture_btn.pack(pady=10)

    quit_btn = tk.Button(root, text="Exit", command=root.quit)
    quit_btn.pack(pady=20)

    root.mainloop()
