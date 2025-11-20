from kivy.storage.jsonstore import JsonStore
from hashlib import sha256
import os
import sqlite3

class Database:
    def __init__(self):
        self.db_path = 'worktime\mobile_app\worktime.db'
        self.setup_database()
   
    def setup_database(self):
        # Ensure directory exists when running in environments with restricted cwd
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        # Use context manager for safe connection handling and enable foreign keys
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            c = conn.cursor()

            # Create necessary tables with a clean, readable schema
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    company TEXT,
                    new_user INTEGER DEFAULT 1
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
    
    def validate_user_login(self, username, password):
        password_hash = sha256(password.encode()).hexdigest()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM users WHERE username=? AND password_hash=?',
                      (username, password_hash))
            result = c.fetchone()
            return result is not None
    
    def validate_new_user(self, username):
        # Returns True if the user exists and is marked as a new user (new_user == 1)
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT new_user FROM users WHERE username=?', (username,))
            row = c.fetchone()
            if row is None:
                return False
            new_user_val = row[0] if isinstance(row, tuple) else row['new_user']
            return bool(new_user_val)
    
    def verify_current_password(self, username, current_password):
        current_password_hash = sha256(current_password.encode()).hexdigest()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT password_hash FROM users WHERE username=?', (username,))
            result = c.fetchone()
            return result is not None and result[0] == current_password_hash
    
    def update_new_password(self, username, new_password):
        new_password_hash = sha256(new_password.encode()).hexdigest()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE users SET password_hash=?, new_user=0 WHERE username=?',
                      (new_password_hash, username))
            conn.commit()
            c.execute('SELECT password_hash FROM users WHERE username=?', (username,))
            result = c.fetchone()
            return result is not None and result[0] == new_password_hash

    def create_user(self, username, password, company='', new_user=1):
        """Create a new user; returns True on success, False if username exists."""
        password_hash = sha256(password.encode()).hexdigest()
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('INSERT INTO users (username, password_hash, company, new_user) VALUES (?, ?, ?, ?)',
                          (username, password_hash, company, new_user))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_employee_id(self, username):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM users WHERE username=?', (username,))
            result = c.fetchone()
            return result[0] if result else None
    

    def save_login(self, username, company, login_time):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT employee_id FROM users WHERE username=?', (username,))
            row = c.fetchone()
            if not row:
                raise ValueError(f"User '{username}' not found")
            user_id = row[0]
            c.execute('''
                INSERT INTO work_hours (employee_id, login_time, company, date)
                VALUES (?, ?, ?, date('now'))
            ''', (user_id, login_time, company))
            conn.commit()
            return True
    
    def save_logout(self, username, logout_time):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM users WHERE username=?', (username,))
            row = c.fetchone()
            if not row:
                raise ValueError(f"User '{username}' not found")
            user_id = row[0]
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
            return True
          
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