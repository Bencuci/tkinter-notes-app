import tkinter as tk
from tkinter import messagebox
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
        self.child_windows = {}
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Welcome to Notes!", font=("Helvetica", 16))
        self.new_note_button = ttk.Button(self, text="New Note", command=self.handle_new_note_button)
        self.list_notes_button = ttk.Button(self, text="List Notes")

    def create_layout(self):
        self.title_label.pack(pady=10)
        self.new_note_button.pack(pady=10)
        self.list_notes_button.pack(pady=10)

    def handle_new_note_button(self):
        if 'new_note' in self.child_windows and self.child_windows['new_note'].winfo_exists():
            self.child_windows['new_note'].lift()
            self.child_windows['new_note'].focus_force()
        else:
            new_note_window = NewNoteWindow(self)
            self.child_windows['new_note'] = new_note_window

    def open_window(self):
        self.mainloop()

class NewNoteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("New Note")
        self.transient(parent) # Make window dependent on parent
        self.grab_set() # Make modal
        self.focus_force() # Ensure focus
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Handle window close
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 400, 300)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Create a New Note", font=("Helvetica", 16))
        self.note_text = tk.Text(self, height=10, width=40)
        self.save_button = ttk.Button(self, text="Save", command=self.handle_save_button)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.on_closing, bootstyle='secondary')
    
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.title_label.grid(row=0, column=0, pady=10, padx=5, columnspan=2, sticky='n')
        self.note_text.grid(row=1, column=0, pady=10, padx=5, columnspan=2)
        self.save_button.grid(row=2, column=0, pady=10, padx=5, sticky='e')
        self.cancel_button.grid(row=2, column=1, pady=10, padx=5, sticky='w')

    def handle_save_button(self):
        self.grab_release()
        response = messagebox.showinfo("Success", "Note saved successfully!")
        self.destroy()

    def open_window(self):
        self.mainloop()

    def on_closing(self):
        self.grab_release()
        self.destroy()


root = MainWindow()
root.open_window()
