Modern Todo List App - CLI Version
A simple and efficient command-line Todo List application built with Python. Manage your tasks with priority levels, track completion statistics, and persist your data automatically.

Features
✅ Add tasks with priority levels (High, Medium, Low)

📋 View tasks with visual status indicators

✏️ Edit existing tasks

🗑️ Delete tasks with confirmation

✅ Mark tasks as completed

📊 View statistics and completion rates

💾 Automatic data persistence to JSON file

🎯 Priority-based organization

🧹 Clear completed tasks in bulk

Installation
Ensure you have Python 3.6 or higher installed

Download the todo_cli.py file

No additional dependencies required!

Quick Start
bash
python todo_cli.py
Usage
Main Menu Options
text
1. View All Tasks      - Display all tasks with their current status
2. Add New Task        - Create a new task with description and priority
3. Mark Task as Completed - Change task status to completed
4. Delete Task         - Remove a specific task
5. Edit Task           - Modify task description
6. Clear Completed Tasks - Remove all completed tasks at once
7. View Statistics     - Show completion rates and priority breakdown
8. Exit                - Safely exit the application
Task Priority Levels
🔴 High - Important and urgent tasks

🟡 Medium - Important but not urgent tasks

🟢 Low - Nice-to-have tasks

Task Status Indicators
⏳ Pending - Task not yet completed

✅ Completed - Task finished

Data Storage
All tasks are automatically saved to todo_data.json in the same directory. The file contains:

Task list with descriptions, priorities, and status

Next available task ID

Last saved timestamp

Example Data Format
json
{
  "tasks": [
    {
      "id": 1,
      "description": "Finish project report",
      "completed": false,
      "priority": "high",
      "created_at": "2024-01-15",
      "completed_at": null
    }
  ],
  "next_id": 2,
  "last_saved": "2024-01-15T10:30:00.000000"
}
Example Session
text
==================================================
           MODERN TODO LIST APP
==================================================
1. View All Tasks
2. Add New Task
3. Mark Task as Completed
4. Delete Task
5. Edit Task
6. Clear Completed Tasks
7. View Statistics
8. Exit
==================================================

Enter your choice (1-8): 2

--- Add New Task ---
Enter task description: Complete Python project

Select priority:
1. 🔴 High
2. 🟡 Medium
3. 🟢 Low

Enter choice (1-3, default 2): 1

✅ Task added successfully! (ID: 1)
Keyboard Shortcuts
Ctrl + C - Safely exit the application at any time

Input numbers 1-8 for menu navigation

Error Handling
Invalid input validation

Task not found handling

File read/write error recovery

Graceful interruption handling

Compatibility
Platform: Windows, macOS, Linux

Python: Version 3.6+

Dependencies: None (uses only standard library)

File Structure
text
todo_app/
├── todo_cli.py          # Main application file
├── todo_data.json       # Auto-generated data file (created on first run)
└── README.md           # This file
