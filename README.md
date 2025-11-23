# Vityarthi-Project-To-Do-list-
Modern Todo List App (Tkinter)
A modern, clean, and interactive Desktop Todo List Application built using Python (Tkinter).
It allows users to create, update, delete, complete, search, and sort tasks, with persistent storage using JSON.
Features
Task Management
Add new tasks
Edit existing tasks
Delete tasks
Mark tasks as Completed / Pending
Search & Sort
Search tasks by text
Sort by:
Newest
Oldest
A → Z
Z → A
Completed First
Pending First
Statistics Panel
Total tasks
Completed tasks
Pending tasks
Completion percentage
Data Persistence
All tasks are automatically stored in todo_data.json
Restores tasks when app reopens
Modern UI
Dark theme layout
Custom styling (ttk + tkinter)
Automatic date/time tracking
Tech Stack
Component	Technology
Language	Python 3
GUI Framework	Tkinter
Storage	JSON file
OS Support	Windows / Linux / Mac
Project Structure
todoapp/
│── app.py               # Main application
│── todo_data.json       # Auto-generated task storage file
│── README.md            # Project documentation
 How To Run

1. Install Python 3
Check:
python --version
2. Install Tkinter (if missing)

Windows → already included
Linux example:

sudo apt-get install python3-tk
3. Run the application
python app.py
📸 Screenshot

(optional – if you want later)
🧾 Data Format Example

[
  {
    "task": "Complete assignment",
    "status": "Pending",
    "date": "2025-01-20 07:10 AM"
  }
]


---

✨ Future Improvements

Add category / priority
Export to Excel/PDF
Notifications / reminders
Themes system
Cloud sync

---

Author
Harsh Gabrani
