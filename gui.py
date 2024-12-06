import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome")
        self.geometry("300x200")
        self.create_widgets()
        self.create_layout()
    
    def create_widgets(self):
        self.label = ttk.Label(self, text="Welcome to Notes!", font=("Helvetica", 16))

    def create_layout(self):
        self.label.pack(pady=10)

    def open_window(self):
        self.mainloop()

MainWindow().open_window()
