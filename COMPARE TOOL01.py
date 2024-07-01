import tkinter as tk
from tkinter import filedialog, messagebox

class FileComparator:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.root.title("File Comparator")

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
    app = FileComparator(root)
    root.mainloop()
