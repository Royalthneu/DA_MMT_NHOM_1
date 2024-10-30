#list_start_stop_app_server.py
import platform
import subprocess
import socket

# Danh sách các ứng dụng được phép khởi chạy
allowed_applications = {"notepad.exe", "calc.exe", "clock.exe", "calendar.exe"}

# Kiểm tra xem ứng dụng có được phép khởi chạy không
def is_application_allowed(app_name):
    return app_name.lower() in allowed_applications

# Liệt kê các tiến trình đang chạy
def list_running_applications(client_socket):
    try:
        print("platform.system():", platform.system())  # Kiểm tra hệ điều hành
        if platform.system() == "Windows":
            # Trên Windows
            output = subprocess.check_output("tasklist", encoding='utf-8')
        else:
            # Trên macOS và Linux
            output = subprocess.check_output("ps aux", shell=True, encoding='utf-8')
        
        # Gửi danh sách ứng dụng đang chạy về client
        client_socket.sendall(output.encode('utf-8'))    
    
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        client_socket.sendall(error_msg.encode('utf-8'))        

# Liệt kê các ứng dụng chưa chạy
def list_not_running_applications(client_socket):
    try:
        # Lấy danh sách tiến trình đang chạy
        result = subprocess.run(["tasklist"], capture_output=True, text=True)
        running_apps = result.stdout.lower()
        
        # Tìm các ứng dụng trong allowed_applications nhưng chưa chạy
        not_running_apps = [app for app in allowed_applications if app.lower() not in running_apps]
        not_running_list = "\n".join(not_running_apps) + "\n"
        
        # Gửi danh sách ứng dụng chưa chạy về client
        client_socket.sendall(not_running_list.encode())
    except Exception as e:
        error_msg = f"Error listing not running applications: {e}\n"
        client_socket.sendall(error_msg.encode())

# Khởi chạy một ứng dụng
def start_application(client_socket, app_name):
    if not is_application_allowed(app_name):
        error_msg = "Application is not allowed to start.\n"
        client_socket.sendall(error_msg.encode())
        return

    try:
        # Khởi chạy ứng dụng
        subprocess.Popen([app_name])
        success_msg = f"Started application: {app_name}\n"
        client_socket.sendall(success_msg.encode())
    except Exception as e:
        error_msg = f"Error starting application: {e}\n"
        client_socket.sendall(error_msg.encode())

# Dừng một ứng dụng dựa trên PID
def stop_application(client_socket, pid):
    try:
        # Sử dụng lệnh taskkill để dừng ứng dụng
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
        success_msg = f"Stopped application with PID {pid}\n"
        client_socket.sendall(success_msg.encode())
    except Exception as e:
        error_msg = f"Error stopping application with PID {pid}: {e}\n"
        client_socket.sendall(error_msg.encode())

# Hàm chính để khởi chạy server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(1)

    # Lấy địa chỉ IP thật và cổng của server
    ip_address = socket.gethostbyname(socket.gethostname())
    port = 8080

    print(f"Server is listening on {ip_address}:{port}...")

    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    try:
        while True:
            # Nhận lệnh từ client
            command = client_socket.recv(1024).decode().strip()

            if command == "LIST_APP_RUNNING":
                list_running_applications(client_socket)
            elif command == "LIST_APP_NOT_RUNNING":
                list_not_running_applications(client_socket)
            elif command.startswith("START"):
                app_name = command.split(" ", 1)[1]  # Lấy tên ứng dụng từ lệnh
                start_application(client_socket, app_name)
            elif command.startswith("STOP"):
                pid = int(command.split(" ", 1)[1])  # Lấy PID từ lệnh
                stop_application(client_socket, pid)
            elif command == "EXIT":
                print("Client requested to exit.")
                break
            else:
                error_msg = "Unknown command.\n"
                client_socket.sendall(error_msg.encode())
    finally:
        # Đóng kết nối
        client_socket.close()
        server_socket.close()
        print("Server stopped.")

# Chạy server
if __name__ == "__main__":
    start_server()
