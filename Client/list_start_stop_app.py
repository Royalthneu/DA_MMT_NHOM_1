import socket
import tkinter as tk
from tkinter import simpledialog, messagebox
from utils import clear_screen

def list_app_running(client_socket):
    client_socket.sendall("LIST_APP_RUNNING".encode())
    running_apps = client_socket.recv(65535).decode()
    if not running_apps.strip():  # Kiểm tra nếu danh sách trống
        messagebox.showinfo("Thông báo", "Không có ứng dụng nào đang chạy.")
    else:
        messagebox.showinfo("Ứng Dụng Đang Chạy", f"Ứng dụng đang chạy:\n{running_apps}")

def stop_app_running_by_PID(client_socket):
    pid = simpledialog.askstring("Dừng Ứng Dụng", "Nhập PID của ứng dụng muốn dừng:")
    if pid and pid.isdigit():  # Kiểm tra xem PID có phải là số không
        client_socket.sendall(f"STOP_APP {pid}".encode())
        response = client_socket.recv(4096).decode()
        if "not found" in response.lower() or "already stopped" in response.lower():
            messagebox.showerror("Lỗi", "Ứng dụng không tồn tại hoặc đã dừng.")
        else:
            messagebox.showinfo("Thông báo", response)
    else:
        messagebox.showerror("Lỗi", "PID không hợp lệ. Vui lòng nhập số.")

def start_app_byname(client_socket, app_name):
    app_name = simpledialog.askstring("Khởi Động Ứng Dụng", "Nhập tên ứng dụng muốn khởi động (ví dụ: notepad.exe):")
    if app_name:
        client_socket.sendall(f"START_APP_NAME {app_name}".encode())
        response = client_socket.recv(4096).decode()
        if "not allowed" in response.lower() or "not installed" in response.lower():
            messagebox.showerror("Lỗi", f"Ứng dụng '{app_name}' không được phép khởi động hoặc không cài đặt.")
        else:
            messagebox.showinfo("Thông báo", response)

def start_app_bypath(client_socket):
    app_path = simpledialog.askstring("Khởi Động Ứng Dụng", "Nhập đường dẫn đầy đủ đến ứng dụng (ví dụ: C:\\Windows\\System32\\notepad.exe):")
    if app_path:
        client_socket.sendall(f"START_APP_PATH {app_path}".encode())
        response = client_socket.recv(4096).decode()
        if "not allowed" in response.lower() or "not found" in response.lower():
            messagebox.showerror("Lỗi", f"Ứng dụng tại '{app_path}' không tìm thấy hoặc không được phép khởi động.")
        else:
            messagebox.showinfo("Thông báo", response)

class AppManagementWindow:
    def __init__(self, root, client_socket):
        self.root = root
        self.client_socket = client_socket
        self.root.title("Quản lý Ứng Dụng")
        self.root.geometry("400x300")

        # Các nút bấm để xử lý các chức năng
        self.list_button = tk.Button(self.root, text="Danh Sách Ứng Dụng Đang Chạy", command=self.list_app_running)
        self.list_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Dừng Ứng Dụng theo PID", command=self.stop_app_running_by_PID)
        self.stop_button.pack(pady=5)

        self.start_button_byname = tk.Button(self.root, text="Khởi Động Ứng Dụng theo Tên", command=self.start_app_byname)
        self.start_button_byname.pack(pady=5)

        self.start_button_bypath = tk.Button(self.root, text="Khởi Động Ứng Dụng theo Đường Dẫn", command=self.start_app_bypath)
        self.start_button_bypath.pack(pady=5)

    def list_app_running(self):
        list_app_running(self.client_socket)

    def stop_app_running_by_PID(self):
        stop_app_running_by_PID(self.client_socket)

    def start_app_byname(self):
        start_app_byname(self.client_socket)

    def start_app_bypath(self):
        start_app_bypath(self.client_socket)

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.client_socket = None
        self.server_ip = ""
        self.server_port = 0

        self.root.title("Client - Quản Lý Máy Chủ")
        self.root.geometry("400x500")

        # Giao diện nhập IP và Cổng
        self.ip_label = tk.Label(root, text="IP Máy Chủ:")
        self.ip_label.pack(pady=5)
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack(pady=5)

        self.port_label = tk.Label(root, text="Cổng:")
        self.port_label.pack(pady=5)
        self.port_entry = tk.Entry(root)
        self.port_entry.pack(pady=5)

        self.connect_button = tk.Button(root, text="Kết Nối", command=self.connect_to_server)
        self.connect_button.pack(pady=10)

        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=10)

        self.app_management_button = tk.Button(self.menu_frame, text="Quản lý Ứng Dụng", command=self.open_app_management_window)
        self.app_management_button.grid(row=0, column=0, pady=5)

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
            self.client_socket.close()

    def open_app_management_window(self):
        app_window = tk.Toplevel(self.root)
        app_management = AppManagementWindow(app_window, self.client_socket)

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    client_app = ClientApp(root)
    root.mainloop()
