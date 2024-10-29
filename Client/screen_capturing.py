import os
import uuid
import platform

def screen_capturing(client_socket):
    client_socket.sendall("SCREEN_CAPTURING".encode())

    try:
        # Receive the size of the incoming image
        image_size_bytes = client_socket.recv(4)
        if not image_size_bytes:
            print("No size information received. Exiting...")
            return
        
        image_size = int.from_bytes(image_size_bytes, byteorder='big')
        print(f"Expected image size: {image_size} bytes")
    except Exception as e:
        print(f"Failed to receive image size: {e}")
        input("Press any key to exit...")
        return

    # Directly receive the image data in one go
    try:
        image_data = client_socket.recv(image_size)
        if image_size > 200000: # neerly 200MB
            print("Image size is too large. Exiting...")
            input("Press any key to exit...")
            return
        
    except Exception as e:
        print(f"Error while receiving image data: {e}")
        input("Press any key to exit...")
        return

    # Save the image to the desktop
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
        print(f"Screenshot saved as {screenshot_filename}.")
    except Exception as e:
        print(f"Error saving screenshot: {e}")

    # Optional: Prompt the user to continue or exit
    user_input = input("Press any keys to return to the main menu: ").strip().lower()
    return  # Exit the function
