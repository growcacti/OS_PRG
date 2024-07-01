import tkinter as tk
from tkinter import filedialog, messagebox, Spinbox, Scrollbar
from tkinter import ttk
import os
import re
from collections import defaultdict

class PyGrepSim:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.subpath = "/"
        self.path = os.path.join(os.path.expanduser("~"), self.subpath)
        
    def setup_gui(self):
        self.create_options_frame()
        self.create_file_frame()
        self.create_text_area()
        self.create_lines_control_frame()
        self.create_pattern_count_frame()

    def create_options_frame(self):
        frame_options = tk.Frame(self.root)
        frame_options.grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(frame_options, text="Pattern: RegEx").grid(row=0, column=0)
        self.entry_pattern = tk.Entry(frame_options, bd=7)
        self.entry_pattern.grid(row=0, column=1, padx=5)
        
        self.var_case_insensitive = tk.BooleanVar()
        check_case_insensitive = tk.Checkbutton(frame_options, text="Case Insensitive", variable=self.var_case_insensitive)
        check_case_insensitive.grid(row=0, column=2)
        
        tk.Label(frame_options, text="Large files may cause 'not responding', but please wait.").grid(row=1, column=0, columnspan=3)

    def create_file_frame(self):
        frame_file = tk.Frame(self.root)
        frame_file.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Label(frame_file, text="Filenames:").grid(row=0, column=0)
        
        self.filenamelist = tk.Listbox(frame_file, width=50, bd=7)
        self.scrollbar_listbox = tk.Scrollbar(frame_file, orient=tk.VERTICAL)
        self.filenamelist.config(yscrollcommand=self.scrollbar_listbox.set)
        self.scrollbar_listbox.config(command=self.filenamelist.yview)
        self.filenamelist.grid(row=0, column=1, padx=5)
        self.scrollbar_listbox.grid(row=0, column=2, sticky='ns')

        tk.Button(frame_file, text="Browse Directory", bd=5, bg="light blue", command=self.open_file_dialog).grid(row=0, column=3)
        tk.Button(frame_file, text="Save Search Results", bd=5, bg="light green", command=self.save_file).grid(row=1, column=3)
        tk.Button(frame_file, text="Save Filelist", bd=5, command=self.save_filelist).grid(row=1, column=2)
        tk.Button(frame_file, text="Search", bd=5, command=self.search_for_pattern).grid(row=1, column=0)
        tk.Button(frame_file, text="Clear", bd=5, command=self.clear_all).grid(row=0, column=4)

    def create_text_area(self):
        tk.Label(self.root, text="Results from search:").grid(row=2, column=0, sticky='w')
        
        frame_text = tk.Frame(self.root)
        frame_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        self.text_area = tk.Text(frame_text, height=15, width=80, bd=10, wrap=tk.NONE)
        self.scrollbar_text_y = tk.Scrollbar(frame_text, orient=tk.VERTICAL, command=self.text_area.yview)
        self.scrollbar_text_x = tk.Scrollbar(frame_text, orient=tk.HORIZONTAL, command=self.text_area.xview)
        self.text_area.config(yscrollcommand=self.scrollbar_text_y.set, xscrollcommand=self.scrollbar_text_x.set)
        
        self.text_area.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_text_y.grid(row=0, column=1, sticky='ns')
        self.scrollbar_text_x.grid(row=1, column=0, sticky='ew')
        
        frame_text.grid_rowconfigure(0, weight=1)
        frame_text.grid_columnconfigure(0, weight=1)

    def create_lines_control_frame(self):
        frame_lines_control = tk.Frame(self.root)
        frame_lines_control.grid(row=4, column=0, columnspan=2, pady=5)

        tk.Label(frame_lines_control, text="Include # lines before search:").grid(row=0, column=0)
        self.spinbox_before = Spinbox(frame_lines_control, from_=0, to=99, width=3)
        self.spinbox_before.grid(row=0, column=1)

        tk.Label(frame_lines_control, text="Include # lines after search:").grid(row=0, column=2)
        self.spinbox_after = Spinbox(frame_lines_control, from_=0, to=99, width=3)
        self.spinbox_after.grid(row=0, column=3)

    def create_pattern_count_frame(self):
        frame_pattern_count = tk.Frame(self.root)
        frame_pattern_count.grid(row=5, column=0, columnspan=2, pady=5)

        tk.Label(frame_pattern_count, text="Min. Repetitions:").grid(row=0, column=0)
        self.spinbox_min_reps = Spinbox(frame_pattern_count, from_=1, to=100, width=5)
        self.spinbox_min_reps.grid(row=0, column=1)

        self.var_ignore_repeats = tk.BooleanVar()
        check_ignore_repeats = tk.Checkbutton(frame_pattern_count, text="Ignore Repeats", variable=self.var_ignore_repeats)
        check_ignore_repeats.grid(row=0, column=2)

    def search_for_pattern(self):
        pattern = self.entry_pattern.get()
        lines_before = int(self.spinbox_before.get())
        lines_after = int(self.spinbox_after.get())
        min_reps = int(self.spinbox_min_reps.get())
        ignore_repeats = self.var_ignore_repeats.get()
        self.text_area.delete('1.0', tk.END)  # Clear the text area for new output

        try:
            re_pattern = re.compile(pattern, re.IGNORECASE if self.var_case_insensitive.get() else 0)
        except re.error:
            messagebox.showerror("Invalid Pattern", "The entered pattern is not a valid regular expression.")
            return

        match_count = 0
        pattern_dict = defaultdict(int)
        try:
            filenames = os.listdir(self.path)
            for filename in filenames:
                file_path = os.path.join(self.path, filename)
                if not os.path.isfile(file_path):
                    continue
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        matches = re_pattern.findall(line)
                        for match in matches:
                            pattern_dict[match] += 1
                            if pattern_dict[match] >= min_reps:
                                match_count += 1
                                if not ignore_repeats:
                                    start = max(i - lines_before, 0)
                                    end = min(i + lines_after + 1, len(lines))
                                    self.text_area.insert(tk.END, f"---{filename}---\n")
                                    for l in lines[start:end]:
                                        self.text_area.insert(tk.END, l)
                                    self.text_area.insert(tk.END, f"\n{'-'*40}\n")
            self.text_area.insert(tk.END, f"\nTotal matches: {match_count}\n")
            self.text_area.insert(tk.END, f"Patterns found more than {min_reps} times:\n{dict(pattern_dict)}")
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
                                                filetypes=[("Text Files", "*.txt")])
        if not filelist:
            return

        with open(filelist, "w") as output_file:
            flist = self.filenamelist.get(0, tk.END)
            output_file.write("\n".join(flist))

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt")])
        if not filename:
            return
        with open(filename, "w") as output_file:
            text = self.text_area.get(1.0, tk.END)
            output_file.write(text)

    def clear_all(self):
        self.text_area.delete('1.0', tk.END)
        self.filenamelist.delete(0, tk.END)
        self.entry_pattern.delete(0, tk.END)


class FileComparator:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Template File:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_template = tk.Entry(self.root, width=50)
        self.entry_template.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_template).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.root, text="File to Compare:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_compare = tk.Entry(self.root, width=50)
        self.entry_compare.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_compare).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(self.root, text="Compare", command=self.compare_files).grid(row=2, column=1, padx=5, pady=20)

    def browse_template(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), ("All Files", "*.*")])
        if file_path:
            self.entry_template.delete(0, tk.END)
            self.entry_template.insert(0, file_path)

    def browse_compare(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), ("All Files", "*.*")])
        if file_path:
            self.entry_compare.delete(0, tk.END)
            self.entry_compare.insert(0, file_path)

    def compare_files(self):
        template_path = self.entry_template.get()
        compare_path = self.entry_compare.get()

        if not template_path or not compare_path:
            messagebox.showwarning("Input Error", "Please select both template and compare files.")
            return

        try:
            with open(template_path, 'r') as template_file:
                template_strings = set(line.strip() for line in template_file.readlines())

            with open(compare_path, 'r') as compare_file:
                compare_strings = set(line.strip() for line in compare_file.readlines())

            matched = template_strings & compare_strings
            unmatched = compare_strings - template_strings

            self.save_results(matched, unmatched)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_results(self, matched, unmatched):
        matched_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Matched Results", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), ("All Files", "*.*")])
        if matched_path:
            with open(matched_path, 'w') as matched_file:
                matched_file.write("\n".join(matched))

        unmatched_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Unmatched Results", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), ("All Files", "*.*")])
        if unmatched_path:
            with open(unmatched_path, 'w') as unmatched_file:
                unmatched_file.write("\n".join(unmatched))

        messagebox.showinfo("Success", "Files compared and results saved.")


if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill='both')

    # Add PyGrepSim Tab
    pygrep_tab = tk.Frame(notebook)
    notebook.add(pygrep_tab, text='PyGrepSim')
    PyGrepSim(pygrep_tab)

    # Add File Comparator Tab
    file_comparator_tab = tk.Frame(notebook)
    notebook.add(file_comparator_tab, text='File Comparator')
    FileComparator(file_comparator_tab)

    root.mainloop()
