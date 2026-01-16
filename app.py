import os
import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "todo.db")

HTML = """
<!doctype html>
<title>ToDo (Azure PaaS)</title>
<h1>ToDo-Liste (dynamisch)</h1>

<form method="POST" action="/add">
  <input name="task" placeholder="Neue Aufgabe" required>
  <button type="submit">Hinzufügen</button>
</form>

<ul>
  {% for id, task in items %}
    <li>
      {{ task }}
      <form method="POST" action="/delete/{{ id }}" style="display:inline">
        <button type="submit">Löschen</button>
      </form>
    </li>
  {% endfor %}
</ul>
"""

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        """)
        con.commit()

@app.route("/")
def index():
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        items = con.execute("SELECT id, task FROM todos ORDER BY id DESC").fetchall()
    return render_template_string(HTML, items=items)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        with sqlite3.connect(DB_PATH) as con:
            con.execute("INSERT INTO todos(task) VALUES (?)", (task,))
            con.commit()
    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("DELETE FROM todos WHERE id = ?", (id,))
        con.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
