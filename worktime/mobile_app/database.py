from kivy.storage.jsonstore import JsonStore
from hashlib import sha256
import os
import sqlite3

class Database:
    def __init__(self):
        self.db_path = 'worktime.db'
        self.setup_database()
    
    def setup_database(self):
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create necessary tables if they don't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                company TEXT
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS work_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                login_time TEXT,
                logout_time TEXT,
                hours_worked REAL,
                company TEXT,
                date TEXT,
                FOREIGN KEY (employee_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def validate_login(self, username, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        password_hash = sha256(password.encode()).hexdigest()
        
        c.execute('SELECT id FROM users WHERE username=? AND password_hash=?',
                 (username, password_hash))
        result = c.fetchone()
        
        conn.close()
        return result is not None
    
    def save_login(self, username, company, login_time):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT id FROM users WHERE username=?', (username,))
        user_id = c.fetchone()[0]
        
        c.execute('''
            INSERT INTO work_hours (employee_id, login_time, company, date)
            VALUES (?, ?, ?, date('now'))
        ''', (user_id, login_time, company))
        
        conn.commit()
        conn.close()
    
    def save_logout(self, username, logout_time):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT id FROM users WHERE username=?', (username,))
        user_id = c.fetchone()[0]
        
        c.execute('''
            UPDATE work_hours 
            SET logout_time=?, 
                hours_worked=ROUND(
                    (strftime('%s', ?) - strftime('%s', login_time))/3600.0 - 0.75, 2
                )
            WHERE employee_id=? 
            AND date=date('now')
            AND logout_time IS NULL
        ''', (logout_time, logout_time, user_id))
        
        conn.commit()
        conn.close()
    
    def get_monthly_report(self, username, month=None, year=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT id FROM users WHERE username=?', (username,))
        user_id = c.fetchone()[0]
        
        if month and year:
            c.execute('''
                SELECT date, login_time, logout_time, hours_worked
                FROM work_hours
                WHERE employee_id=? 
                AND strftime('%m-%Y', date)=?
                ORDER BY date DESC
            ''', (user_id, f"{month:02d}-{year}"))
        else:
            c.execute('''
                SELECT date, login_time, logout_time, hours_worked
                FROM work_hours
                WHERE employee_id=?
                ORDER BY date DESC
                LIMIT 30
            ''', (user_id,))
        
        results = c.fetchall()
        conn.close()
        
        return results