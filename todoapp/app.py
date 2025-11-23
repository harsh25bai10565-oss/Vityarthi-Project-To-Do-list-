import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

class ModernTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Todo List App")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize data
        self.filename = "todo_data.json"
        self.tasks = []
        self.next_id = 1
        self.load_tasks()
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI
        self.create_gui()
        
        # Load initial tasks
        self.refresh_task_list()
    
    def setup_styles(self):
        """Configure modern styles for the application"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'secondary': '#34495e'
        }
        
        # Configure styles
        self.style.configure('Primary.TButton', 
                           background=self.colors['primary'],
                           foreground='white',
                           padding=(20, 10))
        
        self.style.configure('Success.TButton',
                           background=self.colors['success'],
                           foreground='white')
        
        self.style.configure('Danger.TButton',
                           background=self.colors['danger'],
                           foreground='white')
        
        self.style.configure('Warning.TButton',
                           background=self.colors['warning'],
                           foreground='white')
        
        self.style.configure('Custom.Treeview',
                           background=self.colors['light'],
                           fieldbackground=self.colors['light'])
        
        self.style.configure('Title.TLabel',
                           background=self.colors['dark'],
                           foreground='white',
                           font=('Arial', 16, 'bold'))
        
        self.style.configure('Stats.TLabel',
                           background=self.colors['secondary'],
                           foreground='white',
                           font=('Arial', 10))
    
    def create_gui(self):
        """Create the main GUI layout"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🚀 Modern Todo List", 
                              font=('Arial', 20, 'bold'),
                              bg=self.colors['dark'],
                              fg='white')
        title_label.pack(pady=20)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg=self.colors['dark'])
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Task input
        tk.Label(input_frame, text="New Task:", 
                bg=self.colors['dark'], fg='white', font=('Arial', 10)).grid(row=0, column=0, sticky='w')
        
        self.task_entry = tk.Entry(input_frame, width=40, font=('Arial', 12))
        self.task_entry.grid(row=1, column=0, padx=(0, 10), pady=5, sticky='ew')
        self.task_entry.bind('<Return>', lambda e: self.add_task_from_entry())
        
        # Priority selection
        tk.Label(input_frame, text="Priority:", 
                bg=self.colors['dark'], fg='white', font=('Arial', 10)).grid(row=0, column=1, sticky='w')
        
        self.priority_var = tk.StringVar(value="medium")
        priority_combo = ttk.Combobox(input_frame, 
                                    textvariable=self.priority_var,
                                    values=["low", "medium", "high"],
                                    state="readonly",
                                    width=10)
        priority_combo.grid(row=1, column=1, padx=(0, 10), pady=5)
        
        # Add task button
        add_btn = ttk.Button(input_frame, 
                           text="Add Task", 
                           command=self.add_task_from_entry,
                           style='Success.TButton')
        add_btn.grid(row=1, column=2, padx=5, pady=5)
        
        input_frame.columnconfigure(0, weight=1)
        
        # Controls Frame
        controls_frame = tk.Frame(self.root, bg=self.colors['dark'])
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls_frame, 
                  text="Mark Complete", 
                  command=self.mark_completed,
                  style='Primary.TButton').pack(side='left', padx=5)
        
        ttk.Button(controls_frame, 
                  text="Delete Task", 
                  command=self.delete_task,
                  style='Danger.TButton').pack(side='left', padx=5)
        
        ttk.Button(controls_frame, 
                  text="Edit Task", 
                  command=self.edit_task,
                  style='Warning.TButton').pack(side='left', padx=5)
        
        ttk.Button(controls_frame, 
                  text="Clear Completed", 
                  command=self.clear_completed,
                  style='Danger.TButton').pack(side='left', padx=5)
        
        # Filter Frame
        filter_frame = tk.Frame(self.root, bg=self.colors['dark'])
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        self.filter_var = tk.StringVar(value="all")
        tk.Radiobutton(filter_frame, text="All Tasks", variable=self.filter_var, 
                      value="all", command=self.refresh_task_list,
                      bg=self.colors['dark'], fg='white', selectcolor=self.colors['secondary']).pack(side='left', padx=10)
        tk.Radiobutton(filter_frame, text="Pending", variable=self.filter_var, 
                      value="pending", command=self.refresh_task_list,
                      bg=self.colors['dark'], fg='white', selectcolor=self.colors['secondary']).pack(side='left', padx=10)
        tk.Radiobutton(filter_frame, text="Completed", variable=self.filter_var, 
                      value="completed", command=self.refresh_task_list,
                      bg=self.colors['dark'], fg='white', selectcolor=self.colors['secondary']).pack(side='left', padx=10)
        
        # Task List Frame
        list_frame = tk.Frame(self.root, bg=self.colors['dark'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview for tasks
        columns = ('id', 'status', 'priority', 'task', 'created')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('status', text='Status')
        self.tree.heading('priority', text='Priority')
        self.tree.heading('task', text='Task Description')
        self.tree.heading('created', text='Created')
        
        # Define columns
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('status', width=80, anchor='center')
        self.tree.column('priority', width=80, anchor='center')
        self.tree.column('task', width=400)
        self.tree.column('created', width=120, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Statistics Frame
        stats_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=60)
        stats_frame.pack(fill='x', padx=10, pady=10)
        stats_frame.pack_propagate(False)
        
        self.stats_label = tk.Label(stats_frame, 
                                   text="Total: 0 | Completed: 0 | Pending: 0 | Rate: 0%",
                                   font=('Arial', 12),
                                   bg=self.colors['secondary'],
                                   fg='white')
        self.stats_label.pack(expand=True)
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.next_id = data.get('next_id', 1)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")
                self.tasks = []
                self.next_id = 1
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = {
                'tasks': self.tasks,
                'next_id': self.next_id,
                'last_saved': datetime.now().isoformat()
            }
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
    
    def add_task_from_entry(self):
        """Add task from the input entry"""
        description = self.task_entry.get().strip()
        if not description:
            messagebox.showwarning("Warning", "Please enter a task description!")
            return
        
        self.add_task(description, self.priority_var.get())
        self.task_entry.delete(0, tk.END)
    
    def add_task(self, description, priority="medium"):
        """Add a new task"""
        task = {
            'id': self.next_id,
            'description': description,
            'completed': False,
            'priority': priority,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'completed_at': None
        }
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        self.refresh_task_list()
        messagebox.showinfo("Success", f"Task added successfully! (ID: {task['id']})")
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter tasks based on selection
        filter_type = self.filter_var.get()
        if filter_type == "pending":
            display_tasks = [task for task in self.tasks if not task['completed']]
        elif filter_type == "completed":
            display_tasks = [task for task in self.tasks if task['completed']]
        else:
            display_tasks = self.tasks
        
        # Add tasks to treeview
        for task in display_tasks:
            status = "✅ Completed" if task['completed'] else "⏳ Pending"
            priority_icon = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}[task['priority']]
            
            self.tree.insert('', 'end', values=(
                task['id'],
                status,
                priority_icon,
                task['description'],
                task['created_at']
            ))
        
        # Update statistics
        self.update_statistics()
    
    def get_selected_task(self):
        """Get the currently selected task"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task first!")
            return None
        
        item = selection[0]
        task_id = int(self.tree.item(item)['values'][0])
        
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def mark_completed(self):
        """Mark selected task as completed"""
        task = self.get_selected_task()
        if task:
            if task['completed']:
                messagebox.showinfo("Info", "Task is already completed!")
            else:
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save_tasks()
                self.refresh_task_list()
                messagebox.showinfo("Success", "Task marked as completed!")
    
    def delete_task(self):
        """Delete selected task"""
        task = self.get_selected_task()
        if task:
            if messagebox.askyesno("Confirm", f"Delete task: {task['description']}?"):
                self.tasks = [t for t in self.tasks if t['id'] != task['id']]
                self.save_tasks()
                self.refresh_task_list()
                messagebox.showinfo("Success", "Task deleted successfully!")
    
    def edit_task(self):
        """Edit selected task"""
        task = self.get_selected_task()
        if task:
            new_description = simpledialog.askstring("Edit Task", 
                                                   "Enter new description:",
                                                   initialvalue=task['description'])
            if new_description and new_description.strip():
                task['description'] = new_description.strip()
                self.save_tasks()
                self.refresh_task_list()
                messagebox.showinfo("Success", "Task updated successfully!")
    
    def clear_completed(self):
        """Clear all completed tasks"""
        if not any(task['completed'] for task in self.tasks):
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
        
        if messagebox.askyesno("Confirm", "Delete all completed tasks?"):
            self.tasks = [task for task in self.tasks if not task['completed']]
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", "Completed tasks cleared!")
    
    def update_statistics(self):
        """Update statistics display"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        stats_text = f"📊 Total: {total} | ✅ Completed: {completed} | ⏳ Pending: {pending} | 📈 Rate: {completion_rate:.1f}%"
        self.stats_label.config(text=stats_text)

def main():
    """Main function to launch the application"""
    root = tk.Tk()
    app = ModernTodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()