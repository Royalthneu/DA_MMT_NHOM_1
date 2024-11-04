import pyautogui
import io

def screen_capturing(client_socket):
    # Capture the screen
    screenShort = pyautogui.screenshot()

    # Save screen short to the bytes buffer
    with io.BytesIO() as output:
        screenShort.save(output, format="PNG")
        image_data = output.getvalue()

    # Send the size of the image first
    image_size = len(image_data)
    client_socket.sendall(image_size.to_bytes(4, byteorder="big"))
    
    # Send image data
    client_socket.sendall(image_data)
    print("sent image_size: ", image_size)

