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

def start_app(client_socket):
    app_name = input("Enter the name of the application to start (e.g: notepad.exe): ")
    client_socket.sendall(f"START_APP {app_name}".encode())
    response = client_socket.recv(4096).decode()
    if "not allowed" in response.lower() or "not installed" in response.lower():
        print(f"The application '{app_name}' is either not installed or not allowed to start.")
    else:
        print(response)

def list_start_stop_app(client_socket):
    clear_screen()
    while True:
        print("\n--- APPLICATION PROCESSING ---")
        print("1. List Applications Running")
        print("2. Stop Application by PID")        
        print("3. Start Application")       
        print("0. Go Back to Main Menu")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            list_app_running(client_socket)        
        elif choice == '2':
            list_app_running(client_socket)
            stop_app_running_by_PID(client_socket)            
        elif choice == '3':
            start_app(client_socket)        
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
