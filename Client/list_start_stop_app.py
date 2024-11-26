import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

def list_app_running(client_socket):
    client_socket.sendall("LIST_APP_RUNNING".encode())
    running_apps = client_socket.recv(65535).decode()
    if not running_apps.strip():
        messagebox.showinfo("Info", "All allowed applications are not running.")
    else:
        messagebox.showinfo("Applications Running", running_apps)

def stop_app_running_by_PID(client_socket):
    pid = simpledialog.askstring("Input", "Enter PID of the application to stop (e.g: 12345): ")
    if pid and pid.isdigit():
        client_socket.sendall(f"STOP_APP {pid}".encode())
        response = client_socket.recv(4096).decode()
        if "not found" in response.lower() or "already stopped" in response.lower():
            messagebox.showwarning("Warning", "The application is either not running or does not exist.")
        else:
            messagebox.showinfo("Info", response)
    else:
        messagebox.showerror("Error", "Invalid PID. Please enter a valid number.")

def start_app_byname(client_socket):
    app_name = simpledialog.askstring("Input", "Enter the name of the application to start (e.g: notepad.exe): ")
    if app_name:
        client_socket.sendall(f"START_APP_NAME {app_name}".encode())
        response = client_socket.recv(4096).decode()
        if "not allowed" in response.lower() or "not installed" in response.lower():
            messagebox.showwarning("Warning", f"The application '{app_name}' is either not installed or not allowed to start.")
        else:
            messagebox.showinfo("Info", response)

def start_app_bypath(client_socket):
    app_path = simpledialog.askstring("Input", "Enter the full path of the application to start (e.g., C:\\Windows\\System32\\notepad.exe): ")
    if app_path:
        client_socket.sendall(f"START_APP_PATH {app_path}".encode())
        response = client_socket.recv(4096).decode()
        if "not allowed" in response.lower() or "not found" in response.lower():
            messagebox.showwarning("Warning", f"The application at '{app_path}' is either not found or not allowed to start.")
        else:
            messagebox.showinfo("Info", response)

def list_start_stop_app(client_socket):
    root = tk.Tk()
    root.title("Application Manager")
    root.geometry("300x300")

    list_apps_btn = tk.Button(root, text="List Applications Running", command=lambda: list_app_running(client_socket))
    list_apps_btn.pack(pady=10)

    stop_app_btn = tk.Button(root, text="Stop Application by PID", command=lambda: stop_app_running_by_PID(client_socket))
    stop_app_btn.pack(pady=10)

    start_app_byname_btn = tk.Button(root, text="Start Application by Name", command=lambda: start_app_byname(client_socket))
    start_app_byname_btn.pack(pady=10)

    start_app_bypath_btn = tk.Button(root, text="Start Application by Path", command=lambda: start_app_bypath(client_socket))
    start_app_bypath_btn.pack(pady=10)

    quit_btn = tk.Button(root, text="Exit", command=root.quit)
    quit_btn.pack(pady=20)

    root.mainloop()
