import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Get the current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

class DoYourDailys:
    def __init__(self):
        self.prev_todo_list = []
        self.todo_list = self.load_todo_list()

    def load_todo_list(self):
        try:
            with open(os.path.join(current_directory, 'todo_list.json'), 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_todo_list(self):
        with open(os.path.join(current_directory, 'todo_list.json'), 'w') as file:
            json.dump(self.todo_list, file)

    def display_todo_list(self):
        return self.todo_list

    def add_task(self, task):
        self.todo_list.append(task)
        self.save_todo_list()

    def remove_task(self, task_index):
        try:
            removed_task = self.todo_list.pop(task_index - 1)
            self.save_todo_list()
        except IndexError:
            pass  # Ignore invalid task index

    def has_changes(self):
        return self.todo_list != self.prev_todo_list

    def reset_changes(self):
        self.prev_todo_list = self.todo_list.copy()

do_your_dailys = DoYourDailys()

@app.route("/")
def index():
    return render_template("index.html", todo_list=do_your_dailys.display_todo_list())

@app.route("/add_task", methods=["POST"])
def add_task():
    new_task = request.form.get("new_task")
    if new_task:
        do_your_dailys.add_task(new_task)
        do_your_dailys.reset_changes()  # Reset changes after adding a task
    return index()

@app.route("/remove_task/<task>")
def remove_task(task):
    try:
        task_index = do_your_dailys.display_todo_list().index(task)
        do_your_dailys.remove_task(task_index + 1)
    except ValueError:
        pass

    return index()

if __name__ == "__main__":
    app.run(debug=False)
