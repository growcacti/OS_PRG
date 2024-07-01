import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import shutil

class FileSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Extention Search and Copy")

        self.recursive = tk.BooleanVar()
        self.create_widgets()

    def create_widgets(self):
        self.exlabel = tk.Label(self.root, text="Drive Path:")
        self.exlabel.grid(row=0, column=0, padx=10, pady=10)
        
        self.exentry = tk.Entry(self.root, width=50,bd=7,bg="seashell")
        self.exentry.grid(row=0, column=1, padx=10, pady=10)
        
        self.exbrowse_button = tk.Button(self.root, text="Browse", bd=7,bg="light blue",command=self.browse_usb)
        self.exbrowse_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.ext_label = tk.Label(self.root, text="File Extension:")
        self.ext_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.ext_entry = tk.Entry(self.root, width=50,bd=7,bg="azure")
        self.ext_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.dest_label = tk.Label(self.root, text="Destination Path:")
        self.dest_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.dest_entry = tk.Entry(self.root, width=50,bd=7,bg="alice blue")
        self.dest_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.dest_browse_button = tk.Button(self.root, text="Browse", bd=7,bg="light blue",command=self.browse_dest)
        self.dest_browse_button.grid(row=2, column=2, padx=10, pady=10)
        
        self.recursive_checkbutton = tk.Checkbutton(self.root, text="Recursive Search", variable=self.recursive)
        self.recursive_checkbutton.grid(row=3, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.root, text="Search and Copy", bd=7,bg="light green",command=self.search_and_copy)
        self.search_button.grid(row=4, column=1, padx=10, pady=10)

    def browse_usb(self):
        expath = filedialog.askdirectory()
        self.exentry.delete(0, tk.END)
        self.exentry.insert(0, expath)

    def browse_dest(self):
        dest_path = filedialog.askdirectory()
        if dest_path:
            create_new = messagebox.askyesno("Create New Directory", "Do you want to create a new directory?")
            if create_new:
                new_dir_name = simpledialog.askstring("New Directory", "Enter the name of the new directory:")
                if new_dir_name:
                    new_dir_path = os.path.join(dest_path, new_dir_name)
                    os.makedirs(new_dir_path, exist_ok=True)
                    self.dest_entry.delete(0, tk.END)
                    self.dest_entry.insert(0, new_dir_path)
                else:
                    self.dest_entry.delete(0, tk.END)
                    self.dest_entry.insert(0, dest_path)
            else:
                self.dest_entry.delete(0, tk.END)
                self.dest_entry.insert(0, dest_path)

    def search_and_copy(self):
        expath = self.exentry.get()
        file_ext = self.ext_entry.get()
        dest_path = self.dest_entry.get()
        is_recursive = self.recursive.get()
        
        if not expath or not file_ext or not dest_path:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not os.path.exists(expath):
            messagebox.showerror("Error", "USB Path does not exist")
            return
        
        if not os.path.exists(dest_path):
            messagebox.showerror("Error", "Destination Path does not exist")
            return
        
        # Check if the destination directory is within the search path
        if os.path.commonpath([expath]) == os.path.commonpath([expath, dest_path]):
            messagebox.showerror("Error", "Destination path cannot be within the search path")
            return

        if is_recursive:
            files_copied = self.recursive_search_and_copy(expath, file_ext, dest_path)
        else:
            files_copied = self.non_recursive_search_and_copy(expath, file_ext, dest_path)

        messagebox.showinfo("Success", f"Copied {files_copied} files to {dest_path}")

    def recursive_search_and_copy(self, search_path, file_ext, dest_path):
        files_copied = 0
        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith(file_ext):
                    full_file_path = os.path.join(root, file)
                    shutil.copy(full_file_path, dest_path)
                    files_copied += 1
        return files_copied

    def non_recursive_search_and_copy(self, search_path, file_ext, dest_path):
        files_copied = 0
        for file in os.listdir(search_path):
            full_file_path = os.path.join(search_path, file)
            if os.path.isfile(full_file_path) and file.endswith(file_ext):
                shutil.copy(full_file_path, dest_path)
                files_copied += 1
        return files_copied

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()
