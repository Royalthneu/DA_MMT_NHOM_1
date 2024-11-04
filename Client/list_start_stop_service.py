import socket
from utils import clear_screen

def list_running_services(client_socket):
    client_socket.sendall("LIST_SERVICE_RUNNING".encode())
    response = client_socket.recv(4096).decode()
    print("Running Services:\n" + response)

def start_service(client_socket):
    service_name = input("Nhập tên dịch vụ để khởi động: ")
    client_socket.sendall(f"START_SERVICE {service_name}".encode())
    response = client_socket.recv(4096).decode()
    print(response)

def stop_service(client_socket):
    service_name = input("Nhập tên dịch vụ để dừng: ")
    client_socket.sendall(f"STOP_SERVICE {service_name}".encode())
    response = client_socket.recv(4096).decode()
    print(response)

def list_start_stop_service(client_socket):    
    clear_screen()
    while True:
        print("\n--- SERVICE PROCESSING ---")
        print("1. List Services Running")
        print("2. Stop Service by Name")        
        print("3. Start Service")       
        print("0. Go Back to Main Menu")
            
        choice = input("Enter your choice: ")
    
        if choice == '1':
            list_running_services(client_socket)
        elif choice == '2':
            list_running_services(client_socket)
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
