import socket
import subprocess
import win32serviceutil
import win32service
import win32api

def list_running_services(client_socket):
    services = []
    try:
        # Liệt kê dịch vụ đang chạy
        result = subprocess.run(["sc", "query"], capture_output=True, text=True, check=True)
        services = result.stdout.splitlines()
        if not services:
            client_socket.sendall("Không có dịch vụ nào đang chạy.\n".encode())
        else:
            client_socket.sendall("\n".join(services).encode())
    except Exception as e:
        client_socket.sendall(f"Lỗi khi liệt kê dịch vụ: {e}\n".encode())

def start_service(client_socket, service_name):
    try:
        result = subprocess.run(["sc", "start", service_name], check=True, capture_output=True, text=True)
        if "START_PENDING" in result.stdout:
            success_msg = f"Dịch vụ '{service_name}' đang khởi động.\n"
        elif "NOT FOUND" in result.stdout:
            success_msg = f"Dịch vụ '{service_name}' không tìm thấy hoặc chưa được cài đặt.\n"
        elif "ACCESS DENIED" in result.stdout:
            success_msg = f"Dịch vụ '{service_name}' không được phép khởi động.\n"
        else:
            success_msg = f"Dịch vụ '{service_name}' đã khởi động.\n"
        client_socket.sendall(success_msg.encode())
    except subprocess.CalledProcessError as e:
        error_msg = f"Lỗi khi khởi động dịch vụ '{service_name}': {e}\n"
        client_socket.sendall(error_msg.encode())
    
def stop_service(client_socket, service_name):
    try:
        result = subprocess.run(["sc", "stop", service_name], check=True, capture_output=True, text=True)
        if "STOPPED" in result.stdout:
            success_msg = f"Dịch vụ '{service_name}' đã dừng.\n"
        elif "NOT FOUND" in result.stdout:
            success_msg = f"Dịch vụ '{service_name}' không tìm thấy hoặc chưa được cài đặt.\n"
        elif "ACCESS DENIED" in result.stdout:
            success_msg = f"Dịch vụ '{service_name}' không được phép dừng.\n"
        else:
            success_msg = f"Dịch vụ '{service_name}' đang chạy.\n"
        client_socket.sendall(success_msg.encode())
    except subprocess.CalledProcessError as e:
        error_msg = f"Lỗi khi dừng dịch vụ '{service_name}': {e}\n"
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
            command = client_socket.recv(1024).decode().strip()
            if command.startswith("LIST_SERVICES"):
                list_running_services(client_socket)
            elif command.startswith("STOP_SERVICE"):
                service_name = command.split(" ", 1)[1]
                stop_service(client_socket, service_name)
            elif command.startswith("START_SERVICE"):
                service_name = command.split(" ", 1)[1]
                start_service(client_socket, service_name)
            elif command == "EXIT":
                break
            else:
                client_socket.sendall("Lệnh không hợp lệ.\n".encode())
    finally:
        # Đóng kết nối
        client_socket.close()
        server_socket.close()
        print("Server stopped.")

# Chạy server
if __name__ == "__main__":
    start_server()
