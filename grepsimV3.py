import tkinter as tk
from tkinter import filedialog, messagebox, Spinbox
import os
import re
import pathlib
#You can set the number of lines you want to see before and after the search pattern
#using the spinboxes at the bottom
class PyGrepSim:
    def __init__(self, root):
      
        self.root = root
        self.setup_gui()
        self.subpath = "/"       
        self.path= os.path.join(os.path.expanduser("~"), self.subpath)
        
        
    def setup_gui(self):
        self.root.title("Py Grep Simulation")
        self.create_options_frame()
        self.create_file_frame()
        self.create_text_area()
        self.create_lines_control_frame()

    def create_options_frame(self):
        frame_options = tk.Frame(self.root)
        frame_options.pack(pady=5)

        tk.Label(frame_options, text="Pattern: RegEx").pack(side=tk.LEFT)
        self.entry_pattern = tk.Entry(frame_options,bd=7)
        self.entry_pattern.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_options, text="Large files you will get 'not respondeing' But you only need to wait").pack(side=tk.BOTTOM)
        self.var_case_insensitive = tk.BooleanVar()
        check_case_insensitive = tk.Checkbutton(frame_options, text="Case Insensitive", variable=self.var_case_insensitive)
        check_case_insensitive.pack(side=tk.LEFT)
        
    def create_file_frame(self):
        frame_file = tk.Frame(self.root)
        frame_file.pack(pady=5)

        tk.Label(frame_file, text="Filenames:").pack(side=tk.LEFT)
        self.filenamelist = tk.Listbox(frame_file, width=50,bd=7)
        self.filenamelist.pack(side=tk.LEFT, padx=5)

        tk.Button(frame_file, text="Browse Directory", bd=5,bg="light blue",command=self.open_file_dialog).pack(side=tk.LEFT)
        tk.Button(frame_file, text="Save Search Results", bd=5,bg="light green", command=self.save_file).pack(side=tk.RIGHT)
        tk.Button(frame_file, text="Save Filelist",bd=5, command=self.save_filelist).pack(side=tk.RIGHT)
        tk.Button(frame_file, text="Search",bd=5,command=self.search_for_pattern).pack(side=tk.RIGHT,pady=30)
        tk.Button(frame_file, text="Clear",bd=5, command=self.clear_all).pack(side=tk.LEFT,pady=30)

    def create_text_area(self):
        tk.Label(self.root, text="Results from search:").pack(side=tk.LEFT)
        self.text_area = tk.Text(self.root, height=15, width=80,bd=10)
        self.text_area.pack(padx=10, pady=5)

    def create_lines_control_frame(self):
        frame_lines_control = tk.Frame(self.root)
        frame_lines_control.pack(pady=5)

        tk.Label(frame_lines_control, text="Include # lines before search:").pack(side=tk.LEFT)
        self.spinbox_before = Spinbox(frame_lines_control, from_=0, to=99, width=3)
        self.spinbox_before.pack(side=tk.LEFT)

        tk.Label(frame_lines_control, text="Include # lines after search:").pack(side=tk.LEFT)
        self.spinbox_after = Spinbox(frame_lines_control, from_=0, to=99, width=3)
        self.spinbox_after.pack(side=tk.LEFT)



    def search_for_pattern(self):
        pattern = self.entry_pattern.get()
        lines_before = int(self.spinbox_before.get())
        lines_after = int(self.spinbox_after.get())
        self.text_area.delete('1.0', tk.END)  # Clear the text area for new output

        try:
            re_pattern = re.compile(pattern, re.IGNORECASE if self.var_case_insensitive.get() else 0)
        except re.error:
            messagebox.showerror("Invalid Pattern", "The entered pattern is not a valid regular expression.")
            return

        try:
            # Ensure that self.path is a string representing the path, e.g., r"C:\Users\..."
            filenames = os.listdir(self.path)
            for filename in filenames:
                file_path = os.path.join(self.path, filename)  # Correctly join the directory path and filename
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if re_pattern.search(line):
                            start = max(i - lines_before, 0)
                            end = min(i + lines_after + 1, len(lines))
                            self.text_area.insert(tk.END, f"---{filename}---\n")
                            for l in lines[start:end]:
                                self.text_area.insert(tk.END, l)
                            self.text_area.insert(tk.END, f"\n{'-'*40}\n")
        except SyntaxError as syn: 
            print(syn)
            self.text_area.insert(tk.END, "File not found. Please check the path and try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        
        
    def open_file_dialog(self):
        self.path = filedialog.askdirectory()
        filelist = os.listdir(self.path)
        self.filenamelist.delete(0, tk.END)  # Clear the entry field
        for file in filelist:
            self.filenamelist.insert(0, file)  # Insert the selected filename



     
    def save_filelist(self):
        filelist = filedialog.asksaveasfilename(defaultextension=".txt",
                                     filetypes=[("All Files", "*.*")],
                                         )
        if not filelist:
            return

        with open(filelist, "w") as output_file:
            flist = self.filenamelist.get(0, tk.END)
            strflist = str(flist)
            output_file.write(strflist)
            return flist

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("All Files", "*.*")],
                                 )
        if not filename:
            return
        with open(filename, "w") as output_file:
            text = self.text_area.get(1.0, tk.END)
            output_file.write(text)
            output_file.close()
            return 

    def clear_all(self):
        self.text_area.delete('1.0', tk.END)
        self.filenamelist.delete(0, tk.END)
        self.entry_pattern.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    grep = PyGrepSim(root)
    root.mainloop()
