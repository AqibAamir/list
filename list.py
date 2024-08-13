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
