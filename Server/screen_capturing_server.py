import pyautogui
import io
from PIL import Image

def screen_capturing(client_socket):
    # Capture the screen
    screenShort = pyautogui.screenshot()

    # Save screen short to the bytes buffer
    with io.BytesIO() as output:
        screenShort.save(output, format="PNG")
        image_data = output.getvalue()

    # Send the size of the image first
    client_socket.sendall(len(image_data).to_bytes(4, byteorder="big"))
    # Send image data
    client_socket.sendall(image_data)

