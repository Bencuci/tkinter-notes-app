import sqlite3
from datetime import datetime
import os
import csv

class DatabaseCRUD:
    DB_NAME = "notes.db"

    # error handling and initializing database connection
    @staticmethod
    def _get_connection():
        try:
            conn = sqlite3.connect(DatabaseCRUD.DB_NAME)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    # create necessary tables
    @staticmethod
    def initialize_database():
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # notes table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT,
                        date_added TIMESTAMP,
                        date_last_edited TIMESTAMP
                    )
                ''')
                
                # settings table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        font_size INTEGER DEFAULT 12,
                        font_family TEXT DEFAULT 'Helvetica'
                    )
                ''')
                
                # insert default settings if does not exist
                cursor.execute('INSERT OR IGNORE INTO settings (id) VALUES (1)')
                
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error initializing database: {e}")
                return False
            finally:
                conn.close()
        return False

    # add new note, return id
    @staticmethod
    def add_note(title, content):
        try:
            DatabaseCRUD.validate_note_data(title, content)
        except InputValidationError as e:
            print(f"Validation Error: {e}")
            return False

        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('''
                    INSERT INTO notes (title, content, date_added, date_last_edited)
                    VALUES (?, ?, ?, ?)
                ''', (title, content, current_time, current_time))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False

    # edit the existing note
    @staticmethod
    def edit_note(note_id, title, content):
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('''
                    UPDATE notes 
                    SET title = ?, content = ?, date_last_edited = ?
                    WHERE id = ?
                ''', (title, content, current_time, note_id))
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False

    # delete note by id
    @staticmethod
    def delete_note(note_id):
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
                conn.commit()
                return cursor.rowcount > 0
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False

    # save font size
    @staticmethod
    def save_font_size(new_font_size):
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('UPDATE settings SET font_size = ? WHERE id = 1', (new_font_size,))
                conn.commit()
                return True
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False

    # save font family
    @staticmethod
    def save_font_family(new_font_family):
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('UPDATE settings SET font_family = ? WHERE id = 1', (new_font_family,))
                conn.commit()
                return True
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False

    # get all notes as list of dictionaries
    @staticmethod
    def get_notes():
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM notes ORDER BY date_last_edited DESC')
                columns = ['id', 'title', 'content', 'date_added', 'date_last_edited']
                notes = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return notes
            except sqlite3.Error:
                return []
            finally:
                conn.close()
        return []

    # get note by id
    @staticmethod
    def get_note(note_id):
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
                columns = ['id', 'title', 'content', 'date_added', 'date_last_edited']
                row = cursor.fetchone()
                return dict(zip(columns, row)) if row else None
            except sqlite3.Error:
                return None
            finally:
                conn.close()
        return None

    # get font size
    @staticmethod
    def get_font_size():
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT font_size FROM settings WHERE id = 1')
                result = cursor.fetchone()
                return result[0] if result else False
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False

    # get font family
    @staticmethod
    def get_font_family():
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT font_family FROM settings WHERE id = 1')
                result = cursor.fetchone()
                return result[0] if result else False
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False

    

    # title and content validation
    def validate_note_data(title, content):
        if not title or not isinstance(title, str) or len(title.strip()) == 0:
            raise InputValidationError("Title must be a non-empty string.")
        if not isinstance(content, str):
            raise InputValidationError("Content must be a string.")

    # settings input validation
    def validate_settings(font_size=None, font_family=None, save_location=None):
        if font_size is not None:
            if not isinstance(font_size, int) or font_size < 8 or font_size > 72:
                raise InputValidationError("Font size must be an integer between 8 and 72.")
        if font_family is not None:
            if not isinstance(font_family, str) or len(font_family.strip()) == 0:
                raise InputValidationError("Font family must be a non-empty string.")
        if save_location is not None:
            if not os.path.isdir(save_location):
                raise InputValidationError("Save location must be a valid directory path.")



class ExportTools:
    @staticmethod
    def export_notes_to_csv(file_path="notes_export.csv"):
        notes = DatabaseCRUD.get_notes()
        if not notes:
            print("No notes to export.")
            return False

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # write header
                writer.writerow(["ID", "Title", "Content", "Date Added", "Date Last Edited"])

                # write note rows
                for note in notes:
                    writer.writerow([
                        note['id'],
                        note['title'],
                        note['content'],
                        note['date_added'],
                        note['date_last_edited']
                    ])
            print(f"Notes successfully exported to {file_path}")
            return True
        except Exception as e:
            print(f"Error exporting notes: {e}")
            return False

# Validation Methods
# exception class for input validation errors
class InputValidationError(Exception):
    pass

