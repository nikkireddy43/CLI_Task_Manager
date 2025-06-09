# ✅ Task Manager CLI with Reminders

A beautiful and powerful command-line **Task Manager** built in Python using the [Rich](https://github.com/Textualize/rich) library. Easily manage your tasks with priorities, deadlines, tags, undo, and more. Includes a **separate reminder module** for viewing tasks due today and tomorrow.

---

## 📁 Features

### 🌟 Core Features
- Add tasks with:
  - Name
  - Due date
  - Priority (High/Medium/Low)
  - Tag (work/personal/etc)
- List all tasks in a  table
- Mark tasks as done
- Edit tasks interactively
- Delete tasks
- Undo last action (add/edit/delete/mark-done/reset)
- View tasks due soon (next 3 days)
- Full-text search (by task name, tag, priority, status, etc.)
- Daily summary on launch
- Reset all tasks with confirmation

### 🔔 Reminder Script (Separate)
- Standalone script to show tasks due **today** and **tomorrow**
- Useful for daily task checks or cron jobs
- Can be extended for notifications

---

## 🧰 Technologies Used

- 🐍 Python 3.7+
- 🎨 [Rich](https://github.com/Textualize/rich) for terminal UI
- 📄 JSON for local task storage (`reminders.json`)

---

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nikkireddy43/CLI_Task_Manager.git
cd CLI_Task_Manager
````

### 2. Install Required Package

```bash
pip install rich
```

---

## 🚀 Usage

### Run the Task Manager (Main Script)

```bash
python task_manager.py
```

> ✅ On **Windows CMD**, run this to support UTF-8 icons:

```bash
set PYTHONUTF8=1 && python task_manager.py
```

### Run the Reminder Script
  Optional an additional feature given along with the main code.
  
  **Install Required Package

```bash
pip install plyer
```
  
  **To run code
```bash
python reminder.py
```

> 💡 Shows tasks due **today** or **tomorrow** in a quick summary view.

---

## 📂 File Structure

```
📁 your-repo-name/
├── task_manager.py     # Main CLI app
├── reminder.py         # Independent reminder script
├── reminders.json      # Auto-generated task data file
└── README.md           # You're here!
```

---

## 📌 Task Data Format (reminders.json)

Each task is stored as a JSON object:

```json
{
  "task": "Finish report",
  "due": "2025-06-15",
  "priority": "High",
  "tag": "work",
  "done": false
}
```

---

## 🔧 How to Extend

* Add recurring tasks
* Add desktop or email notifications to `reminder.py`
* Sync tasks to cloud storage or a database
* Build a GUI frontend using `tkinter` or `PyQt`

---

## ✍️ Author

**P.Sai Nikhitha Reddy**
GitHub: [https://github.com/nikkireddy43](https://github.com/nikkireddy43)

---

## 🏁 License

This project is licensed under the MIT License.
Feel free to use, modify, and share with attribution.

---


