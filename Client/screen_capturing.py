import os
import uuid
import platform
import tkinter as tk
from tkinter import messagebox

def screen_capturing(client_socket):
    # Create a hidden root window for messagebox
    root = tk.Tk()
    root.withdraw()

    try:
        # Request screen capture
        client_socket.sendall("SCREEN_CAPTURING".encode())

        # Receive the size of the incoming image
        image_size_bytes = client_socket.recv(4)
        if not image_size_bytes:
            messagebox.showerror("Error", "No size information received from the server.")
            return
        
        image_size = int.from_bytes(image_size_bytes, byteorder='big')
        print(f"Expected image size: {image_size} bytes")

        # Check if the image size exceeds a limit (e.g., 20MB)
        if image_size > 20000000:  # nearly 20MB
            messagebox.showerror("Error", "Image size is too large.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to receive image size: {e}")
        return

    # Receive the image data
    try:
        image_data = client_socket.recv(image_size)
        if not image_data or len(image_data) != image_size:
            messagebox.showerror("Error", "Incomplete image data received.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Error while receiving image data: {e}")
        return

    # Determine the desktop path and save the image
    screenshot_filename = f"screenshot_{uuid.uuid4()}.png"

    if platform.system() == "Windows":
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', screenshot_filename)
    elif platform.system() == "Darwin":  # macOS
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop', screenshot_filename)
    else:  # Assuming Linux
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop', screenshot_filename)

    try:
        with open(desktop_path, 'wb') as img_file:
            img_file.write(image_data)
        print(f"Screenshot saved as {screenshot_filename} on Desktop.")
        messagebox.showinfo("Success", f"Screenshot saved successfully as {screenshot_filename}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save screenshot: {e}")
