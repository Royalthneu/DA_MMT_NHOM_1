import socket
import subprocess

def list_running_services(client_socket):
    try:
        # Dùng PowerShell để liệt kê các dịch vụ đang chạy
        output = subprocess.check_output(
            ["powershell", "-Command", "Get-Service | Where-Object { $_.Status -eq 'Running' } | Format-Table -HideTableHeaders -Property Name,DisplayName"],
            encoding='utf-8'
        )
        client_socket.sendall(output.encode())  # Gửi danh sách dịch vụ đang chạy tới client
    except subprocess.CalledProcessError as e:
        error_msg = f"Error retrieving running services: {e}\n"
        client_socket.sendall(error_msg.encode())

def start_service(client_socket, service_name):
    try:
        # Sử dụng PowerShell để khởi động dịch vụ với quyền admin
        result = subprocess.run(
            ["powershell", "-Command", f"Start-Process sc.exe -ArgumentList 'start', '{service_name}' -Verb runAs"],
            check=True, capture_output=True, text=True
        )
        
        # Gửi thông báo thành công
        success_msg = f"Dịch vụ '{service_name}' đã được yêu cầu khởi động.\n"
        client_socket.sendall(success_msg.encode())
    except subprocess.CalledProcessError as e:
        # Gửi lỗi chi tiết tới client nếu có vấn đề xảy ra
        error_msg = f"Lỗi khi khởi động dịch vụ '{service_name}': {e.stderr}\n"
        client_socket.sendall(error_msg.encode())


def stop_service(client_socket, service_name):
    try:
        # Sử dụng PowerShell để dừng dịch vụ với quyền admin
        result = subprocess.run(
            ["powershell", "-Command", f"Start-Process sc.exe -ArgumentList 'stop', '{service_name}' -Verb runAs"],
            check=True, capture_output=True, text=True
        )
        
        # Kiểm tra nếu lệnh thành công
        success_msg = f"Dịch vụ '{service_name}' đã được yêu cầu dừng.\n"
        client_socket.sendall(success_msg.encode())
    except subprocess.CalledProcessError as e:
        # Gửi lỗi chi tiết tới client nếu có vấn đề xảy ra
        error_msg = f"Lỗi khi dừng dịch vụ '{service_name}': {e.stderr}\n"
        client_socket.sendall(error_msg.encode())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(1)
    print("Server đang lắng nghe kết nối...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Đã kết nối với {client_address}")

        try:
            while True:
                command = client_socket.recv(1024).decode().strip()
                
                if command == "LIST_SERVICE_RUNNING":
                    list_running_services(client_socket)
                elif command.startswith("START_SERVICE"):
                    service_name = command.split(" ", 1)[1]
                    start_service(client_socket, service_name)
                elif command.startswith("STOP_SERVICE"):
                    service_name = command.split(" ", 1)[1]
                    stop_service(client_socket, service_name)
                elif command == "EXIT":
                    break
                else:
                    client_socket.sendall("Lệnh không hợp lệ.\n".encode())
        finally:
            client_socket.close()
            print("Kết nối với client đã đóng.")

if __name__ == "__main__":
    start_server()
