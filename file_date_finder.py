import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import shutil
from datetime import datetime

class FileSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Search and Copy")

        self.recursive = tk.BooleanVar()
        self.create_widgets()

    def create_widgets(self):
        # USB Drive Path
        self.usb_label = tk.Label(self.root, text="Search Path:")
        self.usb_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.usb_entry = tk.Entry(self.root, width=50)
        self.usb_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.usb_browse_button = tk.Button(self.root, text="Browse", command=self.browse_usb)
        self.usb_browse_button.grid(row=0, column=2, padx=10, pady=10)
        
        # File Extension
        self.ext_label = tk.Label(self.root, text="File Extension:")
        self.ext_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.ext_entry = tk.Entry(self.root, width=50)
        self.ext_entry.grid(row=1, column=1, padx=10, pady=10)

        # Date Range
        self.start_date_label = tk.Label(self.root, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.start_date_entry = tk.Entry(self.root, width=20)
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        self.end_date_label = tk.Label(self.root, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=2, column=1, padx=10, pady=10, sticky='e')
        
        self.end_date_entry = tk.Entry(self.root, width=20)
        self.end_date_entry.grid(row=2, column=2, padx=10, pady=10, sticky='w')
        
        # Destination Path
        self.dest_label = tk.Label(self.root, text="Destination Path:")
        self.dest_label.grid(row=3, column=0, padx=10, pady=10)
        
        self.dest_entry = tk.Entry(self.root, width=50)
        self.dest_entry.grid(row=3, column=1, padx=10, pady=10)
        
        self.dest_browse_button = tk.Button(self.root, text="Browse", command=self.browse_dest)
        self.dest_browse_button.grid(row=3, column=2, padx=10, pady=10)
        
        # Recursive Search Option
        self.recursive_checkbutton = tk.Checkbutton(self.root, text="Recursive Search", variable=self.recursive)
        self.recursive_checkbutton.grid(row=4, column=1, padx=10, pady=10)

        # Search Button
        self.search_button = tk.Button(self.root, text="Search", command=self.search_files)
        self.search_button.grid(row=5, column=1, padx=10, pady=10)

        # Result Listbox
        self.result_listbox = tk.Listbox(self.root, width=100, height=20)
        self.result_listbox.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        
        # Copy Button
        self.copy_button = tk.Button(self.root, text="Copy Selected Files", command=self.copy_selected_files)
        self.copy_button.grid(row=7, column=1, padx=10, pady=10)

    def browse_usb(self):
        usb_path = filedialog.askdirectory()
        self.usb_entry.delete(0, tk.END)
        self.usb_entry.insert(0, usb_path)

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

    def search_files(self):
        usb_path = self.usb_entry.get()
        file_ext = self.ext_entry.get()
        dest_path = self.dest_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        is_recursive = self.recursive.get()

        if not usb_path or not file_ext or not dest_path or not start_date or not end_date:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not os.path.exists(usb_path):
            messagebox.showerror("Error", "Search Path does not exist")
            return
        
        if not os.path.exists(dest_path):
            messagebox.showerror("Error", "Destination Path does not exist")
            return
        
        # Check if the destination directory is within the search path
        if os.path.commonpath([usb_path]) == os.path.commonpath([usb_path, dest_path]):
            messagebox.showerror("Error", "Destination path cannot be within the search path")
            return

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return

        self.result_listbox.delete(0, tk.END)

        if is_recursive:
            files_found = self.recursive_search(usb_path, file_ext, start_date, end_date)
        else:
            files_found = self.non_recursive_search(usb_path, file_ext, start_date, end_date)

        for file in files_found:
            self.result_listbox.insert(tk.END, file)

        messagebox.showinfo("Success", f"Found {len(files_found)} files")

    def recursive_search(self, search_path, file_ext, start_date, end_date):
        files_found = []
        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith(file_ext):
                    full_file_path = os.path.join(root, file)
                    file_creation_date = datetime.fromtimestamp(os.path.getctime(full_file_path))
                    if start_date <= file_creation_date <= end_date:
                        files_found.append(full_file_path)
        return files_found

    def non_recursive_search(self, search_path, file_ext, start_date, end_date):
        files_found = []
        for file in os.listdir(search_path):
            full_file_path = os.path.join(search_path, file)
            if os.path.isfile(full_file_path) and file.endswith(file_ext):
                file_creation_date = datetime.fromtimestamp(os.path.getctime(full_file_path))
                if start_date <= file_creation_date <= end_date:
                    files_found.append(full_file_path)
        return files_found

    def copy_selected_files(self):
        dest_path = self.dest_entry.get()
        if not dest_path:
            messagebox.showerror("Error", "Destination path is required")
            return

        if not os.path.exists(dest_path):
            messagebox.showerror("Error", "Destination path does not exist")
            return

        selected_files = self.result_listbox.curselection()
        files_to_copy = [self.result_listbox.get(i) for i in selected_files]

        for file in files_to_copy:
            shutil.copy(file, dest_path)

        messagebox.showinfo("Success", f"Copied {len(files_to_copy)} files to {dest_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()
