import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from back import TaskDatabase

class TaskTrackerApp:
    """GUI for Task Tracker Application with Modern UI"""
    
    # Color Scheme
    PRIMARY_COLOR = '#2E7D32'      # Green
    SECONDARY_COLOR = '#FFA726'    # Orange
    ACCENT_COLOR = '#1976D2'       # Blue
    BG_COLOR = '#F5F5F5'           # Light Gray
    CARD_COLOR = '#FFFFFF'         # White
    TEXT_COLOR = '#212121'         # Dark Gray
    SUCCESS_COLOR = '#4CAF50'      # Light Green
    PENDING_COLOR = '#FFC107'      # Amber
    COMPLETED_COLOR = '#81C784'    # Green
    
    def __init__(self, root):
        self.root = root
        self.root.title('Task Tracker')
        self.root.geometry('900x700')
        self.root.configure(bg=self.BG_COLOR)
        
        # Configure styles
        self.setup_styles()
        
        self.db = TaskDatabase()
        self.selected_task_id = None
        self.tasks_cache = []
        
        self.setup_ui()
        self.refresh_tasks()
    
    def setup_styles(self):
        """Configure custom ttk styles"""
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Accent.TButton', font=('Segoe UI', 9))
        style.configure('Action.TButton', font=('Segoe UI', 9))
        
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'))
        style.configure('Normal.TLabel', font=('Segoe UI', 10))
    
    def setup_ui(self):
        """Setup the modern user interface"""
        # ===== HEADER SECTION =====
        header_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text='📋 Task Tracker',
            font=('Segoe UI', 22, 'bold'),
            bg=self.PRIMARY_COLOR,
            fg='white'
        )
        title_label.pack(pady=15)
        
        # ===== MAIN CONTENT FRAME =====
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # ===== INPUT SECTION =====
        input_frame = tk.Frame(main_frame, bg=self.CARD_COLOR, relief='flat', bd=1)
        input_frame.pack(fill='x', pady=(0, 15))
        
        input_frame.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        input_label = tk.Label(
            input_frame,
            text='➕ Add New Task',
            font=('Segoe UI', 12, 'bold'),
            bg=self.CARD_COLOR,
            fg=self.PRIMARY_COLOR
        )
        input_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        # Input container
        input_container = tk.Frame(input_frame, bg=self.CARD_COLOR)
        input_container.pack(fill='x', padx=15, pady=(5, 15))
        
        # Title input
        tk.Label(input_container, text='Title:', font=('Segoe UI', 10), bg=self.CARD_COLOR, fg=self.TEXT_COLOR).grid(row=0, column=0, sticky='w', pady=5, padx=(0, 10))
        self.title_entry = tk.Entry(input_container, font=('Segoe UI', 10), width=45, relief='solid', bd=1)
        self.title_entry.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        self.title_entry.bind('<Return>', lambda e: self.add_task())
        
        # Description input
        tk.Label(input_container, text='Description:', font=('Segoe UI', 10), bg=self.CARD_COLOR, fg=self.TEXT_COLOR).grid(row=1, column=0, sticky='w', pady=5, padx=(0, 10))
        self.desc_entry = tk.Entry(input_container, font=('Segoe UI', 10), width=45, relief='solid', bd=1)
        self.desc_entry.grid(row=1, column=1, sticky='ew', padx=(0, 10))
        self.desc_entry.bind('<Return>', lambda e: self.add_task())
        
        # Configure grid weights
        input_container.columnconfigure(1, weight=1)
        
        # Action buttons for input
        button_container = tk.Frame(input_container, bg=self.CARD_COLOR)
        button_container.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        
        add_btn = tk.Button(
            button_container,
            text='Add Task',
            command=self.add_task,
            bg=self.PRIMARY_COLOR,
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        add_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(
            button_container,
            text='Clear',
            command=self.clear_input,
            bg='#E0E0E0',
            fg=self.TEXT_COLOR,
            font=('Segoe UI', 10),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        clear_btn.pack(side='left')
        
        # ===== STATS SECTION =====
        stats_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        stats_frame.pack(fill='x', pady=(0, 15))
        
        self.total_label = tk.Label(stats_frame, text='Total: 0', font=('Segoe UI', 10, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.total_label.pack(side='left', padx=(0, 20))
        
        self.pending_label = tk.Label(stats_frame, text='Pending: 0', font=('Segoe UI', 10), bg=self.BG_COLOR, fg=self.PENDING_COLOR)
        self.pending_label.pack(side='left', padx=(0, 20))
        
        self.completed_label = tk.Label(stats_frame, text='Completed: 0', font=('Segoe UI', 10), bg=self.BG_COLOR, fg=self.COMPLETED_COLOR)
        self.completed_label.pack(side='left')
        
        # ===== TASKS DISPLAY SECTION =====
        tasks_header_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        tasks_header_frame.pack(fill='x', pady=(0, 10))
        
        tasks_label = tk.Label(
            tasks_header_frame,
            text='📝 Your Tasks',
            font=('Segoe UI', 12, 'bold'),
            bg=self.BG_COLOR,
            fg=self.PRIMARY_COLOR
        )
        tasks_label.pack(side='left')
        
        refresh_btn = tk.Button(
            tasks_header_frame,
            text='🔄 Refresh',
            command=self.refresh_tasks,
            bg=self.ACCENT_COLOR,
            fg='white',
            font=('Segoe UI', 9),
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        refresh_btn.pack(side='right')
        
        # Tasks display with frame
        display_frame = tk.Frame(main_frame, bg=self.CARD_COLOR, relief='flat', bd=1)
        display_frame.pack(fill='both', expand=True)
        display_frame.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(display_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox for tasks
        self.task_listbox = tk.Listbox(
            display_frame,
            yscrollcommand=scrollbar.set,
            font=('Segoe UI', 10),
            bg=self.CARD_COLOR,
            fg=self.TEXT_COLOR,
            relief='flat',
            bd=0,
            highlightthickness=0,
            activestyle='none',
            selectmode='single'
        )
        self.task_listbox.pack(fill='both', expand=True, padx=1, pady=1)
        scrollbar.config(command=self.task_listbox.yview)
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)
        
        # ===== ACTION BUTTONS SECTION =====
        action_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        action_frame.pack(fill='x', pady=(15, 0))
        
        # Complete button
        complete_btn = tk.Button(
            action_frame,
            text='✓ Mark Complete',
            command=self.mark_complete,
            bg=self.SUCCESS_COLOR,
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        complete_btn.pack(side='left', padx=(0, 10))
        
        # Edit button
        edit_btn = tk.Button(
            action_frame,
            text='✏️ Edit',
            command=self.edit_task,
            bg=self.SECONDARY_COLOR,
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        edit_btn.pack(side='left', padx=(0, 10))
        
        # Delete button
        delete_btn = tk.Button(
            action_frame,
            text='🗑️ Delete',
            command=self.delete_task,
            bg='#E53935',
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        delete_btn.pack(side='left')
    
    def add_task(self):
        """Add a new task"""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        
        if not title:
            messagebox.showwarning('Input Error', 'Please enter a task title!')
            return
        
        self.db.add_task(title, description)
        messagebox.showinfo('Success', '✓ Task added successfully!', icon='info')
        self.clear_input()
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """Refresh the task list display with improved formatting"""
        self.task_listbox.delete(0, tk.END)
        self.tasks_cache = self.db.get_all_tasks()
        
        total = len(self.tasks_cache)
        pending = sum(1 for t in self.tasks_cache if t[3] == 'Pending')
        completed = sum(1 for t in self.tasks_cache if t[3] == 'Completed')
        
        # Update stats
        self.total_label.config(text=f'Total: {total}')
        self.pending_label.config(text=f'Pending: {pending}')
        self.completed_label.config(text=f'Completed: {completed}')
        
        # Display tasks with better formatting
        for task in self.tasks_cache:
            task_id, title, description, status, created_date = task
            
            # Format display text
            status_icon = '✓' if status == 'Completed' else '○'
            desc_preview = f' • {description[:35]}...' if description else ''
            date_str = created_date.split()[0] if created_date else ''
            
            display_text = f"{status_icon} [{task_id}] {title}{desc_preview}"
            self.task_listbox.insert(tk.END, display_text)
            
            # Color code by status
            if status == 'Completed':
                self.task_listbox.itemconfig(tk.END, {'bg': '#E8F5E9', 'fg': '#2E7D32'})
            else:
                self.task_listbox.itemconfig(tk.END, {'bg': '#FFF9C4', 'fg': '#F57F17'})
    
    def on_task_select(self, event):
        """Handle task selection from listbox"""
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.tasks_cache):
                self.selected_task_id = self.tasks_cache[index][0]
    
    def mark_complete(self):
        """Mark selected task as completed"""
        if self.selected_task_id is None:
            messagebox.showwarning('Selection Error', 'Please select a task first!')
            return
        
        self.db.update_task_status(self.selected_task_id, 'Completed')
        messagebox.showinfo('Success', '✓ Task marked as completed!')
        self.refresh_tasks()
        self.selected_task_id = None
    
    def edit_task(self):
        """Edit selected task with modern dialog"""
        if self.selected_task_id is None:
            messagebox.showwarning('Selection Error', 'Please select a task first!')
            return
        
        task = next((t for t in self.tasks_cache if t[0] == self.selected_task_id), None)
        
        if not task:
            messagebox.showerror('Error', 'Task not found!')
            return
        
        # Create modern edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title('Edit Task')
        edit_window.geometry('500x280')
        edit_window.configure(bg=self.BG_COLOR)
        edit_window.resizable(False, False)
        
        # Header
        header = tk.Frame(edit_window, bg=self.SECONDARY_COLOR, height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text='✏️ Edit Task',
            font=('Segoe UI', 14, 'bold'),
            bg=self.SECONDARY_COLOR,
            fg='white'
        )
        header_label.pack(pady=10)
        
        # Content frame
        content_frame = tk.Frame(edit_window, bg=self.BG_COLOR)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title input
        tk.Label(content_frame, text='Task Title:', font=('Segoe UI', 10, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).grid(row=0, column=0, sticky='w', pady=(0, 5))
        title_var = tk.StringVar(value=task[1])
        title_edit = tk.Entry(content_frame, textvariable=title_var, font=('Segoe UI', 10), relief='solid', bd=1, width=40)
        title_edit.grid(row=1, column=0, sticky='ew', pady=(0, 15))
        
        # Description input
        tk.Label(content_frame, text='Description:', font=('Segoe UI', 10, 'bold'), bg=self.BG_COLOR, fg=self.TEXT_COLOR).grid(row=2, column=0, sticky='w', pady=(0, 5))
        desc_var = tk.StringVar(value=task[2] or '')
        desc_edit = tk.Entry(content_frame, textvariable=desc_var, font=('Segoe UI', 10), relief='solid', bd=1, width=40)
        desc_edit.grid(row=3, column=0, sticky='ew')
        
        content_frame.columnconfigure(0, weight=1)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg=self.BG_COLOR)
        button_frame.grid(row=4, column=0, sticky='ew', pady=(20, 0))
        
        def save_changes():
            new_title = title_var.get().strip()
            new_desc = desc_var.get().strip()
            
            if not new_title:
                messagebox.showwarning('Input Error', 'Title cannot be empty!')
                return
            
            self.db.update_task(self.selected_task_id, new_title, new_desc)
            messagebox.showinfo('Success', '✓ Task updated successfully!')
            edit_window.destroy()
            self.refresh_tasks()
        
        save_btn = tk.Button(
            button_frame,
            text='Save Changes',
            command=save_changes,
            bg=self.SUCCESS_COLOR,
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        save_btn.pack(side='left', padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text='Cancel',
            command=edit_window.destroy,
            bg='#E0E0E0',
            fg=self.TEXT_COLOR,
            font=('Segoe UI', 10),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        cancel_btn.pack(side='left')
    
    def delete_task(self):
        """Delete selected task with confirmation"""
        if self.selected_task_id is None:
            messagebox.showwarning('Selection Error', 'Please select a task first!')
            return
        
        task = next((t for t in self.tasks_cache if t[0] == self.selected_task_id), None)
        if not task:
            return
        
        result = messagebox.askyesno(
            'Confirm Delete',
            f'Are you sure you want to delete:\n"{task[1]}"?',
            icon='warning'
        )
        
        if result:
            self.db.delete_task(self.selected_task_id)
            messagebox.showinfo('Success', '✓ Task deleted successfully!')
            self.refresh_tasks()
            self.selected_task_id = None
    
    def clear_input(self):
        """Clear input fields"""
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.title_entry.focus()

def main():
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
