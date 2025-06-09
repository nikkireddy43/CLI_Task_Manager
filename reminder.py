import json
import os
import time
from datetime import datetime, timedelta
from plyer import notification

FILE = "reminders.json"

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def notify_upcoming_tasks():
    tasks = load_tasks()
    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)

    for task in tasks:
        try:
            due = datetime.strptime(task["due"], "%Y-%m-%d")
            if now <= due <= one_hour_later and not task["done"]:
                notification.notify(
                    title=f"⏰ Upcoming Task: {task['task']}",
                    message=f"Due on {task['due']} | Priority: {task['priority']} | Tag: {task['tag']}",
                    timeout=10
                )
        except Exception as e:
            continue  # Skip tasks with invalid dates

if __name__ == "__main__":
    while True:
        notify_upcoming_tasks()
        time.sleep(600)  # Check every 10 minutes
