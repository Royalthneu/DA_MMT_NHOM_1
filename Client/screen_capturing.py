import os
import platform
import uuid

def screen_capturing(client_socket):
    while True:
        # Receive the size of the incoming image
        image_size = int.from_bytes(client_socket.recv(4), byteorder='big')
        
        # Receive the image data
        image_data = b""
        while len(image_data) < image_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            image_data += packet

        # Save the image to the desktop
        screenshot_filename = f"screenshot_{uuid.uuid4()}.png"

        if platform.system() == "Windows":
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', screenshot_filename)
        elif platform.system() == "Darwin":  # macOS
            desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop', screenshot_filename)
        else:  # Assuming Linux
            desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop', screenshot_filename)

        with open(desktop_path, 'wb') as img_file:
            img_file.write(image_data)

        print(f"Screenshot saved as {screenshot_filename}.")
            
        # Prompt user to continue capturing or return to the main menu
        user_input = input("Press 'y' to continue capturing or any other key to return to the main menu: ").strip().lower()
        if user_input != 'y':
            break  # Exit the loop to return to the main menu
    