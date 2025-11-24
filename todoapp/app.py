import json
import os
from datetime import datetime

class CLITodoApp:
    def __init__(self):
        self.filename = "todo_data.json"
        self.tasks = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.next_id = data.get('next_id', 1)
            except Exception as e:
                print(f"Error loading tasks: {e}")
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
            print(f"Error saving tasks: {e}")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("           MODERN TODO LIST APP")
        print("="*50)
        print("1. View All Tasks")
        print("2. Add New Task")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Clear Completed Tasks")
        print("7. View Statistics")
        print("8. Exit")
        print("="*50)
    
    def display_tasks(self, task_list=None, show_completed=True):
        """Display tasks in a formatted way"""
        if task_list is None:
            task_list = self.tasks
        
        if not task_list:
            print("\nNo tasks found!")
            return
        
        print("\n" + "-"*80)
        print(f"{'ID':<4} {'Status':<12} {'Priority':<8} {'Task Description':<40} {'Created':<12}")
        print("-"*80)
        
        for task in task_list:
            if not show_completed and task['completed']:
                continue
                
            status = "✅" if task['completed'] else "⏳"
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[task['priority']]
            
            # Truncate long task descriptions
            description = task['description']
            if len(description) > 38:
                description = description[:35] + "..."
            
            print(f"{task['id']:<4} {status:<12} {priority_icon:<8} {description:<40} {task['created_at']:<12}")
        
        print("-"*80")
    
    def add_task(self):
        """Add a new task"""
        print("\n--- Add New Task ---")
        description = input("Enter task description: ").strip()
        
        if not description:
            print("Task description cannot be empty!")
            return
        
        print("\nSelect priority:")
        print("1. 🔴 High")
        print("2. 🟡 Medium")
        print("3. 🟢 Low")
        
        priority_choice = input("Enter choice (1-3, default 2): ").strip()
        priority_map = {"1": "high", "2": "medium", "3": "low"}
        priority = priority_map.get(priority_choice, "medium")
        
        task = {
            'id': self.next_id,
            'description': description,
            'completed': False,
            'priority': priority,
            'created_at': datetime.now().strftime("%Y-%m-%d"),
            'completed_at': None
        }
        
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        print(f"\n✅ Task added successfully! (ID: {task['id']})")
    
    def mark_completed(self):
        """Mark a task as completed"""
        if not self.tasks:
            print("\nNo tasks available!")
            return
        
        self.display_tasks(show_completed=False)
        try:
            task_id = int(input("\nEnter task ID to mark as completed: "))
        except ValueError:
            print("Please enter a valid number!")
            return
        
        task = self.find_task_by_id(task_id)
        if task:
            if task['completed']:
                print("Task is already completed!")
            else:
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save_tasks()
                print("✅ Task marked as completed!")
        else:
            print("Task not found!")
    
    def delete_task(self):
        """Delete a task"""
        if not self.tasks:
            print("\nNo tasks available!")
            return
        
        self.display_tasks()
        try:
            task_id = int(input("\nEnter task ID to delete: "))
        except ValueError:
            print("Please enter a valid number!")
            return
        
        task = self.find_task_by_id(task_id)
        if task:
            confirm = input(f"Are you sure you want to delete '{task['description']}'? (y/n): ").lower()
            if confirm == 'y':
                self.tasks = [t for t in self.tasks if t['id'] != task_id]
                self.save_tasks()
                print("✅ Task deleted successfully!")
        else:
            print("Task not found!")
    
    def edit_task(self):
        """Edit a task"""
        if not self.tasks:
            print("\nNo tasks available!")
            return
        
        self.display_tasks()
        try:
            task_id = int(input("\nEnter task ID to edit: "))
        except ValueError:
            print("Please enter a valid number!")
            return
        
        task = self.find_task_by_id(task_id)
        if task:
            print(f"\nCurrent description: {task['description']}")
            new_description = input("Enter new description: ").strip()
            
            if new_description:
                task['description'] = new_description
                self.save_tasks()
                print("✅ Task updated successfully!")
            else:
                print("Task description cannot be empty!")
        else:
            print("Task not found!")
    
    def clear_completed(self):
        """Clear all completed tasks"""
        completed_tasks = [task for task in self.tasks if task['completed']]
        
        if not completed_tasks:
            print("\nNo completed tasks to clear!")
            return
        
        print(f"\nFound {len(completed_tasks)} completed tasks:")
        self.display_tasks(completed_tasks)
        
        confirm = input("\nAre you sure you want to delete all completed tasks? (y/n): ").lower()
        if confirm == 'y':
            self.tasks = [task for task in self.tasks if not task['completed']]
            self.save_tasks()
            print(f"✅ Cleared {len(completed_tasks)} completed tasks!")
    
    def show_statistics(self):
        """Show task statistics"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        print("\n--- Statistics ---")
        print(f"📊 Total Tasks: {total}")
        print(f"✅ Completed: {completed}")
        print(f"⏳ Pending: {pending}")
        print(f"📈 Completion Rate: {completion_rate:.1f}%")
        
        # Priority breakdown
        priorities = {'high': 0, 'medium': 0, 'low': 0}
        for task in self.tasks:
            if not task['completed']:
                priorities[task['priority']] += 1
        
        print(f"\n📋 Pending by Priority:")
        print(f"   🔴 High: {priorities['high']}")
        print(f"   🟡 Medium: {priorities['medium']}")
        print(f"   🟢 Low: {priorities['low']}")
    
    def find_task_by_id(self, task_id):
        """Find a task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def run(self):
        """Main application loop"""
        print("Welcome to the Modern Todo List App!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-8): ").strip()
                
                if choice == '1':
                    self.display_tasks()
                elif choice == '2':
                    self.add_task()
                elif choice == '3':
                    self.mark_completed()
                elif choice == '4':
                    self.delete_task()
                elif choice == '5':
                    self.edit_task()
                elif choice == '6':
                    self.clear_completed()
                elif choice == '7':
                    self.show_statistics()
                elif choice == '8':
                    print("\nThank you for using the Todo List App! Goodbye! 👋")
                    break
                else:
                    print("Invalid choice! Please enter a number between 1-8.")
            
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Goodbye! 👋")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

def main():
    """Main function to launch the application"""
    app = CLITodoApp()
    app.run()

if __name__ == "__main__":
    main()
