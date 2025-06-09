import json
import os
from datetime import datetime, timedelta
from copy import deepcopy
from rich.console import Console
from rich.table import Table

FILE = "reminders.json"
console = Console()
last_action = {}

def sort_tasks(tasks):
    def sort_key(t):
        try:
            due = datetime.strptime(t["due"], "%Y-%m-%d")
        except Exception:
            due = datetime.max
        priority_order = {"high": 1, "medium": 2, "low": 3}
        return (due, priority_order.get(t["priority"].lower(), 4))
    return sorted(tasks, key=sort_key)

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        tasks = json.load(f)
    return sort_tasks(tasks)

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(sort_tasks(tasks), f, indent=2)

def get_priority_color(priority):
    if priority.lower() == "high":
        return "bold red"
    elif priority.lower() == "medium":
        return "bold yellow"
    elif priority.lower() == "low":
        return "bold green"
    return ""

def show_tasks(tasks, only_pending=False):
    sorted_tasks = sort_tasks(tasks)
    table = Table(title="📋 Tasks")
    table.add_column("#", justify="right")
    table.add_column("Task", style="bold")
    table.add_column("Due", justify="center")
    table.add_column("Priority", justify="center")
    table.add_column("Tag")
    table.add_column("Status", style="cyan")

    displayed_tasks = []
    for idx, t in enumerate(sorted_tasks):
        if only_pending and t["done"]:
            continue
        status = "✓ Done" if t["done"] else "⏳ Pending"
        table.add_row(
            str(len(displayed_tasks) + 1),
            t["task"],
            t["due"],
            f"[{get_priority_color(t['priority'])}]{t['priority']}[/{get_priority_color(t['priority'])}]",
            t["tag"],
            status
        )
        displayed_tasks.append(t)

    if not displayed_tasks:
        console.print("🙌 No tasks to show!", style="green")
    else:
        console.print(table)
    return displayed_tasks

def add_task(tasks):
    task = input("Task: ").strip()
    due = input("Due date (YYYY-MM-DD): ").strip()
    priority = input("Priority (High/Medium/Low): ").strip().capitalize()
    while priority.lower() not in ("high", "medium", "low"):
        console.print("⚠️ Priority must be High, Medium, or Low.", style="red")
        priority = input("Priority (High/Medium/Low): ").strip().capitalize()
    tag = input("Tag (work/personal/etc): ").strip().lower()

    new_task = {
        "task": task,
        "due": due,
        "priority": priority,
        "tag": tag,
        "done": False
    }
    tasks.append(new_task)
    last_action.clear()
    last_action["type"] = "add"
    last_action["task"] = new_task

    console.print("✅ Task added successfully!", style="green")
    try:
        due_date = datetime.strptime(due, "%Y-%m-%d")
        delta = due_date - datetime.now()
        if delta.total_seconds() > 0:
            console.print(f"⏳ Time left: {delta.days} days and {delta.seconds//3600} hours", style="yellow")
        else:
            console.print("⚠️ Due date is in the past!", style="red")
    except Exception:
        console.print("⚠️ Invalid date format.", style="red")

def mark_done(tasks):
    displayed = show_tasks(tasks, only_pending=True)
    if not displayed:
        return
    try:
        i = int(input("Enter task number to mark as done: ")) - 1
        task = displayed[i]
        index = tasks.index(task)
        last_action.clear()
        last_action["type"] = "mark_done"
        last_action["index"] = index
        last_action["prev_state"] = deepcopy(tasks[index])
        tasks[index]["done"] = True
        console.print("✔️ Marked as done!", style="green")
    except:
        console.print("❌ Invalid task number", style="red")

def delete_task(tasks):
    displayed = show_tasks(tasks)
    if not displayed:
        return
    try:
        i = int(input("Enter task number to delete: ")) - 1
        task = displayed[i]
        index = tasks.index(task)
        last_action.clear()
        last_action["type"] = "delete"
        last_action["task"] = task
        last_action["index"] = index
        tasks.pop(index)
        console.print("🗑️ Task deleted!", style="red")
    except:
        console.print("❌ Invalid task number", style="red")

def edit_task(tasks):
    displayed = show_tasks(tasks)
    if not displayed:
        return
    try:
        i = int(input("Enter task number to edit: ")) - 1
        task = displayed[i]
        index = tasks.index(task)
        last_action.clear()
        last_action["type"] = "edit"
        last_action["index"] = index
        last_action["prev_state"] = deepcopy(tasks[index])

        new_task = input(f"Task [{task['task']}]: ").strip() or task['task']
        new_due = input(f"Due date (YYYY-MM-DD) [{task['due']}]: ").strip() or task['due']
        new_priority = input(f"Priority (High/Medium/Low) [{task['priority']}]: ").strip().capitalize() or task['priority']
        while new_priority.lower() not in ("high", "medium", "low"):
            console.print("⚠️ Priority must be High, Medium, or Low.", style="red")
            new_priority = input("Priority (High/Medium/Low): ").strip().capitalize()
        new_tag = input(f"Tag (work/personal/etc) [{task['tag']}]: ").strip().lower() or task['tag']

        tasks[index].update({
            "task": new_task,
            "due": new_due,
            "priority": new_priority,
            "tag": new_tag
        })
        console.print("✏️ Task updated!", style="green")
    except:
        console.print("❌ Invalid task number", style="red")

def search_tasks(tasks):
    keyword = input("Enter search keyword: ").strip().lower()
    if not keyword:
        console.print("⚠️ Enter a keyword", style="red")
        return
    matched = []
    for t in tasks:
        if (keyword in t["task"].lower() or
            keyword in t["due"].lower() or
            keyword in t["priority"].lower() or
            keyword in t["tag"].lower() or
            (keyword in ("done", "completed") and t["done"]) or
            (keyword == "pending" and not t["done"])):
            matched.append(t)
    if not matched:
        console.print(f"❌ No matches for '{keyword}'", style="red")
    else:
        console.print(f"🔍 Matches for '{keyword}':", style="cyan")
        show_tasks(matched)

def show_due_soon(tasks):
    today = datetime.today().date()
    soon = today + timedelta(days=3)
    found = False
    console.print("\n📅 Tasks Due Soon (next 3 days):", style="bold yellow")
    for t in tasks:
        try:
            due = datetime.strptime(t["due"], "%Y-%m-%d").date()
            if today <= due <= soon and not t["done"]:
                console.print(f"• {t['task']} (Due: {t['due']}) [{t['priority']}]", style="cyan")
                found = True
        except:
            continue
    if not found:
        console.print("🎉 No upcoming tasks!", style="green")

def undo_action(tasks):
    if not last_action:
        console.print("⚠️ Nothing to undo.", style="red")
        return
    typ = last_action["type"]
    if typ == "add":
        tasks.remove(last_action["task"])
        console.print("↩️ Undo: Task added removed.", style="cyan")
    elif typ == "delete":
        tasks.insert(last_action["index"], last_action["task"])
        console.print("↩️ Undo: Task restored.", style="cyan")
    elif typ == "edit":
        tasks[last_action["index"]] = last_action["prev_state"]
        console.print("↩️ Undo: Edit reverted.", style="cyan")
    elif typ == "mark_done":
        tasks[last_action["index"]] = last_action["prev_state"]
        console.print("↩️ Undo: Mark undone.", style="cyan")
    elif typ == "reset":
        tasks.extend(last_action["backup"])
        console.print("↩️ Undo: Reset reverted.", style="cyan")
    last_action.clear()

def reset_tasks(tasks):
    confirm = input("⚠️ This will delete ALL tasks. Are you sure? (y/n): ").strip().lower()
    if confirm == "y":
        last_action.clear()
        last_action["type"] = "reset"
        last_action["backup"] = deepcopy(tasks)
        tasks.clear()
        console.print("🧹 All tasks cleared!", style="red")
    else:
        console.print("❌ Reset cancelled.", style="green")

def daily_summary(tasks):
    console.print("\n📊 [bold blue]Daily Summary[/bold blue]")
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    pending = total - done
    console.print(f"✅ Completed: {done}, ⏳ Pending: {pending}, 📌 Total: {total}", style="cyan")
    show_due_soon(tasks)

def main():
    tasks = load_tasks()
    daily_summary(tasks)
    while True:
        console.print("\n[bold blue]📌 Menu[/bold blue]")
        console.print("1. Add Task\n2. List All Tasks\n3. Mark as Done\n4. View Upcoming\n5. Delete Task\n"
                      "6. Edit Task\n7. Search Tasks\n8. Undo Last Action\n9. Reset All Tasks\n0. Exit")
        ch = input("Choose option (0-9): ").strip()
        if ch == '1': add_task(tasks)
        elif ch == '2': show_tasks(tasks)
        elif ch == '3': mark_done(tasks)
        elif ch == '4': show_due_soon(tasks)
        elif ch == '5': delete_task(tasks)
        elif ch == '6': edit_task(tasks)
        elif ch == '7': search_tasks(tasks)
        elif ch == '8': undo_action(tasks)
        elif ch == '9': reset_tasks(tasks)
        elif ch == '0':
            save_tasks(tasks)
            console.print("📁 Tasks saved. Goodbye!", style="italic")
            break
        else:
            console.print("❌ Invalid choice", style="red")

if __name__ == "__main__":
    main()
