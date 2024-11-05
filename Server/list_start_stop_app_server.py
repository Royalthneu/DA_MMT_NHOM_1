#list_start_stop_app_server.py
import os
import platform
import subprocess
import socket

# # Danh sách các ứng dụng được phép khởi chạy
# allowed_applications = {"notepad.exe", "calc.exe"}

# # Kiểm tra xem ứng dụng có được phép khởi chạy không
# def is_application_allowed(app_name):
#     return app_name.lower() in allowed_applications

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

# Khởi chạy một ứng dụng
def start_application_byname(client_socket, app_name):
    try:
        # Khởi chạy ứng dụng
        subprocess.Popen([app_name])
        success_msg = f"Started application: {app_name}\n"
        client_socket.sendall(success_msg.encode())
    except Exception as e:
        error_msg = f"Error starting application: {e}\n"
        client_socket.sendall(error_msg.encode())

def start_application_bypath(client_socket, app_path):
    # Kiểm tra đường dẫn có hợp lệ không
    if not os.path.isfile(app_path):
        error_msg = f"Error: Application '{app_path}' not found or path is invalid.\n"
        client_socket.sendall(error_msg.encode())
        return    
    try:
        # Khởi chạy ứng dụng bằng subprocess với đường dẫn đầy đủ
        subprocess.Popen([app_path], shell=True)
        success_msg = f"Started application: {app_path}\n"
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
            elif command.startswith("START_APP_NAME"):
                app_name = command.split(" ", 1)[1]  # Lấy tên ứng dụng từ lệnh
                start_application_byname(client_socket, app_name)
            elif command.startswith("START_APP_PATH"):
                app_path = command.split(" ", 1)[1]  # Lấy đường dẫn ứng dụng
                if '\\\\' in app_path:
                    app_path = app_path.replace("\\\\", "\\")  # Thay thế '\\' thành '\'                
                start_application_bypath(client_socket, app_path)            
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
