import subprocess
import socket

# Danh sách các services được phép khởi chạy
allowed_services = {"wuauserv", "bits", "MpsSvc"}  # Thay thế với các services cụ thể mà bạn muốn

# Kiểm tra xem service có được phép khởi chạy không
def is_service_allowed(service_name):
    return service_name.lower() in allowed_services

# Liệt kê các services đang chạy
def list_running_services(client_socket):
    try:
        # Chạy lệnh sc query để lấy danh sách các services đang chạy
        output = subprocess.check_output("sc query state= running", encoding='utf-8')
        # Gửi toàn bộ đầu ra cho client
        client_socket.sendall(output.encode())
    except subprocess.CalledProcessError as e:
        error_msg = f"Error retrieving running services: {e}\n"
        client_socket.send(error_msg.encode())

# # Liệt kê các services chưa chạy
# def list_not_running_services(client_socket):
#     try:
#         # Lấy danh sách các service đang chạy
#         result = subprocess.run(["sc", "query"], capture_output=True, text=True)
#         running_services = result.stdout.lower()
        
#         # Tìm các services trong allowed_services nhưng chưa chạy
#         not_running_services = [service for service in allowed_services if service.lower() not in running_services]
#         not_running_list = "\n".join(not_running_services) + "\n"
        
#         # Gửi danh sách services chưa chạy về client
#         client_socket.sendall(not_running_list.encode())
#     except Exception as e:
#         error_msg = f"Error listing not running services: {e}\n"
#         client_socket.sendall(error_msg.encode())

# Khởi chạy một service
def start_service(client_socket, service_name):
    if not is_service_allowed(service_name):
        error_msg = "Service is not allowed to start.\n"
        client_socket.sendall(error_msg.encode())
        return

    try:
        # Khởi chạy service
        subprocess.run(["sc", "start", service_name], check=True)
        success_msg = f"Started service: {service_name}\n"
        client_socket.sendall(success_msg.encode())
    except Exception as e:
        error_msg = f"Error starting service: {e}\n"
        client_socket.sendall(error_msg.encode())

# Dừng một service dựa trên tên
def stop_service(client_socket, service_name):
    try:
        # Sử dụng lệnh sc để dừng service
        subprocess.run(["sc", "stop", service_name], check=True)
        success_msg = f"Stopped service: {service_name}\n"
        client_socket.sendall(success_msg.encode())
    except Exception as e:
        error_msg = f"Error stopping service: {service_name}: {e}\n"
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

            if command == "LIST_RUNNING":
                list_running_services(client_socket)
            # elif command == "LIST_NOT_RUNNING":
            #     list_not_running_services(client_socket)
            elif command.startswith("START"):
                service_name = command.split(" ", 1)[1]  # Lấy tên service từ lệnh
                start_service(client_socket, service_name)
            elif command.startswith("STOP"):
                service_name = command.split(" ", 1)[1]  # Lấy tên service từ lệnh
                stop_service(client_socket, service_name)
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
