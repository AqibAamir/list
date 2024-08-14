import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
from datetime import datetime
import json
import csv

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced To-Do List App")
        self.root.geometry("800x600")
        
        self.tasks = []
        self.undo_stack = []
        self.redo_stack = []
        self.theme = {
            "bg_color": "#F5F5F5",
            "fg_color": "#333333",
            "btn_color": "#007BFF",
            "font": ("Arial", 14)
        }
        
        self.create_widgets()
        self.create_menu()
        self.apply_theme()
        
    def create_widgets(self):
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_listbox)

        self.search_entry = tk.Entry(self.root, textvariable=self.search_var, font=self.theme["font"], width=30)
        self.search_entry.pack(pady=10)
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)
        
        self.listbox = tk.Listbox(self.frame, width=50, height=15, font=self.theme["font"], selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.entry = tk.Entry(self.root, font=self.theme["font"], width=50)
        self.entry.pack(pady=10)
        
        self.category_var = tk.StringVar()
        self.category_entry = tk.Entry(self.root, textvariable=self.category_var, font=self.theme["font"], width=20)
        self.category_entry.pack(pady=5)

        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.Combobox(self.root, textvariable=self.priority_var, values=["Low", "Medium", "High"], font=self.theme["font"], width=10)
        self.priority_menu.pack(pady=5)
        
        self.due_date_var = tk.StringVar()
        self.due_date_entry = tk.Entry(self.root, textvariable=self.due_date_var, font=self.theme["font"], width=20)
        self.due_date_entry.pack(pady=5)
        
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        
        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task, width=15, bg=self.theme["btn_color"], fg="white")
        self.add_button.grid(row=0, column=0, padx=10)
        
        self.remove_button = tk.Button(self.button_frame, text="Remove Task", command=self.remove_task, width=15, bg=self.theme["btn_color"], fg="white")
        self.remove_button.grid(row=0, column=1, padx=10)
        
        self.update_button = tk.Button(self.button_frame, text="Update Task", command=self.update_task, width=15, bg=self.theme["btn_color"], fg="white")
        self.update_button.grid(row=0, column=2, padx=10)
        
        self.sort_button = tk.Button(self.button_frame, text="Sort Tasks", command=self.sort_tasks, width=15, bg=self.theme["btn_color"], fg="white")
        self.sort_button.grid(row=1, column=0, padx=10, pady=5)
        
        self.undo_button = tk.Button(self.button_frame, text="Undo", command=self.undo, width=15, bg=self.theme["btn_color"], fg="white")
        self.undo_button.grid(row=1, column=1, padx=10, pady=5)
        
        self.redo_button = tk.Button(self.button_frame, text="Redo", command=self.redo, width=15, bg=self.theme["btn_color"], fg="white")
        self.redo_button.grid(row=1, column=2, padx=10, pady=5)

       
    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load Tasks", command=self.load_tasks)
        self.file_menu.add_command(label="Save Tasks", command=self.save_tasks)
        self.file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        self.file_menu.add_command(label="Import from CSV", command=self.import_from_csv)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Settings", command=self.open_settings)
        
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        
    def add_task(self):
        task = self.entry.get()
        category = self.category_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()
        
        if task != "":
            task_info = {
                "task": task,
                "category": category,
                "priority": priority,
                "due_date": due_date,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.tasks.append(task_info)
            self.undo_stack.append(("add", task_info))
            self.update_listbox()
            self.entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")
            
    def remove_task(self):
        selected_task = self.listbox.curselection()
        if selected_task:
            task_info = self.tasks.pop(selected_task[0])
            self.undo_stack.append(("remove", task_info))
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task.")
    
    def update_task(self):
        selected_task = self.listbox.curselection()
        if selected_task:
            task_info = self.tasks[selected_task[0]]
            new_task = simpledialog.askstring("Update Task", "Edit your task:", initialvalue=task_info["task"])
            if new_task:
                task_info["task"] = new_task
                task_info["category"] = simpledialog.askstring("Update Category", "Edit your category:", initialvalue=task_info["category"])
                task_info["priority"] = simpledialog.askstring("Update Priority", "Edit your priority:", initialvalue=task_info["priority"])
                task_info["due_date"] = simpledialog.askstring("Update Due Date", "Edit your due date:", initialvalue=task_info["due_date"])
                self.undo_stack.append(("update", task_info))
                self.update_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task.")
   
    def sort_tasks(self):
        sort_by = simpledialog.askstring("Sort Tasks", "Sort by (task/category/priority/due_date):").lower()
        if sort_by in ["task", "category", "priority", "due_date"]:
            self.tasks.sort(key=lambda x: x.get(sort_by, ""))
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Invalid sort option.")
    
    def undo(self):
        if self.undo_stack:
            action, task_info = self.undo_stack.pop()
            if action == "add":
                self.tasks.remove(task_info)
            elif action == "remove":
                self.tasks.append(task_info)
            elif action == "update":
                old_task_info = next((task for task in self.tasks if task["task"] == task_info["task"]), None)
                if old_task_info:
                    old_task_info.update(task_info)
            self.redo_stack.append((action, task_info))
            self.update_listbox()
    
    def redo(self):
        if self.redo_stack:
            action, task_info = self.redo_stack.pop()
            if action == "add":
                self.tasks.append(task_info)
            elif action == "remove":
                self.tasks.remove(task_info)
            elif action == "update":
                old_task_info = next((task for task in self.tasks if task["task"] == task_info["task"]), None)
                if old_task_info:
                    old_task_info.update(task_info)
            self.undo_stack.append((action, task_info))
            self.update_listbox()
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
                self.update_listbox()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved tasks found.")
    
    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=4)
        messagebox.showinfo("Success", "Tasks saved successfully.")
    
    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Task", "Category", "Priority", "Due Date", "Created At"])
                for task_info in self.tasks:
                    writer.writerow([task_info["task"], task_info["category"], task_info["priority"], task_info["due_date"], task_info["created_at"]])
            messagebox.showinfo("Success", "Tasks exported to CSV successfully.")
    
    def import_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                self.tasks = list(reader)
                self.update_listbox()
            messagebox.showinfo("Success", "Tasks imported from CSV successfully.")
    
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x300")

class ToDoApp:
        def __init__(self, root):
            self.root = root
            self.root.title("To-Do List App")
            self.root.geometry("500x400")

        # Initialize theme
            self.theme = {
            "bg_color": "#F5F5F5",
            "fg_color": "#333333",
            "btn_color": "#007BFF",
            "font": ("Arial", 14)
        }

        # Create the main frame and widgets
            self.button_frame = tk.Frame(self.root)
            self.button_frame.pack(fill="x", padx=10, pady=10)

            self.listbox = tk.Listbox(self.root, selectmode="extended", font=self.theme["font"])
            self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

            self.entry = tk.Entry(self.root, font=self.theme["font"])
            self.entry.pack(fill="x", padx=10, pady=5)

        # Settings button
            settings_button = tk.Button(self.button_frame, text="Settings", command=self.open_settings, font=self.theme["font"], bg=self.theme["btn_color"], fg=self.theme["fg_color"])
            settings_button.pack(side="right", padx=10)

        # Show About button
            about_button = tk.Button(self.button_frame, text="About", command=self.show_about, font=self.theme["font"], bg=self.theme["btn_color"], fg=self.theme["fg_color"])
            about_button.pack(side="left", padx=10)

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x250")
        settings_window.configure(bg=self.theme["bg_color"])

        # Theme Selection
        theme_label = tk.Label(settings_window, text="Select Theme:", font=self.theme["font"], bg=self.theme["bg_color"], fg=self.theme["fg_color"])
        theme_label.pack(pady=10)
        
        self.theme_var = tk.StringVar(value="Default")
        default_theme = tk.Radiobutton(settings_window, text="Default", variable=self.theme_var, value="Default", font=self.theme["font"], command=self.change_theme)
        default_theme.pack(anchor="w", padx=20)
        dark_theme = tk.Radiobutton(settings_window, text="Dark", variable=self.theme_var, value="Dark", font=self.theme["font"], command=self.change_theme)
        dark_theme.pack(anchor="w", padx=20)

        # Font Size Selection
        font_label = tk.Label(settings_window, text="Select Font Size:", font=self.theme["font"], bg=self.theme["bg_color"], fg=self.theme["fg_color"])
        font_label.pack(pady=10)

        self.font_size_var = tk.IntVar(value=14)
        font_size_spinbox = tk.Spinbox(settings_window, from_=10, to=30, textvariable=self.font_size_var, font=self.theme["font"])
        font_size_spinbox.pack(pady=5)

        apply_button = tk.Button(settings_window, text="Apply", command=self.apply_settings, font=self.theme["font"], bg=self.theme["btn_color"], fg=self.theme["fg_color"])
        apply_button.pack(pady=20)

    def change_theme(self):
        theme = self.theme_var.get()
        if theme == "Default":
            self.theme = {
                "bg_color": "#F5F5F5",
                "fg_color": "#333333",
                "btn_color": "#007BFF",
                "font": ("Arial", 14)
            }
        elif theme == "Dark":
            self.theme = {
                "bg_color": "#333333",
                "fg_color": "#F5F5F5",
                "btn_color": "#1E90FF",
                "font": ("Arial", 14)
            }
        self.apply_theme()
    
    def apply_theme(self):
        self.root.configure(bg=self.theme["bg_color"])
        self.listbox.configure(bg=self.theme["bg_color"], fg=self.theme["fg_color"], font=self.theme["font"])
        self.entry.configure(bg=self.theme["bg_color"], fg=self.theme["fg_color"], font=self.theme["font"])
        for button in self.button_frame.winfo_children():
            button.configure(bg=self.theme["btn_color"], fg=self.theme["fg_color"], font=self.theme["font"])

    def apply_settings(self):
        new_font_size = self.font_size_var.get()
        self.theme["font"] = ("Arial", new_font_size)
        self.apply_theme()

    def reset_settings(self):
        self.theme_var.set("Default")
        self.font_size_var.set(14)
        self.change_theme()
        self.apply_theme()

        messagebox.showinfo("Settings", "Settings have been reset to default.")

    def show_about(self):
        messagebox.showinfo("About", "Advanced To-Do List App\nVersion 2.0\nCreated by ChatGPT")

def main():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
