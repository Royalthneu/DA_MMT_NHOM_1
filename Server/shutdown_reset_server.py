import subprocess
import platform

def shutdown_server(client_socket):
    try:
        if platform.system() == "Windows":
            subprocess.call("shutdown /s /t 1", shell=True)
        else:
            subprocess.call("shutdown now", shell=True)
        client_socket.sendall("Server is shutting down...".encode())
    except Exception as e:
        client_socket.sendall(f"Failed to shutdown server: {e}".encode())

def reset_server(client_socket):
    try:
        if platform.system() == "Windows":
            subprocess.call("shutdown /r /t 1", shell=True)
        else:
            subprocess.call("reboot", shell=True)
        client_socket.sendall("Server is rebooting...".encode())
    except Exception as e:
        client_socket.sendall(f"Failed to reboot server: {e}".encode())
