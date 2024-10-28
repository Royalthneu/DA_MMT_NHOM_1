import socket
from Client.screen_capturing import screen_capturing
from Client.utils import clear_screen
from list_start_stop_app import list_start_stop_app
from list_start_stop_service import list_start_stop_service

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
        clear_screen()
        print("\n--- MAIN MENU ---")
        print("1. Application Processing")
        print("2. Service Processing")
        print("4. Server Screen Processing")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_start_stop_app(client_socket)
        if choice == '2':
            list_start_stop_service(client_socket)   
        if choice == '4':
            client_socket.sendall("SCREEN_CAPTURING".encode())
            screen_capturing(client_socket)   
        if choice == '5':
            client_socket.sendall("SCREEN_CAPTURING".encode())
            screen_capturing(client_socket)   
        elif choice == '6':
            client_socket.close()
            print("Disconnected from server.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
