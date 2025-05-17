from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("vocab.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT,
        meaning TEXT,
        etymology TEXT,
        related TEXT,
        genre TEXT,
        added_at TEXT
    )""")
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect("vocab.db")
    c = conn.cursor()
    c.execute("SELECT * FROM words")
    words = c.fetchall()
    conn.close()
    return render_template("index.html", words=words)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        term = request.form["term"]
        meaning = request.form["meaning"]
        etymology = request.form["etymology"]
        related = request.form["related"]
        genre = request.form["genre"]
        now = datetime.now().strftime("%Y/%m/%d %H:%M")
        conn = sqlite3.connect("vocab.db")
        c = conn.cursor()
        c.execute("INSERT INTO words (term, meaning, etymology, related, genre, added_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (term, meaning, etymology, related, genre, now))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add_word.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
