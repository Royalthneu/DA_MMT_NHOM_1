import socket
import subprocess

def list_running_services():
    """Liệt kê tất cả các dịch vụ đang chạy."""
    try:
        # Chạy lệnh sc query để lấy danh sách dịch vụ
        output = subprocess.check_output("sc query", encoding='utf-8')
        
        # Lọc kết quả để chỉ hiển thị tên dịch vụ đang chạy
        running_services = []
        
        # Tạo một biến để theo dõi trạng thái
        is_running = False
        
        for line in output.splitlines():
            # Kiểm tra dòng tên dịch vụ
            if "SERVICE_NAME:" in line:
                service_name = line.split(":")[1].strip()  # Lấy tên dịch vụ
            elif "STATE" in line and "RUNNING" in line:
                is_running = True  # Đánh dấu rằng dịch vụ đang chạy
            
            # Nếu dịch vụ đang chạy, thêm vào danh sách
            if is_running and 'SERVICE_NAME:' in line:
                running_services.append(service_name)
                is_running = False  # Reset cho dịch vụ tiếp theo

        return "\n".join(running_services) if running_services else "No running services found."
        
    except subprocess.CalledProcessError as e:
        print(f"Error while fetching running services: {e}")
        return ""
    
def list_start_stop_service(client_socket):
    while True:
        print("\n--- SERVICE PROCESSING ---")
        print("1. List Services Running")
        print("2. Stop Service by Name")
        print("3. List Services Not Running")
        print("4. Start Service")       
        print("5. Go Back to Main Menu")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            # Liệt kê tất cả các dịch vụ đang chạy
            running_services = list_running_services()  # Gọi hàm để lấy danh sách dịch vụ
            if not running_services.strip():  # Kiểm tra nếu danh sách trống
                print("\nNo services are currently running.\n")
            else:
                print("\nServices Running:\n")
                print(running_services)  # In toàn bộ danh sách dịch vụ
        
        elif choice == '2':
            # Dừng dịch vụ theo tên
            service_name = input("Enter name of the service to stop: ")
            client_socket.sendall(f"STOP SERVICE {service_name}".encode())
            response = client_socket.recv(4096).decode()
            if "not found" in response.lower() or "already stopped" in response.lower():
                print(f"The service '{service_name}' is either not running or does not exist.")
            else:
                print(response)
        
        elif choice == '3':
            # Liệt kê các dịch vụ chưa chạy
            client_socket.sendall("LIST_SERVICE_NOT_RUNNING".encode())
            not_running_services = client_socket.recv(4096).decode()
            if not not_running_services.strip():  # Kiểm tra nếu danh sách trống
                print("\nAll allowed services are already running.\n")
            else:
                print("\nServices Not Running:\n", not_running_services)
        
        elif choice == '4':
            # Khởi chạy dịch vụ
            service_name = input("Enter the name of the service to start (e.g., wuauserv, bits): ")
            client_socket.sendall(f"START SERVICE {service_name}".encode())
            response = client_socket.recv(4096).decode()
            if "not allowed" in response.lower() or "not installed" in response.lower():
                print(f"The service '{service_name}' is either not installed or not allowed to start.")
            else:
                print(response)
        
        elif choice == '5':
            print("Going back to the main menu.")
            break

        else:
            print("Invalid choice. Please try again.")

# Khởi tạo socket và gọi hàm
if __name__ == "__main__":
    # Đây chỉ là ví dụ, bạn có thể thay đổi cách kết nối đến server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))  # Địa chỉ IP và port của server
    list_start_stop_service(client_socket)
    client_socket.close()
