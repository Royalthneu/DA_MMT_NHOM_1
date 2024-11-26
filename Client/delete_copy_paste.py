import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def replace_path(file_path):
    if '\\\\' in file_path:
         file_path = file_path.replace("\\\\", "\\")  # Thay thế '\\' thành '\'


def delete_file_from_server(client_socket, file_path):
    replace_path(file_path)
    client_socket.sendall(f"DELETE_FILE {file_path}".encode())
    response = client_socket.recv(1024).decode()
    print(response)

def copy_file_from_server(client_socket):
    """
    GUI function to copy a file from the server to a selected local folder.
    """
    def select_folder():
        """Opens a dialog to select the destination folder."""
        folder = filedialog.askdirectory(title="Select the destination folder")
        if folder:
            destination_folder.set(folder)

    def copy_file():
        """Performs the file copy operation."""
        file_path = file_path_entry.get().strip()
        folder = destination_folder.get()

        if not file_path:
            messagebox.showerror("Error", "Please enter the server file path.")
            return

        if not folder:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        if not os.path.exists(folder):
            messagebox.showerror("Error", "The specified folder does not exist.")
            return

        # Determine the destination file path
        filename = os.path.basename(file_path)
        destination_path = os.path.join(folder, filename)

        try:
            # Send copy file request to the server
            client_socket.sendall(f"COPY_FILE {file_path}".encode())

            # Receive file size
            file_size_data = client_socket.recv(4)
            if not file_size_data:
                messagebox.showerror("Error", "Failed to receive file size from the server.")
                return
            file_size = int.from_bytes(file_size_data, byteorder='big')

            if file_size == 0:
                # Create an empty file if size is 0
                with open(destination_path, 'wb') as f:
                    pass
                messagebox.showinfo("File Copy", f"An empty file has been created at {destination_path}.")
            else:
                # Copy file content
                with open(destination_path, 'wb') as f:
                    data_received = 0
                    while data_received < file_size:
                        packet = client_socket.recv(4096)
                        if not packet:
                            messagebox.showerror("Error", "Connection lost while receiving file data.")
                            return
                        f.write(packet)
                        data_received += len(packet)
                messagebox.showinfo("File Copy", f"File has been successfully copied to {destination_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during file copy: {e}")

    # Create the main Tkinter window
    window = tk.Tk()
    window.title("File Copy from Server")
    window.geometry("600x300")  # Set window size

    # Input Frame
    input_frame = tk.Frame(window)
    input_frame.pack(padx=10, pady=20, fill="x")

    # Server File Path Label and Entry
    tk.Label(input_frame, text="Server File Path:", font=("Roboto", 14), anchor="w", width=20).grid(
        row=0, column=0, sticky="w"
    )
    file_path_entry = tk.Entry(input_frame, font=("Roboto", 14))
    file_path_entry.grid(row=0, column=1, padx=5, sticky="ew")
    input_frame.columnconfigure(1, weight=1)  # Make the entry field expandable

    # Destination Folder Label
    tk.Label(input_frame, text="Destination Folder:", font=("Roboto", 14), anchor="w", width=20).grid(
        row=1, column=0, sticky="w"
    )

    # Destination Folder Value Label (moved to row 2)
    destination_folder = tk.StringVar()
    folder_label = tk.Label(
        input_frame, textvariable=destination_folder, font=("Roboto", 14), fg="blue", anchor="w"
    )
    folder_label.grid(row=2, column=0, columnspan=2, padx=5, sticky="ew")  # Adjusted row and column span

    # Select Folder Button (moved to row 2, column 2)
    ttk.Button(
        input_frame,
        text="Select Folder",
        command=select_folder,
        width=15
    ).grid(row=2, column=2, padx=5, sticky="w")

    # Copy Button
    copy_button = ttk.Button(
        window, text="Copy File", command=copy_file
    )
    copy_button.pack(pady=20)

    window.mainloop()
