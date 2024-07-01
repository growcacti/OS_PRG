import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, directory)

def merge_files():
    directory = entry_dir.get()
    file_types = entry_file_types.get().split()
    
    if not directory or not file_types:
        messagebox.showerror("Error", "Please provide both directory and file types.")
        return

    merged_content = ""
    for file_type in file_types:
        for file_name in os.listdir(directory):
            if file_name.endswith(file_type):
                with open(os.path.join(directory, file_name), 'r') as file:
                    merged_content += file.read() + "\n"
    
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as output_file:
            output_file.write(merged_content)
        messagebox.showinfo("Success", "Files merged successfully!")

# Create the main window
window = tk.Tk()
window.title("Merge Text Files")

# Create and place labels and entry fields
ttk.Label(window, text="Select Directory:").pack(pady=5)
entry_dir = ttk.Entry(window, width=50)
entry_dir.pack(pady=5)
ttk.Button(window, text="Browse", command=select_directory).pack(pady=5)

ttk.Label(window, text="Enter File Types (e.g. .txt .py .log):").pack(pady=5)
entry_file_types = ttk.Entry(window, width=50)
entry_file_types.pack(pady=5)

# Create and place the merge button
merge_button = ttk.Button(window, text="Merge Files", command=merge_files)
merge_button.pack(pady=20)

# Run the application
window.mainloop()
