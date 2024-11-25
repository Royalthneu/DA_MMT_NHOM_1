import os
import socket
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from list_start_stop_app import list_app_running, stop_app_running_by_PID, start_app_byname
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def is_valid_ip_address(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def is_valid_port(port):
    return 0 < port <= 65535

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.client_socket = None
        self.server_ip = ""
        self.server_port = 0

        self.root.title("Client - Quản Lý Máy Chủ")
        self.root.geometry("500x700")

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

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10, fill="x") 

        self.ip_label = tk.Label(input_frame, text="IP Máy Chủ:", font=("Roboto", 14))
        self.ip_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")  

        self.ip_entry = tk.Entry(input_frame, font=("Roboto", 14))
        self.ip_entry.grid(row=0, column=1, padx=5, pady=3, sticky="ew")  
        self.ip_entry.grid_configure(ipady=5)

        self.port_label = tk.Label(input_frame, text="Cổng:", font=("Roboto", 14))
        self.port_label.grid(row=1, column=0, padx=5, pady=3, sticky="w")  

        self.port_entry = tk.Entry(input_frame, font=("Roboto", 14))
        self.port_entry.grid(row=1, column=1, padx=5, pady=3, sticky="ew")  
        self.port_entry.grid_configure(ipady=5)

        input_frame.grid_columnconfigure(0, weight=1)  
        input_frame.grid_columnconfigure(1, weight=2) 

        # Connect Server
        connect_button = tk.Frame(root, width=450, height=40)
        connect_button.pack_propagate(False) 
        connect_button.pack(pady=10)  

        self.connect_button = ttk.Button(
            connect_button, text="Connect Server", style="Rounded.TButton", command=self.connect_to_server
        )
        self.connect_button.pack(fill="both", expand=True)

        # Application Processing
        app_management_button = tk.Frame(root, width=450, height=40)
        app_management_button.pack_propagate(False) 
        app_management_button.pack(pady=10)  

        self.app_management_button = ttk.Button(
            app_management_button, text="Application Processing", style="Rounded.TButton", command=self.open_app_management_window
        )
        self.app_management_button.pack(fill="both", expand=True)

        # Service Processing
        service_management_button = tk.Frame(root, width=450, height=40)
        service_management_button.pack_propagate(False) 
        service_management_button.pack(pady=10) 

        self.service_management_button = ttk.Button(
            service_management_button, text="Service Processing", style="Rounded.TButton", command=self.open_service_management_window
        )
        self.service_management_button.pack(fill="both", expand=True)

        # Shutdown Server
        shutdown_button = tk.Frame(root, width=450, height=40)
        shutdown_button.pack_propagate(False) 
        shutdown_button.pack(pady=10)  

        self.shutdown_button = ttk.Button(
            shutdown_button, text="Shutdown Server", style="Rounded.TButton", command=self.shutdown_server_window
        )
        self.shutdown_button.pack(fill="both", expand=True)

        # Reset Server
        reset_button = tk.Frame(root, width=450, height=40)
        reset_button.pack_propagate(False) 
        reset_button.pack(pady=10)  

        self.reset_button = ttk.Button(
            reset_button, text="Reset Server", style="Rounded.TButton", command=self.shutdown_server_window
        )
        self.reset_button.pack(fill="both", expand=True)

        # Server Screen Processing
        screen_button = tk.Frame(root, width=450, height=40)
        screen_button.pack_propagate(False) 
        screen_button.pack(pady=10)  

        self.screen_button = ttk.Button(
            screen_button, text="Server Screen Processing", style="Rounded.TButton", command=self.shutdown_server_window
        )
        self.screen_button.pack(fill="both", expand=True)

         # Start Keylogger
        keylogger_button = tk.Frame(root, width=450, height=40)
        keylogger_button.pack_propagate(False) 
        keylogger_button.pack(pady=10)  

        self.keylogger_button = ttk.Button(
            keylogger_button, text="Start Keylogger", style="Rounded.TButton", command=self.shutdown_server_window
        )
        self.keylogger_button.pack(fill="both", expand=True)

         # Delete File from Server
        delete_file_button = tk.Frame(root, width=450, height=40)
        delete_file_button.pack_propagate(False) 
        delete_file_button.pack(pady=10)  

        self.delete_file_button = ttk.Button(
            delete_file_button, text="Delete File from Server", style="Rounded.TButton", command=self.shutdown_server_window
        )
        self.delete_file_button.pack(fill="both", expand=True)

        # Copy File from Server
        copy_file_button = tk.Frame(root, width=450, height=40)
        copy_file_button.pack_propagate(False) 
        copy_file_button.pack(pady=10)  

        self.copy_file_button = ttk.Button(
            copy_file_button, text="Copy File from Server", style="Rounded.TButton", command=self.shutdown_server_window
        )
        self.copy_file_button.pack(fill="both", expand=True)

    def connect_to_server(self):
        self.server_ip = self.ip_entry.get()
        try:
            self.server_port = int(self.port_entry.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Cổng phải là số nguyên.")
            return

        if not is_valid_ip_address(self.server_ip):
            messagebox.showerror("Lỗi", "Địa chỉ IP không hợp lệ.")
            return

        if not is_valid_port(self.server_port):
            messagebox.showerror("Lỗi", "Cổng không hợp lệ.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            messagebox.showinfo("Kết Nối Thành Công", "Đã kết nối đến máy chủ!")
        except socket.error as e:
            messagebox.showerror("Lỗi Kết Nối", f"Kết nối thất bại: {e}")
            self.client_socket = None

    def shutdown_server_window(self):
        app_window = tk.Toplevel(self.root)
        app_window.title("Quản lý Ứng Dụng")
        app_window.geometry("400x300")

        tk.Button(app_window, text="Danh Sách Ứng Dụng Đang Chạy", command=self.list_running_apps).pack(pady=5)
        tk.Button(app_window, text="Khởi Động Ứng Dụng", command=self.start_application).pack(pady=5)
        tk.Button(app_window, text="Dừng Ứng Dụng", command=self.stop_application).pack(pady=5)
    
    def open_app_management_window(self):
        app_window = tk.Toplevel(self.root)
        app_window.title("Quản lý Ứng Dụng")
        app_window.geometry("400x300")

        tk.Button(app_window, text="Danh Sách Ứng Dụng Đang Chạy", command=self.list_running_apps).pack(pady=5)
        tk.Button(app_window, text="Khởi Động Ứng Dụng", command=self.start_application).pack(pady=5)
        tk.Button(app_window, text="Dừng Ứng Dụng", command=self.stop_application).pack(pady=5)

    def open_service_management_window(self):
        app_window = tk.Toplevel(self.root)
        app_window.title("Quản lý Ứng Dụng")
        app_window.geometry("400x300")

        tk.Button(app_window, text="Danh Sách Ứng Dụng Đang Chạy", command=self.list_running_apps).pack(pady=5)
        tk.Button(app_window, text="Khởi Động Ứng Dụng", command=self.start_application).pack(pady=5)
        tk.Button(app_window, text="Dừng Ứng Dụng", command=self.stop_application).pack(pady=5)

    def list_running_apps(self):
        list_app_running(self.client_socket)
    def start_application(self):
        app_name = simpledialog.askstring("Khởi Động Ứng Dụng", "Nhập tên ứng dụng:")
        if app_name:
            start_app_byname(self.client_socket, app_name)

    def stop_application(self):
        pid = simpledialog.askinteger("Dừng Ứng Dụng", "Nhập PID của ứng dụng:")
        if pid:
            stop_app_running_by_PID(self.client_socket, pid)

class AutoReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(__file__):
            print("Detected change in script, restarting...")
            os.execv(sys.executable, ['python3'] + sys.argv)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)

    # Set up Watchdog for auto-reload
    observer = Observer()
    event_handler = AutoReloadHandler()
    observer.schedule(event_handler, os.path.dirname(os.path.abspath(__file__)), recursive=False)
    observer.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
