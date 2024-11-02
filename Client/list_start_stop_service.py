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

def stop_service(client_socket):
    service_name = input("Nhập tên dịch vụ để dừng: ")
    client_socket.sendall(f"STOP {service_name}".encode())
    response = client_socket.recv(4096).decode()
    print(response)

def start_service(client_socket):
    service_name = input("Nhập tên dịch vụ để khởi động: ")
    client_socket.sendall(f"START {service_name}".encode())
    response = client_socket.recv(4096).decode()
    print(response)

def main_menu():
    print("\n--- SERVICE PROCESSING ---")
    print("1. List Services Running")
    print("2. Stop Service by Name")        
    print("3. Start Service")       
    print("0. Go Back to Main Menu")
        
    choice = input("Enter your choice: ")
    return choice

def list_start_stop_service(client_socket):    
        while True:
            choice = main_menu()
            if choice == '1':
                list_running_services(client_socket)
            elif choice == '2':
                stop_service(client_socket)
            elif choice == '3':
                start_service(client_socket)
            elif choice == '0':
                break
            else:
                print("Error choice. Try again.")


if __name__ == "__main__":    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))  # Địa chỉ IP và port của server
    list_start_stop_service(client_socket)
    client_socket.close()