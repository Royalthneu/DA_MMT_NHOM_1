import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

def list_running_services(client_socket):
    client_socket.sendall("LIST_SERVICE_RUNNING".encode())
    response = client_socket.recv(4096).decode()
    messagebox.showinfo("Running Services", response)

def start_service(client_socket):
    service_name = simpledialog.askstring("Input", "Enter the name of the service to start: ")
    if service_name:
        client_socket.sendall(f"START_SERVICE {service_name}".encode())
        response = client_socket.recv(4096).decode()
        messagebox.showinfo("Info", response)

def stop_service(client_socket):
    service_name = simpledialog.askstring("Input", "Enter the name of the service to stop: ")
    if service_name:
        client_socket.sendall(f"STOP_SERVICE {service_name}".encode())
        response = client_socket.recv(4096).decode()
        messagebox.showinfo("Info", response)

def list_start_stop_service(client_socket):
    root = tk.Tk()
    root.title("Service Manager")
    root.geometry("300x300")

    list_services_btn = tk.Button(root, text="List Running Services", command=lambda: list_running_services(client_socket))
    list_services_btn.pack(pady=10)

    stop_service_btn = tk.Button(root, text="Stop Service by Name", command=lambda: stop_service(client_socket))
    stop_service_btn.pack(pady=10)

    start_service_btn = tk.Button(root, text="Start Service", command=lambda: start_service(client_socket))
    start_service_btn.pack(pady=10)

    quit_btn = tk.Button(root, text="Exit", command=root.quit)
    quit_btn.pack(pady=20)

    root.mainloop()
