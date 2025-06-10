from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bus.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source TEXT,
        destination TEXT,
        time TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('bus.db')
    c = conn.cursor()
    c.execute("SELECT * FROM schedule")
    buses = c.fetchall()
    conn.close()
    return render_template('index.html', buses=buses)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        source = request.form['source']
        destination = request.form['destination']
        time = request.form['time']
        conn = sqlite3.connect('bus.db')
        c = conn.cursor()
        c.execute("INSERT INTO schedule (name, source, destination, time) VALUES (?, ?, ?, ?)",
                  (name, source, destination, time))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('bus.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        source = request.form['source']
        destination = request.form['destination']
        time = request.form['time']
        c.execute("UPDATE schedule SET name=?, source=?, destination=?, time=? WHERE id=?",
                  (name, source, destination, time, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        c.execute("SELECT * FROM schedule WHERE id=?", (id,))
        bus = c.fetchone()
        conn.close()
        return render_template('edit.html', bus=bus)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('bus.db')
    c = conn.cursor()
    c.execute("DELETE FROM schedule WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
