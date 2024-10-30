#list_start_stop_app.py
import socket
import subprocess
import platform
from utils import clear_screen

def list_start_stop_app(client_socket):
    clear_screen()
    while True:
        print("\n--- APPLICATION PROCESSING ---")
        print("1. List Applications Running")
        print("2. Stop Application by PID")
        # print("3. List Applications Not Running")
        print("4. Start Application")       
        print("5. Go Back to Main Menu")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            # Liệt kê tất cả các ứng dụng đang chạy
            client_socket.sendall("LIST_APP_RUNNING".encode())
            running_apps = client_socket.recv(65535).decode()
            if not running_apps.strip():  # Kiểm tra nếu danh sách trống
                print("\nAll allowed applications are not running.\n")
            else:
                print("\nApplications Running:\n", running_apps)
        
        elif choice == '2':
            # Dừng ứng dụng theo PID
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
        
        # elif choice == '3':
        #     # Liệt kê các ứng dụng chưa chạy
        #     client_socket.sendall("LIST_APP_NOT_RUNNING".encode())
        #     not_running_apps = client_socket.recv(4096).decode()
        #     if not not_running_apps.strip():  # Kiểm tra nếu danh sách trống
        #         print("\nAll allowed applications are already running.\n")
        #     else:
        #         print("\nApplications Not Running:\n", not_running_apps)
        
        elif choice == '4':
            # Khởi chạy ứng dụng
            app_name = input("Enter the name of the application to start (e.g: notepad.exe, calc.exe): ")
            client_socket.sendall(f"START_APP {app_name}".encode())
            response = client_socket.recv(4096).decode()
            if "not allowed" in response.lower() or "not installed" in response.lower():
                print(f"The application '{app_name}' is either not installed or not allowed to start.")
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
    client_socket.connect(('localhost', 12345))  # Địa chỉ IP và port của server
    list_start_stop_app(client_socket)
    client_socket.close()
