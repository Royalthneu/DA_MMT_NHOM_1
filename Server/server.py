import socket
import threading
import subprocess
from screen_capturing_server import screen_capturing
from list_start_stop_app_server import list_running_applications, list_not_running_applications, start_application, stop_application
from list_start_stop_service_server import list_not_running_services, list_running_services, start_service, stop_service

PORT = 8080
BUFFER_SIZE = 1024

def handle_client(client_socket):
    """Xử lý các lệnh từ client."""
    try:
        while True:
            buffer = client_socket.recv(BUFFER_SIZE).decode()
            if not buffer:
                print("Client disconnected or error occurred.")
                break
            print(f"Received command: {buffer}")
            #Yêu cầu 1. xử lý APP
            if buffer.startswith("LIST_APP_RUNNING"):
                list_running_applications(client_socket)
            elif buffer.startswith("LIST_APP_NOT_RUNNING"):
                list_not_running_applications(client_socket)
            elif buffer.startswith("START_APP"):
                app_name = buffer.split()[1]
                start_application(client_socket, app_name)
            elif buffer.startswith("SCREEN_CAPTURING"):
                screen_capturing(client_socket)
            elif buffer.startswith("STOP_APP"):
                pid = int(buffer.split()[1])
                stop_application(client_socket, pid)
                
                
            # Yêu cầu 2. xử lý SERVICES    
            elif buffer.startswith("LIST_SERVICE_RUNNING"):
                list_running_services(client_socket)
            elif buffer.startswith("LIST_SERVICE_NOT_RUNNING"):
                list_not_running_services(client_socket)
            elif buffer.startswith("START_SERVICE"):
                service_name = buffer.split()[1]
                start_service(client_socket, service_name)
            elif buffer.startswith("STOP_SERVICE"):
                service_name = buffer.split()[1]
                stop_service(client_socket, service_name)                
                
                
            elif buffer.startswith("GO BACK MENU LIST"):
                print("Client requested to return to menu.")                
                break
            else:
                print("Unknown command received.")

            client_socket.sendall("Command received".encode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Client connection closed.")

def main():
    # Hỏi người dùng xác nhận mở cổng 8080
    response = input("Do you want to open port 8080? (y/n): ")
    if response.lower() != 'y':
        print("Port 8080 will not be opened. Exiting program.")
        return

    # Tạo socket và bind với địa chỉ IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(3)

    # Lấy địa chỉ IP của máy chủ
    host_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server is listening on {host_ip}:{PORT}")

    try:
        while True:
            # Chấp nhận kết nối từ client
            client_socket, addr = server_socket.accept()
            print(f"Client connected from {addr}")

            # Tạo một thread mới để xử lý client
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        server_socket.close()
        print("Server stopped.")

if __name__ == "__main__":
    main()
