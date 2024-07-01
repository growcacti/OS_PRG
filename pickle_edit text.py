import tkinter as tk
from tkinter import filedialog, messagebox
import pickle

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.text_widget = tk.Text(root)
        self.text_widget.pack(expand=True, fill='both')

        # Load stacks if they exist
        self.undo_stack, self.redo_stack = self.load_stacks()

        # Create menu bar
        self.create_menu()

        # Create toolbar
        self.create_toolbar()

        # Bind keypress event to capture text changes
        self.text_widget.bind('<Key>', self.capture_edit)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        self.root.config(menu=menu_bar)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        
        undo_button = tk.Button(toolbar, text="Undo", command=self.undo)
        undo_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        redo_button = tk.Button(toolbar, text="Redo", command=self.redo)
        redo_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        save_button = tk.Button(toolbar, text="Save", command=self.save_file)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def capture_edit(self, event):
        # Simplified edit capture logic
        key = event.char
        if key and event.keysym != "BackSpace":
            insert_point = self.text_widget.index("insert")
            self.undo_stack.append(('insert', insert_point, key))
        elif event.keysym == "BackSpace":
            insert_point = self.text_widget.index("insert")
            char_before_cursor = self.text_widget.get(insert_point + "-1c", insert_point)
            if char_before_cursor:
                self.undo_stack.append(('delete', insert_point, char_before_cursor))
    
    def undo(self):
        if self.undo_stack:
            action, position, char = self.undo_stack.pop()
            self.redo_stack.append((action, position, char))
            
            if action == 'insert':
                self.text_widget.delete(f"{position} -1c")
            elif action == 'delete':
                self.text_widget.insert(position, char)

    def redo(self):
        if self.redo_stack:
            action, position, char = self.redo_stack.pop()
            self.undo_stack.append((action, position, char))
            
            if action == 'delete':
                self.text_widget.delete(f"{position} -1c")
            elif action == 'insert':
                self.text_widget.insert(position, char)

    def on_close(self):
        # Save stacks to a file upon closing
        self.save_stacks(self.undo_stack, self.redo_stack)
        self.root.destroy()

    def save_stacks(self, undo_stack, redo_stack):
        with open('text_editor_stacks.pkl', 'wb') as file:
            pickle.dump((undo_stack, redo_stack), file)

    def load_stacks(self):
        try:
            with open('text_editor_stacks.pkl', 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return [], []

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.get(1.0, tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
