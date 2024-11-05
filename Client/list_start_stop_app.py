#list_start_stop_app.py
import socket
from utils import clear_screen

def list_app_running(client_socket):
    client_socket.sendall("LIST_APP_RUNNING".encode())
    running_apps = client_socket.recv(65535).decode()
    if not running_apps.strip():  # Kiểm tra nếu danh sách trống
        print("\nAll allowed applications are not running.\n")
    else:
        print("\nApplications Running:\n", running_apps)

def stop_app_running_by_PID(client_socket):
    pid = input("Enter PID of the application to stop (e.g: 12345): ")
    if pid.isdigit():  # Kiểm tra xem PID có phải là số không
        client_socket.sendall(f"STOP_APP {pid}".encode())
        response = client_socket.recv(4096).decode()
        if "not found" in response.lower() or "already stopped" in response.lower():
            print("The application is either not running or does not exist.")
        else:
            print(response)
    else:
        print("Invalid PID. Please enter a number.")

def start_app_byname(client_socket):
    app_name = input("Enter the name of the application to start (e.g: notepad.exe): ")
    client_socket.sendall(f"START_APP_NAME {app_name}".encode())
    response = client_socket.recv(4096).decode()
    if "not allowed" in response.lower() or "not installed" in response.lower():
        print(f"The application '{app_name}' is either not installed or not allowed to start.")
    else:
        print(response)
        
def start_app_bypath(client_socket):
    # Yêu cầu người dùng nhập đường dẫn đầy đủ đến file .exe
    app_path = input("Enter the full path of the application to start (e.g., C:\\Windows\\System32\\notepad.exe): ")
    
    # Gửi lệnh START_APP cùng với đường dẫn đầy đủ của ứng dụng đến server
    client_socket.sendall(f"START_APP_PATH {app_path}".encode())
    
    # Nhận phản hồi từ server
    response = client_socket.recv(4096).decode()
    if "not allowed" in response.lower() or "not found" in response.lower():
        print(f"The application at '{app_path}' is either not found or not allowed to start.")
    else:
        print(response) 


def list_start_stop_app(client_socket):
    clear_screen()
    while True:
        print("\n--- APPLICATION PROCESSING ---")
        print("1. List Applications Running")
        print("2. Stop Application by PID")        
        print("3. Start Application by Name") 
        print("4. Start Application by Path")        
        print("0. Go Back to Main Menu")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            list_app_running(client_socket)        
        elif choice == '2':
            list_app_running(client_socket)
            stop_app_running_by_PID(client_socket)            
        elif choice == '3':
            start_app_byname(client_socket) 
        elif choice == '4':
            start_app_bypath(client_socket)         
        elif choice == '0':
            print("Going back to the main menu.")
            break
        else:
            print("Invalid choice. Please try again.")

# Khởi tạo socket và gọi hàm
if __name__ == "__main__":    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))  # Địa chỉ IP và port của server
    list_start_stop_app(client_socket)
    client_socket.close()
