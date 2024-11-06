import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
    )
''')
conn.commit()

# Function to refresh the task list
def refresh_tasks():
    for widget in task_frame.winfo_children():
        widget.destroy()

    cursor.execute('SELECT * FROM tasks')
    for task in cursor.fetchall():
        task_id = task[0]
        title = task[1]
        description = task[2]
        completed = task[3]

        frame = tk.Frame(task_frame)
        frame.pack(fill='x')

        check_var = tk.BooleanVar(value=completed)
        check_button = tk.Checkbutton(frame, variable=check_var, command=lambda task_id=task_id, var=check_var: toggle_task(task_id, var))
        check_button.pack(side='left')

        title_entry = tk.Entry(frame, width=30)  # Increase width of title_entry
        title_entry.insert(0, title)
        title_entry.pack(side='left', fill='x', expand=True)

        description_entry = tk.Entry(frame, width=50)  # Increase width of description_entry
        description_entry.insert(0, description)
        description_entry.pack(side='left', fill='x', expand=True)

        update_button = tk.Button(frame, text='Update', command=lambda task_id=task_id, title_entry=title_entry, description_entry=description_entry, var=check_var: update_task(task_id, title_entry, description_entry, var))
        update_button.pack(side='left')

        delete_button = tk.Button(frame, text='Delete', command=lambda task_id=task_id: delete_task(task_id))
        delete_button.pack(side='left')

# Function to add a new task
def add_task():
    title = title_entry.get()
    description = description_entry.get()

    if title == "":
        messagebox.showwarning("Input Error", "Task title cannot be empty")
        return

    cursor.execute('INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)', (title, description, False))
    conn.commit()
    refresh_tasks()
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# Function to toggle the task completion status
def toggle_task(task_id, var):
    cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (var.get(), task_id))
    conn.commit()
    refresh_tasks()

# Function to update a task
def update_task(task_id, title_entry, description_entry, var):
    title = title_entry.get()
    description = description_entry.get()
    completed = var.get()

    if title == "":
        messagebox.showwarning("Input Error", "Task title cannot be empty")
        return

    cursor.execute('UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?', (title, description, completed, task_id))
    conn.commit()
    refresh_tasks()

# Function to delete a task
def delete_task(task_id):
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    refresh_tasks()

# Tkinter setup
root = tk.Tk()
root.title("Task Manager")

frame = tk.Frame(root)
frame.pack(pady=10)

title_label = tk.Label(frame, text="Title:")
title_label.grid(row=0, column=0, padx=5)

title_entry = tk.Entry(frame, width=30)  # Increase width of title_entry
title_entry.grid(row=0, column=1, padx=5)

description_label = tk.Label(frame, text="Description:")
description_label.grid(row=0, column=2, padx=5)

description_entry = tk.Entry(frame, width=50)  # Increase width of description_entry
description_entry.grid(row=0, column=3, padx=5)

add_button = tk.Button(frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=4, padx=5)

task_frame = tk.Frame(root)
task_frame.pack(pady=10)

refresh_tasks()

root.mainloop()

# Close the database connection when the application is closed
conn.close()


