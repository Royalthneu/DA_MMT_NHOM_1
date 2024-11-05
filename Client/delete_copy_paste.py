import socket
import os

def replace_path(file_path):
    if '\\\\' in file_path:
         file_path = file_path.replace("\\\\", "\\")  # Thay thế '\\' thành '\'


def delete_file_from_server(client_socket, file_path):
    replace_path(file_path)
    client_socket.sendall(f"DELETE_FILE {file_path}".encode())
    response = client_socket.recv(1024).decode()
    print(response)

def copy_file_from_server(client_socket):
    # Nhập đường dẫn file từ server
    file_path = input("Enter the full file path on the server to copy: ").strip()
    replace_path(file_path)
    
    # Yêu cầu người dùng nhập vị trí dán file
    destination_folder = input("Enter the destination folder path on client to save the file: ").strip()
    replace_path(file_path)
    
    # Kiểm tra nếu thư mục tồn tại
    if not os.path.exists(destination_folder):
        print("The specified folder does not exist. Please check the path.")
        return

    # Tạo tên file dựa trên đường dẫn từ server
    filename = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, filename)
    
    # Gửi yêu cầu copy file đến server với đường dẫn file đầy đủ
    client_socket.sendall(f"COPY_FILE {file_path}".encode())
    
    # Nhận kích thước file
    file_size = int.from_bytes(client_socket.recv(4), byteorder='big')

    if file_size > 0:
        with open(destination_path, 'wb') as f:
            data_received = 0
            while data_received < file_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                f.write(packet)
                data_received += len(packet)
        print(f"File has been copied from server to {destination_path}.")
    else:
        print("File not found on server.")
