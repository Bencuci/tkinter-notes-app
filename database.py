import sqlite3
from datetime import datetime
import os

class DatabaseCRUD:
    DB_NAME = "notes.db"

    @staticmethod
    def _get_connection():
        # error handling and initializing database connection
        try:
            conn = sqlite3.connect(DatabaseCRUD.DB_NAME)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

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
                        font_family TEXT DEFAULT 'Helvetica',
                        default_save_location TEXT DEFAULT ''
                    )
                ''')
                
                # insert default settings if not exists
                cursor.execute('INSERT OR IGNORE INTO settings (id) VALUES (1)')
                
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error initializing database: {e}")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def add_note(title, content):
        # add new note, return id
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

    @staticmethod
    def edit_note(note_id, title, content):
        # edit the existing note
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

    @staticmethod
    def delete_note(note_id):
        # delete note by id
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

    @staticmethod
    def save_font_size(new_font_size):
        # save font size
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

    @staticmethod
    def save_font_family(new_font_family):
        # save font family
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

    @staticmethod
    def save_default_save_location(new_default_save_location):
        # save "default save location" 
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('UPDATE settings SET default_save_location = ? WHERE id = 1', 
                             (new_default_save_location,))
                conn.commit()
                return True
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def get_notes():
        # get all notes as list of dictionaries
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

    @staticmethod
    def get_note(note_id):
        # get note by id
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

    @staticmethod
    def get_font_size():
        # get font size
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

    @staticmethod
    def get_font_family():
        # get font family
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

    @staticmethod
    def get_default_save_location():
        # get default save location
        conn = DatabaseCRUD._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT default_save_location FROM settings WHERE id = 1')
                result = cursor.fetchone()
                return result[0] if result else False
            except sqlite3.Error:
                return False
            finally:
                conn.close()
        return False