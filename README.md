# Task Tracker App - Complete Guide

## Project Overview
A desktop application to manage your daily tasks with a graphical user interface. Built with Python, SQLite, and Tkinter.

## Architecture

### Components:
1. **back.py** - Database layer (SQLite operations)
2. **front.py** - GUI layer (Tkinter interface)

## Installation & Setup

### Requirements:
- Python 3.x
- Tkinter (usually comes with Python)
- SQLite3 (included with Python)

### To Run:
```bash
python front.py
```

This will automatically create `tasks.db` in the same directory.

## Features

### 1. **Add Tasks**
   - Enter task title (required)
   - Add optional description
   - Press Enter or click "Add Task"

### 2. **View All Tasks**
   - Tasks displayed in a scrollable list
   - Shows: Task ID, Title, Status
   - Color-coded: Green for completed tasks

### 3. **Mark Tasks Complete**
   - Click task to select
   - Click "Mark Complete" button
   - Task status changes to "Completed"

### 4. **Edit Tasks**
   - Select a task
   - Click "Edit Task"
   - Modify title or description
   - Save changes

### 5. **Delete Tasks**
   - Select a task
   - Click "Delete Task"
   - Confirm deletion

### 6. **Refresh**
   - Update the task list without restarting

## Database Schema

**Table: tasks**
```
id (INTEGER) - Primary Key
title (TEXT) - Task title (required)
description (TEXT) - Task details (optional)
status (TEXT) - 'Pending' or 'Completed'
created_date (TEXT) - Creation timestamp
```

## Code Structure

### back.py - TaskDatabase Class
- `__init__()` - Initialize database
- `init_db()` - Create tables
- `add_task()` - Create new task
- `get_all_tasks()` - Fetch all tasks
- `update_task_status()` - Mark complete/pending
- `delete_task()` - Remove task
- `update_task()` - Edit task details

### front.py - TaskTrackerApp Class
- `setup_ui()` - Build interface
- `add_task()` - Handle new task input
- `refresh_tasks()` - Reload task list
- `on_task_select()` - Detect selection
- `mark_complete()` - Complete task
- `edit_task()` - Open edit dialog
- `delete_task()` - Remove task
- `clear_input()` - Reset fields

## Keyboard Shortcuts
- **Enter** in Title/Description fields - Add task quickly

## Tips
1. Select a task before performing actions (Mark Complete, Edit, Delete)
2. Use Refresh button to sync after closing/reopening the app
3. All timestamps are in YYYY-MM-DD HH:MM:SS format
4. Tasks are sorted newest first (by ID descending)

## Future Enhancements
- Task categories/labels
- Due dates with reminders
- Task priority levels
- Search/filter functionality
- Data export (CSV)
- Task recurrence
- Cloud sync

## Troubleshooting

**"No module named tkinter"**
- Linux: `sudo apt-get install python3-tk`
- macOS: Usually included with Python

**Database locked**
- Close the app completely and reopen

**Tasks not saving**
- Ensure write permissions in the app directory
- Check that `tasks.db` isn't corrupted
