import socket
import tkinter as tk
from tkinter import messagebox

def shutdown_server(client_socket):
    client_socket.sendall("SHUTDOWN_SERVER".encode())
    response = client_socket.recv(1024).decode()
    messagebox.showinfo("Server Shutdown", response)

def reset_server(client_socket):
    client_socket.sendall("RESET_SERVER".encode())
    response = client_socket.recv(1024).decode()
    messagebox.showinfo("Server Reset", response)

def shutdown_reset(client_socket):
    root = tk.Tk()
    root.title("Server Shutdown/Reset")
    root.geometry("300x200")

    shutdown_btn = tk.Button(root, text="Shutdown Server", command=lambda: shutdown_server(client_socket))
    shutdown_btn.pack(pady=10)

    reset_btn = tk.Button(root, text="Reset Server", command=lambda: reset_server(client_socket))
    reset_btn.pack(pady=10)

    quit_btn = tk.Button(root, text="Exit", command=root.quit)
    quit_btn.pack(pady=20)

    root.mainloop()
