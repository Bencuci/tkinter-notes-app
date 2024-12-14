import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from window_utils import center_window
from database import DatabaseCRUD
from langpack import I18N

temp_tk = tk.Tk()
SCREEN_WIDTH = temp_tk.winfo_screenwidth()
SCREEN_HEIGHT = temp_tk.winfo_screenheight()
temp_tk.destroy()

THEMES = ['superhero', 'darkly', 'solar', 'cyborg', 'vapor', 'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']

DatabaseCRUD.initialize_database()
lang = I18N(DatabaseCRUD.get_language())

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(lang.trn.get("notes_app"))
        self.style = ttk.Style(theme=DatabaseCRUD.get_theme())
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 400, 150)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
        self.child_windows = {}
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text=lang.trn.get("welcome"), font=("Helvetica", 16))
        self.new_note_button = ttk.Button(self, text=lang.trn.get("new_note"), command=self.handle_new_note_button)
        self.list_notes_button = ttk.Button(self, text=lang.trn.get("list_notes"), command=self.handle_list_notes_button)
        self.settings_button = ttk.Button(self, text=lang.trn.get("settings"), command=self.handle_settings_button, bootstyle='secondary')
        self.help_button = ttk.Button(self, text=lang.trn.get("help"), command=self.handle_help_button, bootstyle='info')
        self.exit_button = ttk.Button(self, text=lang.trn.get("exit"), command=self.quit, bootstyle='danger')

    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.title_label.grid(row=0, columnspan=2, pady=10)
        self.new_note_button.grid(row=1, column=0, pady=5, padx=5, sticky='nswe')
        self.list_notes_button.grid(row=1, column=1, pady=5, padx=5, sticky='nswe')
        self.settings_button.grid(row=2, column=0, pady=5, padx=5, sticky='nswe')
        self.help_button.grid(row=2, column=1, pady=5, padx=5, sticky='nswe')
        self.exit_button.grid(row=3, column=0, pady=5, padx=5, sticky='nswe', columnspan=2)

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

    def handle_help_button(self):
        messagebox.showinfo("Help", lang.trn.get("help_text").replace("\\n", "\n"))

    def handle_list_notes_button(self):
        if 'list_notes' in self.child_windows and self.child_windows['list_notes'].winfo_exists():
            self.child_windows['list_notes'].lift()
            self.child_windows['list_notes'].focus_force()
        else:
            list_notes_window = ListNotesWindow(self)
            self.child_windows['list_notes'] = list_notes_window

    def open_window(self):
        self.mainloop()

    def update_translations(self):
        self.title(lang.trn.get("notes_app"))
        self.title_label.config(text=lang.trn.get("welcome"))
        self.new_note_button.config(text=lang.trn.get("new_note"))
        self.list_notes_button.config(text=lang.trn.get("list_notes"))
        self.settings_button.config(text=lang.trn.get("settings"))
        self.help_button.config(text=lang.trn.get("help"))
        self.exit_button.config(text=lang.trn.get("exit"))

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
        self.title_label = ttk.Label(self, text=lang.trn.get("add_new_note"), font=("Helvetica", 16))
        self.note_title_label = ttk.Label(self, text=lang.trn.get("title"))
        self.note_title = ttk.Entry(self, font=(DatabaseCRUD.get_font_family(), DatabaseCRUD.get_font_size()))
        self.note_content_label = ttk.Label(self, text=lang.trn.get("content"))
        self.note_content= tk.Text(self, font=(DatabaseCRUD.get_font_family(), DatabaseCRUD.get_font_size()))
        self.save_button = ttk.Button(self, text=lang.trn.get("save"), command=self.handle_save_button)
        self.cancel_button = ttk.Button(self, text=lang.trn.get("cancel"), command=self.on_closing, bootstyle='secondary')
    
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.title_label.grid(row=0, columnspan=2, pady=(20,10))
        self.note_title_label.grid(row=1, column=0, sticky='w', padx=20)
        self.note_title.grid(row=2, columnspan=2, sticky='ew', padx=20)
        self.note_content_label.grid(row=3, column=0, sticky='w', padx=20)
        self.note_content.grid(row=4, columnspan=2, sticky='nsew', padx=20)
        self.save_button.grid(row=5, column=0, sticky='e', padx=5, pady=20)
        self.cancel_button.grid(row=5, column=1, sticky='w', padx=5, pady=20)

    def handle_save_button(self):
        title = self.note_title.get()
        content = self.note_content.get("1.0", tk.END)
        success = DatabaseCRUD.add_note(title, content)
        self.grab_release()
        if not success:
            messagebox.showerror("Error", lang.trn.get("failed_to_save"))
        else:
            messagebox.showinfo("Success", lang.trn.get("saved_successfully")) 
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
        self.title_label = ttk.Label(self, text=lang.trn.get("your_notes"), font=("Helvetica", 16))
        self.notes_list = tk.Listbox(self, height=10, width=40)
        self.edit_button = ttk.Button(self, text=lang.trn.get("edit_note"), command=self.handle_edit_button)
        self.delete_button = ttk.Button(self, text=lang.trn.get("delete_note"), command=self.handle_delete_button)
        self.go_back_button = ttk.Button(self, text=lang.trn.get("go_back"), command=self.on_closing, bootstyle='secondary')
    
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
            messagebox.showerror("Error", "No note selected!")

    def handle_delete_button(self):
        selected_note = self.notes_list.curselection()
        if selected_note:
            confirm = messagebox.askyesno(lang.trn.get("delete_note"), lang.trn.get("are_you_sure_delete"))
            if not confirm:
                return
            else:
                note = self.notes_list.get(selected_note)
                success = DatabaseCRUD.delete_note(self.note_ids[note])
                if success:
                    messagebox.showinfo(lang.trn.get("success"), lang.trn.get("deleted_successfully"))
                else:
                    messagebox.showerror("Error", lang.trn.get("failed_to_delete"))
                self.notes_list.delete(selected_note)
        else:
            messagebox.showerror("Error", lang.trn.get("no_note_selected"))

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
        self.title(lang.trn.get("edit_note"))
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
        self.title_label = ttk.Label(self, text=lang.trn.get("edit_note"), font=("Helvetica", 16))
        self.note_title_label = ttk.Label(self, text=lang.trn.get("title"))
        self.note_title = ttk.Entry(self, font=(DatabaseCRUD.get_font_family(), DatabaseCRUD.get_font_size()))
        self.note_content_label = ttk.Label(self, text=lang.trn.get("content"))
        self.note_content= tk.Text(self, font=(DatabaseCRUD.get_font_family(), DatabaseCRUD.get_font_size()))
        self.save_button = ttk.Button(self, text=lang.trn.get("save"), command=self.handle_save_button)
        self.cancel_button = ttk.Button(self, text=lang.trn.get("cancel"), command=self.on_closing, bootstyle='secondary')
    
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.title_label.grid(row=0, columnspan=2, pady=(20,10))
        self.note_title_label.grid(row=1, column=0, sticky='w', padx=20)
        self.note_title.grid(row=2, columnspan=2, sticky='ew', padx=20)
        self.note_content_label.grid(row=3, column=0, sticky='w', padx=20)
        self.note_content.grid(row=4, columnspan=2, sticky='nsew', padx=20)
        self.save_button.grid(row=5, column=0, sticky='e', padx=5, pady=20)
        self.cancel_button.grid(row=5, column=1, sticky='w', padx=5, pady=20)

    def handle_save_button(self):
        title = self.note_title.get()
        content = self.note_content.get("1.0", tk.END)
        success = DatabaseCRUD.edit_note(self.note["id"], title, content)
        if success:
            messagebox.showinfo(lang.trn.get("success"), lang.trn.get("saved_successfully"))
        else:
            messagebox.showerror("Error", lang.trn.get("failed_to_save"))
        self.grab_release()
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
        self.title(lang.trn.get("settings"))
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        dimensions = center_window(SCREEN_WIDTH, SCREEN_HEIGHT, 450, 225)
        self.geometry(dimensions)
        self.create_widgets()
        self.create_layout()
    
    def create_widgets(self):
        self.title_label = ttk.Label(self, text=lang.trn.get("settings"), font=("Helvetica", 16))
        self.language_label = ttk.Label(self, text=lang.trn.get("language_label"))
        self.language_var = tk.StringVar()
        self.language_var.set(lang.trn.get("language"))
        self.language_combobox = ttk.Combobox(self, textvariable=self.language_var, values=['English', 'Türkçe'], state='readonly')
        self.theme_label = ttk.Label(self, text=lang.trn.get("theme"))
        self.theme_var = tk.StringVar()
        self.theme_var.set(self.parent.style.theme_use())
        self.font_size_label = ttk.Label(self, text=lang.trn.get("font_size"))
        self.font_size_var = tk.StringVar()
        self.font_size_var.set(str(DatabaseCRUD.get_font_size()))
        self.font_family_label = ttk.Label(self, text=lang.trn.get("font_family"))
        self.font_family_var = tk.StringVar()
        self.font_family_var.set(str(DatabaseCRUD.get_font_family()))
        self.theme_combobox = ttk.Combobox(self, textvariable=self.theme_var, values=THEMES, state='readonly')
        self.theme_combobox.bind("<<ComboboxSelected>>", self.handle_theme_selection)
        self.font_size_combobox = ttk.Combobox(self, textvariable=self.font_size_var, values=['10', '12', '14', '16', '18', '20'])
        self.font_family_combobox = ttk.Combobox(self, textvariable=self.font_family_var, values=['Helvetica', 'Arial', 'Times New Roman', 'Courier New'], state='readonly')
        self.save_button = ttk.Button(self, text=lang.trn.get("save"), command=self.handle_save_button)
        self.cancel_button = ttk.Button(self, text=lang.trn.get("cancel"), command=self.on_closing, bootstyle='secondary')
    
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.title_label.grid(row=0, columnspan=2, pady=(20,10))
        self.language_label.grid(row=1, column=0, sticky='w', padx=20)
        self.language_combobox.grid(row=1, column=1, sticky='ew', padx=20)
        self.theme_label.grid(row=2, column=0, sticky='w', padx=20)
        self.theme_combobox.grid(row=2, column=1, sticky='ew', padx=20)
        self.font_size_label.grid(row=3, column=0, sticky='w', padx=20)
        self.font_size_combobox.grid(row=3, column=1, sticky='ew', padx=20)
        self.font_family_label.grid(row=4, column=0, sticky='w', padx=20)
        self.font_family_combobox.grid(row=4, column=1, sticky='ew', padx=20)
        self.save_button.grid(row=5, column=0, sticky='we', padx=5, pady=20)
        self.cancel_button.grid(row=5, column=1, sticky='we', padx=5, pady=20)

    def handle_theme_selection(self, event):
        theme = self.theme_var.get()
        self.parent.style.theme_use(theme)

    def handle_save_button(self):
        global lang 
        if self.language_var.get() == "Türkçe":
            lang = I18N("tr")
            DatabaseCRUD.save_language("tr")
        elif self.language_var.get() == "English":
            lang = I18N("en")
            DatabaseCRUD.save_language("en")
        else:
            lang = I18N("en") # default language is English
            DatabaseCRUD.save_language("en")
        font_size = int(self.font_size_var.get())
        font_family = self.font_family_var.get()
        theme = self.theme_var.get()
        self.parent.style.theme_use(theme)
        success_font_size = DatabaseCRUD.save_font_size(font_size)
        if not success_font_size:
            messagebox.showerror("Error", lang.trn.get("failed_font_size"))
        success_font_family = DatabaseCRUD.save_font_family(font_family)
        if not success_font_family:
            messagebox.showerror("Error", lang.trn.get("failed_font_family"))
        success_theme = DatabaseCRUD.save_theme(theme)
        if not success_theme:
            messagebox.showerror("Error", lang.trn.get("failed_theme"))
        if success_font_size and success_font_family and success_theme:
            messagebox.showinfo(lang.trn.get("success"), lang.trn.get("settings_saved_successfully"))
        self.grab_release()
        self.destroy()
        self.parent.update_translations()

    def open_window(self):
        self.mainloop()

    def on_closing(self):
        self.grab_release()
        self.destroy()

root = MainWindow()
root.open_window()
