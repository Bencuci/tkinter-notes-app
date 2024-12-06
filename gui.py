import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from window_utils import center_window

SCREEN_WIDTH = 1366 
SCREEN_HEIGHT = 768

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome")
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 300, 200)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Welcome to Notes!", font=("Helvetica", 16))
        self.new_note_button = ttk.Button(self, text="New Note", command=lambda: NewNoteWindow().open_window())
        self.list_notes_button = ttk.Button(self, text="List Notes")

    def create_layout(self):
        self.title_label.pack(pady=10)
        self.new_note_button.pack(pady=10)
        self.list_notes_button.pack(pady=10)

    def open_window(self):
        self.mainloop()

class NewNoteWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("New Note")
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 400, 300)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Create a New Note", font=("Helvetica", 16))
        self.note_text = tk.Text(self, height=10, width=40)
        self.save_button = ttk.Button(self, text="Save")
    
    def create_layout(self):
        self.title_label.pack(pady=10)
        self.note_text.pack(pady=10)
        self.save_button.pack(pady=10)

    def open_window(self):
        self.mainloop()


MainWindow().open_window()
