import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from window_utils import center_window
from database import DatabaseCRUD

SCREEN_WIDTH = 1366 
SCREEN_HEIGHT = 768
THEMES = ['superhero', 'darkly', 'solar', 'cyborg', 'vapor', 'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']

DatabaseCRUD.initialize_database()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome")
        self.style = ttk.Style(theme='superhero')
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 300, 200)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
        self.child_windows = {}
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Welcome to Notes!", font=("Helvetica", 16))
        self.new_note_button = ttk.Button(self, text="New Note", command=self.handle_new_note_button)
        self.list_notes_button = ttk.Button(self, text="List Notes", command=self.handle_list_notes_button)
        self.settings_button = ttk.Button(self, text="Settings", command=self.handle_settings_button)

    def create_layout(self):
        self.title_label.pack(pady=10)
        self.new_note_button.pack(pady=5)
        self.list_notes_button.pack(pady=5)
        self.settings_button.pack(pady=5)

    def handle_settings_button(self):
        if 'settings' in self.child_windows and self.child_windows['settings'].winfo_exists():
            self.child_windows['settings'].lift()
            self.child_windows['settings'].focus_force()
        else:
            settings_window = SettingsWindow(self)
            self.child_windows['settings'] = settings_window

    def handle_new_note_button(self):
        if 'new_note' in self.child_windows and self.child_windows['new_note'].winfo_exists():
            self.child_windows['new_note'].lift()
            self.child_windows['new_note'].focus_force()
        else:
            new_note_window = NewNoteWindow(self)
            self.child_windows['new_note'] = new_note_window

    def handle_list_notes_button(self):
        if 'list_notes' in self.child_windows and self.child_windows['list_notes'].winfo_exists():
            self.child_windows['list_notes'].lift()
            self.child_windows['list_notes'].focus_force()
        else:
            list_notes_window = ListNotesWindow(self)
            self.child_windows['list_notes'] = list_notes_window

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
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 400, 350)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Create a New Note", font=("Helvetica", 16))
        self.note_title_label = ttk.Label(self, text="Title")
        self.note_title = ttk.Entry(self)
        self.note_content_label = ttk.Label(self, text="Content")
        self.note_content= tk.Text(self, height=10, width=40)
        self.save_button = ttk.Button(self, text="Save", command=self.handle_save_button)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.on_closing, bootstyle='secondary')
    
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.title_label.grid(row=0, columnspan=2, pady=(20,10))
        self.note_title_label.grid(row=1, column=0, sticky='w', padx=20)
        self.note_title.grid(row=2, columnspan=2, sticky='ew', padx=20)
        self.note_content_label.grid(row=3, column=0, sticky='w', padx=20)
        self.note_content.grid(row=4, columnspan=2, sticky='ew', padx=20)
        self.save_button.grid(row=5, column=0, sticky='e', padx=5, pady=20)
        self.cancel_button.grid(row=5, column=1, sticky='w', padx=5, pady=20)

    def handle_save_button(self):
        title = self.note_title.get()
        content = self.note_content.get("1.0", tk.END)
        DatabaseCRUD.add_note(title, content)
        self.grab_release()
        response = messagebox.showinfo("Success", "Note saved successfully!")
        self.destroy()

    def open_window(self):
        self.mainloop()

    def on_closing(self):
        self.grab_release()
        self.destroy()


class ListNotesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.note_ids = {}
        self.parent = parent
        self.title("List Notes")
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 400, 325)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
        self.load_notes()
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="List of Notes", font=("Helvetica", 16))
        self.notes_list = tk.Listbox(self, height=10, width=40)
        self.edit_button = ttk.Button(self, text="Edit", command=self.handle_edit_button)
        self.delete_button = ttk.Button(self, text="Delete", command=self.handle_delete_button)
        self.go_back_button = ttk.Button(self, text="Go Back", command=self.on_closing, bootstyle='secondary')
    
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.title_label.grid(row=0, column=0, pady=10, padx=5, columnspan=2, sticky='n')
        self.notes_list.grid(row=1, column=0, pady=10, padx=5, columnspan=2)
        self.edit_button.grid(row=2, column=0, pady=10, padx=5, sticky='e')
        self.delete_button.grid(row=2, column=1, pady=10, padx=5, sticky='w')
        self.go_back_button.grid(row=3, column=0, pady=10, padx=5, columnspan=2)

    def handle_edit_button(self):
        selected_note = self.notes_list.curselection()
        if selected_note:
            note = DatabaseCRUD.get_note(self.note_ids[self.notes_list.get(selected_note)])
            if 'edit_note' in self.parent.child_windows and self.parent.child_windows['edit_note'].winfo_exists():
                self.parent.child_windows['edit_note'].lift()
                self.parent.child_windows['edit_note'].focus_force()
            else:
                edit_note_window = EditNoteWindow(self, note)
                self.parent.child_windows['edit_note'] = edit_note_window
        else:
            response = messagebox.showerror("Error", "No note selected!")

    def handle_delete_button(self):
        selected_note = self.notes_list.curselection()
        if selected_note:
            note = self.notes_list.get(selected_note)

    def load_notes(self):
        notes = DatabaseCRUD.get_notes()
        self.note_ids = {note["title"]: note["id"] for note in notes}
        for note in notes:
            self.notes_list.insert(tk.END, note["title"])

    def open_window(self):
        self.mainloop()

    def on_closing(self):
        self.grab_release()
        self.destroy()

class EditNoteWindow(tk.Toplevel):
    def __init__(self, parent, note):
        super().__init__(parent)
        self.parent = parent
        self.note = note
        self.title("Edit Note")
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 400, 350)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
        self.populate_fields()
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Edit Note", font=("Helvetica", 16))
        self.note_title_label = ttk.Label(self, text="Title")
        self.note_title = ttk.Entry(self)
        self.note_content_label = ttk.Label(self, text="Content")
        self.note_content= tk.Text(self, height=10, width=40)
        self.save_button = ttk.Button(self, text="Save", command=self.handle_save_button)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.on_closing, bootstyle='secondary')
    
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.title_label.grid(row=0, columnspan=2, pady=(20,10))
        self.note_title_label.grid(row=1, column=0, sticky='w', padx=20)
        self.note_title.grid(row=2, columnspan=2, sticky='ew', padx=20)
        self.note_content_label.grid(row=3, column=0, sticky='w', padx=20)
        self.note_content.grid(row=4, columnspan=2, sticky='ew', padx=20)
        self.save_button.grid(row=5, column=0, sticky='e', padx=5, pady=20)
        self.cancel_button.grid(row=5, column=1, sticky='w', padx=5, pady=20)

    def handle_save_button(self):
        title = self.note_title.get()
        content = self.note_content.get("1.0", tk.END)
        DatabaseCRUD.edit_note(self.note["id"], title, content)
        self.grab_release()
        response = messagebox.showinfo("Success", "Note updated successfully!")
        self.destroy()

    def populate_fields(self):
        self.note_title.insert(0, self.note["title"])
        self.note_content.insert(tk.END, self.note["content"])

    def open_window(self):
        self.mainloop()

    def on_closing(self):
        self.grab_release()
        self.destroy()

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 400, 200)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Settings", font=("Helvetica", 16))
        self.theme_label = ttk.Label(self, text="Theme")
        self.theme_var = tk.StringVar()
        self.theme_var.set(self.parent.style.theme_use())
        self.font_size_label = ttk.Label(self, text="Font Size")
        self.font_size_var = tk.StringVar()
        self.font_size_var.set("12")
        self.font_family_label = ttk.Label(self, text="Font Family")
        self.font_family_var = tk.StringVar()
        self.font_family_var.set("Helvetica")
        self.theme_combobox = ttk.Combobox(self, textvariable=self.theme_var, values=THEMES)
        self.font_size_combobox = ttk.Combobox(self, textvariable=self.font_size_var, values=['10', '12', '14', '16', '18', '20'])
        self.font_family_combobox = ttk.Combobox(self, textvariable=self.font_family_var, values=['Helvetica', 'Arial', 'Times New Roman', 'Courier New'])
        self.save_button = ttk.Button(self, text="Save", command=self.handle_save_button)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.on_closing, bootstyle='secondary')
    
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.title_label.grid(row=0, columnspan=2, pady=(20,10))
        self.theme_label.grid(row=1, column=0, sticky='w', padx=20)
        self.theme_combobox.grid(row=1, column=1, sticky='ew', padx=20)
        self.font_size_label.grid(row=2, column=0, sticky='w', padx=20)
        self.font_size_combobox.grid(row=2, column=1, sticky='ew', padx=20)
        self.font_family_label.grid(row=3, column=0, sticky='w', padx=20)
        self.font_family_combobox.grid(row=3, column=1, sticky='ew', padx=20)
        self.save_button.grid(row=4, column=0, sticky='we', padx=5, pady=20)
        self.cancel_button.grid(row=4, column=1, sticky='we', padx=5, pady=20)

    def handle_save_button(self):
        theme = self.theme_var.get()
        self.parent.style.theme_use(theme)
        self.grab_release()
        response = messagebox.showinfo("Success", "Settings updated successfully!")
        self.destroy()

    def open_window(self):
        self.mainloop()

    def on_closing(self):
        self.grab_release()
        self.destroy()


root = MainWindow()
root.open_window()
