import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = 'tasks.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    # Default structure
    data = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
    data['notes'] = ''
    return data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class TaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Task Manager')
        self.geometry('400x400')
        self.resizable(False, False)

        self.data = load_data()
        self.task_vars = {day: [] for day in self.data if day != 'notes'}

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=day)
            self.build_day_tab(frame, day)

        self.build_notes_tab()

    def build_day_tab(self, frame, day):
        tasks = self.data.get(day, [])
        container = ttk.Frame(frame)
        container.pack(fill='both', expand=True, padx=10, pady=10)

        for task in tasks:
            var = tk.BooleanVar(value=task.get('done', False))
            chk = ttk.Checkbutton(container, text=task['text'], variable=var, command=self.save)
            chk.pack(anchor='w')
            self.task_vars[day].append((var, task))

        entry_var = tk.StringVar()
        entry = ttk.Entry(container, textvariable=entry_var)
        entry.pack(fill='x', pady=(10,0))

        def add_task():
            text = entry_var.get().strip()
            if text:
                task = {'text': text, 'done': False}
                var = tk.BooleanVar(value=False)
                chk = ttk.Checkbutton(container, text=text, variable=var, command=self.save)
                chk.pack(anchor='w')
                self.task_vars[day].append((var, task))
                self.save()
                entry_var.set('')
        add_btn = ttk.Button(container, text='Add Task', command=add_task)
        add_btn.pack(pady=5)

    def build_notes_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Notes')

        text = tk.Text(frame, wrap='word')
        text.pack(fill='both', expand=True)
        text.insert('1.0', self.data.get('notes', ''))

        def save_notes():
            self.data['notes'] = text.get('1.0', 'end').rstrip()
            save_data(self.data)
            messagebox.showinfo('Saved', 'Notes saved.')

        btn = ttk.Button(frame, text='Save Notes', command=save_notes)
        btn.pack(pady=5)

    def save(self):
        for day, vars_tasks in self.task_vars.items():
            self.data[day] = []
            for var, task in vars_tasks:
                task['done'] = var.get()
                self.data[day].append(task)
        save_data(self.data)

if __name__ == '__main__':
    app = TaskApp()
    app.mainloop()
