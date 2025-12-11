import sqlite3
from datetime import datetime

class TaskDatabase:
    """Handles all database operations for task management"""
    
    def __init__(self, db_name='tasks.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Initialize database and create tasks table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'Pending',
                created_date TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_task(self, title, description):
        """Add a new task to the database"""
        if not title.strip():
            return False
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO tasks (title, description, created_date)
            VALUES (?, ?, ?)
        ''', (title, description, created_date))
        conn.commit()
        conn.close()
        return True
    
    def get_all_tasks(self):
        """Retrieve all tasks from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, description, status, created_date FROM tasks ORDER BY id DESC')
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    
    def update_task_status(self, task_id, status):
        """Update the status of a task (Pending, Completed)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
        conn.commit()
        conn.close()
    
    def delete_task(self, task_id):
        """Delete a task from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
    
    def update_task(self, task_id, title, description):
        """Update task title and description"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks SET title = ?, description = ? WHERE id = ?
        ''', (title, description, task_id))
        conn.commit()
        conn.close()
