import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from back import TaskDatabase

class TaskTrackerApp:
    """GUI for Task Tracker Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title('Task Tracker App')
        self.root.geometry('700x600')
        self.root.configure(bg='#f0f0f0')
        
        self.db = TaskDatabase()
        self.selected_task_id = None
        
        self.setup_ui()
        self.refresh_tasks()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title Label
        title_label = tk.Label(
            self.root,
            text='Task Tracker',
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=10)
        
        # Input Frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill='x')
        
        # Task Title Input
        ttk.Label(input_frame, text='Task Title:').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.title_entry.bind('<Return>', lambda e: self.add_task())
        
        # Task Description Input
        ttk.Label(input_frame, text='Description:').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        self.desc_entry.bind('<Return>', lambda e: self.add_task())
        
        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, fill='x')
        
        add_btn = ttk.Button(button_frame, text='Add Task', command=self.add_task)
        add_btn.pack(side='left', padx=5)
        
        refresh_btn = ttk.Button(button_frame, text='Refresh', command=self.refresh_tasks)
        refresh_btn.pack(side='left', padx=5)
        
        # Tasks Display Frame
        display_frame = ttk.LabelFrame(self.root, text='Tasks', padding=10)
        display_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(display_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox for tasks
        self.task_listbox = tk.Listbox(
            display_frame,
            yscrollcommand=scrollbar.set,
            font=('Arial', 10),
            height=15,
            bg='white'
        )
        self.task_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)
        
        # Action Frame
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=10, padx=10, fill='x')
        
        complete_btn = ttk.Button(action_frame, text='Mark Complete', command=self.mark_complete)
        complete_btn.pack(side='left', padx=5)
        
        edit_btn = ttk.Button(action_frame, text='Edit Task', command=self.edit_task)
        edit_btn.pack(side='left', padx=5)
        
        delete_btn = ttk.Button(action_frame, text='Delete Task', command=self.delete_task)
        delete_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(action_frame, text='Clear Input', command=self.clear_input)
        clear_btn.pack(side='left', padx=5)
    
    def add_task(self):
        """Add a new task"""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        
        if not title:
            messagebox.showwarning('Input Error', 'Please enter a task title!')
            return
        
        self.db.add_task(title, description)
        messagebox.showinfo('Success', 'Task added successfully!')
        self.clear_input()
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """Refresh the task list display"""
        self.task_listbox.delete(0, tk.END)
        tasks = self.db.get_all_tasks()
        
        for task in tasks:
            task_id, title, description, status, created_date = task
            status_symbol = '✓' if status == 'Completed' else '○'
            display_text = f"[{status_symbol}] ID: {task_id} | {title} ({status})"
            self.task_listbox.insert(tk.END, display_text)
            
            # Color code by status
            if status == 'Completed':
                self.task_listbox.itemconfig(tk.END, {'bg': '#e8f5e9', 'fg': '#558b2f'})
    
    def on_task_select(self, event):
        """Handle task selection from listbox"""
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            tasks = self.db.get_all_tasks()
            if index < len(tasks):
                self.selected_task_id = tasks[index][0]
    
    def mark_complete(self):
        """Mark selected task as completed"""
        if self.selected_task_id is None:
            messagebox.showwarning('Selection Error', 'Please select a task!')
            return
        
        self.db.update_task_status(self.selected_task_id, 'Completed')
        messagebox.showinfo('Success', 'Task marked as completed!')
        self.refresh_tasks()
        self.selected_task_id = None
    
    def edit_task(self):
        """Edit selected task"""
        if self.selected_task_id is None:
            messagebox.showwarning('Selection Error', 'Please select a task!')
            return
        
        tasks = self.db.get_all_tasks()
        task = next((t for t in tasks if t[0] == self.selected_task_id), None)
        
        if not task:
            messagebox.showerror('Error', 'Task not found!')
            return
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title('Edit Task')
        edit_window.geometry('400x200')
        
        ttk.Label(edit_window, text='Title:').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        title_var = tk.StringVar(value=task[1])
        title_edit = ttk.Entry(edit_window, textvariable=title_var, width=30)
        title_edit.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(edit_window, text='Description:').grid(row=1, column=0, sticky='w', padx=10, pady=10)
        desc_var = tk.StringVar(value=task[2] or '')
        desc_edit = ttk.Entry(edit_window, textvariable=desc_var, width=30)
        desc_edit.grid(row=1, column=1, padx=10, pady=10)
        
        def save_changes():
            new_title = title_var.get().strip()
            new_desc = desc_var.get().strip()
            
            if not new_title:
                messagebox.showwarning('Input Error', 'Title cannot be empty!')
                return
            
            self.db.update_task(self.selected_task_id, new_title, new_desc)
            messagebox.showinfo('Success', 'Task updated successfully!')
            edit_window.destroy()
            self.refresh_tasks()
        
        save_btn = ttk.Button(edit_window, text='Save Changes', command=save_changes)
        save_btn.grid(row=2, column=0, columnspan=2, pady=20)
    
    def delete_task(self):
        """Delete selected task"""
        if self.selected_task_id is None:
            messagebox.showwarning('Selection Error', 'Please select a task!')
            return
        
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete this task?'):
            self.db.delete_task(self.selected_task_id)
            messagebox.showinfo('Success', 'Task deleted successfully!')
            self.refresh_tasks()
            self.selected_task_id = None
    
    def clear_input(self):
        """Clear input fields"""
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
