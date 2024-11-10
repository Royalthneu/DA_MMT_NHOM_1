import socket
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk  # Thêm dòng này
from delete_copy_paste import copy_file_from_server, delete_file_from_server
from shutdown_reset import reset_server, shutdown_server
from screen_capturing import screen_capturing
from list_start_stop_app import list_app_running, stop_app_running_by_PID, start_app_byname, start_app_bypath
from list_start_stop_service import list_start_stop_service
from key_logger import toggle_key_logger


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

        # Menu các chức năng
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=10)

        self.app_management_button = tk.Button(self.menu_frame, text="Quản lý Ứng Dụng", command=self.open_app_management_window)
        self.app_management_button.grid(row=0, column=0, pady=5)

        self.service_management_button = tk.Button(self.menu_frame, text="Quản lý Dịch Vụ", command=self.open_service_management_window)
        self.service_management_button.grid(row=1, column=0, pady=5)

        self.shutdown_button = tk.Button(self.menu_frame, text="Tắt Máy Chủ", command=self.shutdown_server_ui)
        self.shutdown_button.grid(row=2, column=0, pady=5)

        self.reset_button = tk.Button(self.menu_frame, text="Khởi Động Lại Máy Chủ", command=self.reset_server_ui)
        self.reset_button.grid(row=3, column=0, pady=5)

        self.screen_button = tk.Button(self.menu_frame, text="Xem Màn Hình Máy Chủ", command=self.open_screen_capturing)
        self.screen_button.grid(row=4, column=0, pady=5)

        self.keylogger_button = tk.Button(self.menu_frame, text="Bật/Tắt Keylogger", command=self.open_keylogger)
        self.keylogger_button.grid(row=5, column=0, pady=5)

        self.file_management_button = tk.Button(self.menu_frame, text="Quản lý Tệp", command=self.open_file_management_window)
        self.file_management_button.grid(row=6, column=0, pady=5)

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
        app_window.title("Quản lý Ứng Dụng")
        app_window.geometry("400x300")

        list_button = tk.Button(app_window, text="Danh Sách Ứng Dụng Đang Chạy", command=self.list_running_apps)
        list_button.pack(pady=5)

        start_button = tk.Button(app_window, text="Khởi Động Ứng Dụng", command=self.start_application)
        start_button.pack(pady=5)

        stop_button = tk.Button(app_window, text="Dừng Ứng Dụng", command=self.stop_application)
        stop_button.pack(pady=5)

    def list_running_apps(self):
        # Gửi yêu cầu danh sách ứng dụng đang chạy tới server
        self.client_socket.sendall("LIST_APP_RUNNING".encode())
        running_apps = self.client_socket.recv(65535).decode()

        # Tạo cửa sổ con để hiển thị bảng
        app_window = tk.Toplevel(self.root)
        app_window.title("Danh Sách Ứng Dụng Đang Chạy")
        app_window.geometry("600x400")

        # Tạo bảng Treeview
        tree = ttk.Treeview(app_window, columns=("PID", "Tên Ứng Dụng"), show="headings")
    
        # Định nghĩa tiêu đề cột
        tree.heading("PID", text="PID")
        tree.heading("Tên Ứng Dụng", text="Tên Ứng Dụng")

        # Cấu hình cột để dễ nhìn
        tree.column("PID", width=100, anchor="center")
        tree.column("Tên Ứng Dụng", width=400)

        # Thêm cuộn dọc cho bảng
        scrollbar = tk.Scrollbar(app_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(fill="both", expand=True)

        # Thêm các ứng dụng vào bảng
        if running_apps.strip():
            apps = running_apps.splitlines()
            for app in apps:
                # Kiểm tra nếu app có ít nhất 2 phần (PID và tên ứng dụng)
                parts = app.split(" ", 1)
                if len(parts) == 2:  # Nếu có đủ PID và tên ứng dụng
                    pid, app_name = parts
                    tree.insert("", "end", values=(pid, app_name))
                else:
                    # Nếu không thể tách, in thông báo hoặc xử lý theo cách khác
                    print(f"Không thể tách thông tin từ ứng dụng: {app}")
        else:
            messagebox.showinfo("Thông Báo", "Không có ứng dụng nào đang chạy.")



    def start_application(self):
        app_name = simpledialog.askstring("Khởi Động Ứng Dụng", "Nhập tên ứng dụng:")
        if app_name:
        # Gọi hàm với đúng số lượng tham số
            start_app_byname(self.client_socket, app_name)


    def stop_application(self):
        pid = simpledialog.askinteger("Dừng Ứng Dụng", "Nhập PID của ứng dụng:")
        if pid:
            stop_app_running_by_PID(self.client_socket, pid)

    def open_service_management_window(self):
        service_window = tk.Toplevel(self.root)
        service_window.title("Quản lý Dịch Vụ")
        service_window.geometry("400x300")

        list_button = tk.Button(service_window, text="Danh Sách Dịch Vụ Đang Chạy", command=self.list_running_services)
        list_button.pack(pady=5)

        start_button = tk.Button(service_window, text="Khởi Động Dịch Vụ", command=self.start_service)
        start_button.pack(pady=5)

        stop_button = tk.Button(service_window, text="Dừng Dịch Vụ", command=self.stop_service)
        stop_button.pack(pady=5)

    def list_running_services(self):
        list_start_stop_service(self.client_socket)

    def start_service(self):
        service_name = simpledialog.askstring("Khởi Động Dịch Vụ", "Nhập tên dịch vụ:")
        if service_name:
            start_service(self.client_socket, service_name)

    def stop_service(self):
        service_name = simpledialog.askstring("Dừng Dịch Vụ", "Nhập tên dịch vụ:")
        if service_name:
            stop_service(self.client_socket, service_name)

    def shutdown_server_ui(self):
        confirmation = messagebox.askyesno("Tắt Máy Chủ", "Bạn có chắc chắn muốn tắt máy chủ?")
        if confirmation:
            shutdown_server(self.client_socket)

    def reset_server_ui(self):
        confirmation = messagebox.askyesno("Khởi Động Lại Máy Chủ", "Bạn có chắc chắn muốn khởi động lại máy chủ?")
        if confirmation:
            reset_server(self.client_socket)

    def open_screen_capturing(self):
        screen_capturing(self.client_socket)

    def open_keylogger(self):
        toggle_key_logger(self.client_socket)

    def open_file_management_window(self):
        file_management_window = tk.Toplevel(self.root)
        file_management_window.title("Quản lý Tệp")
        file_management_window.geometry("400x200")

        delete_file_button = tk.Button(file_management_window, text="Xóa Tệp", command=self.delete_file_from_server_ui)
        delete_file_button.pack(pady=5)

        copy_file_button = tk.Button(file_management_window, text="Sao Chép Tệp", command=self.copy_file_from_server_ui)
        copy_file_button.pack(pady=5)

    def delete_file_from_server_ui(self):
        file_path = simpledialog.askstring("Xóa Tệp", "Nhập đường dẫn tệp cần xóa:")
        if file_path:
            delete_file_from_server(self.client_socket, file_path)

    def copy_file_from_server_ui(self):
        file_path = simpledialog.askstring("Sao Chép Tệp", "Nhập đường dẫn tệp cần sao chép:")
        if file_path:
            copy_file_from_server(self.client_socket, file_path)

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    client_app = ClientApp(root)
    root.mainloop()
import socket
import tkinter as tk
from tkinter import simpledialog, messagebox
from delete_copy_paste import copy_file_from_server, delete_file_from_server
from shutdown_reset import reset_server, shutdown_server
from screen_capturing import screen_capturing
from list_start_stop_app import list_app_running, stop_app_running_by_PID, start_app_byname, start_app_bypath
from list_start_stop_service import list_start_stop_service
from key_logger import toggle_key_logger

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

        # Menu các chức năng
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=10)

        self.app_management_button = tk.Button(self.menu_frame, text="Quản lý Ứng Dụng", command=self.open_app_management_window)
        self.app_management_button.grid(row=0, column=0, pady=5)

        self.service_management_button = tk.Button(self.menu_frame, text="Quản lý Dịch Vụ", command=self.open_service_management_window)
        self.service_management_button.grid(row=1, column=0, pady=5)

        self.shutdown_button = tk.Button(self.menu_frame, text="Tắt Máy Chủ", command=self.shutdown_server_ui)
        self.shutdown_button.grid(row=2, column=0, pady=5)

        self.reset_button = tk.Button(self.menu_frame, text="Khởi Động Lại Máy Chủ", command=self.reset_server_ui)
        self.reset_button.grid(row=3, column=0, pady=5)

        self.screen_button = tk.Button(self.menu_frame, text="Xem Màn Hình Máy Chủ", command=self.open_screen_capturing)
        self.screen_button.grid(row=4, column=0, pady=5)

        self.keylogger_button = tk.Button(self.menu_frame, text="Bật/Tắt Keylogger", command=self.open_keylogger)
        self.keylogger_button.grid(row=5, column=0, pady=5)

        self.file_management_button = tk.Button(self.menu_frame, text="Quản lý Tệp", command=self.open_file_management_window)
        self.file_management_button.grid(row=6, column=0, pady=5)

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
        app_window.title("Quản lý Ứng Dụng")
        app_window.geometry("400x300")

        list_button = tk.Button(app_window, text="Danh Sách Ứng Dụng Đang Chạy", command=self.list_running_apps)
        list_button.pack(pady=5)

        start_button = tk.Button(app_window, text="Khởi Động Ứng Dụng", command=self.start_application)
        start_button.pack(pady=5)

        stop_button = tk.Button(app_window, text="Dừng Ứng Dụng", command=self.stop_application)
        stop_button.pack(pady=5)

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

    def open_service_management_window(self):
        service_window = tk.Toplevel(self.root)
        service_window.title("Quản lý Dịch Vụ")
        service_window.geometry("400x300")

        list_button = tk.Button(service_window, text="Danh Sách Dịch Vụ Đang Chạy", command=self.list_running_services)
        list_button.pack(pady=5)

        start_button = tk.Button(service_window, text="Khởi Động Dịch Vụ", command=self.start_service)
        start_button.pack(pady=5)

        stop_button = tk.Button(service_window, text="Dừng Dịch Vụ", command=self.stop_service)
        stop_button.pack(pady=5)

    def list_running_services(self):
        list_start_stop_service(self.client_socket)

    def start_service(self):
        service_name = simpledialog.askstring("Khởi Động Dịch Vụ", "Nhập tên dịch vụ:")
        if service_name:
            start_service(self.client_socket, service_name)

    def stop_service(self):
        service_name = simpledialog.askstring("Dừng Dịch Vụ", "Nhập tên dịch vụ:")
        if service_name:
            stop_service(self.client_socket, service_name)

    def shutdown_server_ui(self):
        confirmation = messagebox.askyesno("Tắt Máy Chủ", "Bạn có chắc chắn muốn tắt máy chủ?")
        if confirmation:
            shutdown_server(self.client_socket)

    def reset_server_ui(self):
        confirmation = messagebox.askyesno("Khởi Động Lại Máy Chủ", "Bạn có chắc chắn muốn khởi động lại máy chủ?")
        if confirmation:
            reset_server(self.client_socket)

    def open_screen_capturing(self):
        screen_capturing(self.client_socket)

    def open_keylogger(self):
        toggle_key_logger(self.client_socket)

    def open_file_management_window(self):
        file_management_window = tk.Toplevel(self.root)
        file_management_window.title("Quản lý Tệp")
        file_management_window.geometry("400x200")

        delete_file_button = tk.Button(file_management_window, text="Xóa Tệp", command=self.delete_file_from_server_ui)
        delete_file_button.pack(pady=5)

        copy_file_button = tk.Button(file_management_window, text="Sao Chép Tệp", command=self.copy_file_from_server_ui)
        copy_file_button.pack(pady=5)

    def delete_file_from_server_ui(self):
        file_path = simpledialog.askstring("Xóa Tệp", "Nhập đường dẫn tệp cần xóa:")
        if file_path:
            delete_file_from_server(self.client_socket, file_path)

    def copy_file_from_server_ui(self):
        file_path = simpledialog.askstring("Sao Chép Tệp", "Nhập đường dẫn tệp cần sao chép:")
        if file_path:
            copy_file_from_server(self.client_socket, file_path)

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    client_app = ClientApp(root)
    root.mainloop()
