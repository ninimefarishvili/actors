import sqlite3
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'database.db'

def connect_db():
    return sqlite3.connect(DATABASE)
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actors_1990 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            movies TEXT NOT NULL,
            photo_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actors_1982 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            movies TEXT NOT NULL,
            photo_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actors_2002 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            movies TEXT NOT NULL,
            photo_url TEXT NOT NULL
        )
    ''')
    conn.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['logged_in'] = True
            flash('You have successfully logged in.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        flash('You have successfully registered. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/year/<int:year>')
def year(year):
    table_name = f'actors_{year}'
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    actors = cursor.fetchall()
    conn.close()
    return render_template('year.html', year=year, actors=actors)

@app.route('/add_actor/<int:year>', methods=['GET', 'POST'])
def add_actor(year):
    if 'logged_in' not in session:
        flash('You must be logged in to add an actor.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        movies = request.form['movies']
        photo_url = request.form['photo_url']
        table_name = f'actors_{year}'
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO {table_name} (name, year, movies, photo_url) VALUES (?, ?, ?, ?)', (name, year, movies, photo_url))
        conn.commit()
        conn.close()
        flash('Actor added successfully.', 'success')
        return redirect(url_for('year', year=year))
    return render_template('add_edit_actor.html', year=year, action='Add')

@app.route('/edit_actor/<int:year>/<int:actor_id>', methods=['GET', 'POST'])
def edit_actor(year, actor_id):
    if 'logged_in' not in session:
        flash('You must be logged in to edit an actor.', 'danger')
        return redirect(url_for('login'))

    table_name = f'actors_{year}'
    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        movies = request.form['movies']
        photo_url = request.form['photo_url']
        cursor.execute(f'UPDATE {table_name} SET name = ?, movies = ?, photo_url = ? WHERE id = ?', (name, movies, photo_url, actor_id))
        conn.commit()
        conn.close()
        flash('Actor updated successfully.', 'success')
        return redirect(url_for('year', year=year))
    cursor.execute(f'SELECT * FROM {table_name} WHERE id = ?', (actor_id,))
    actor = cursor.fetchone()
    conn.close()
    return render_template('add_edit_actor.html', year=year, actor=actor, action='Edit')

@app.route('/delete_actor/<int:year>/<int:actor_id>')
def delete_actor(year, actor_id):
    if 'logged_in' not in session:
        flash('You must be logged in to delete an actor.', 'danger')
        return redirect(url_for('login'))

    table_name = f'actors_{year}'
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table_name} WHERE id = ?', (actor_id,))
    conn.commit()
    conn.close()
    flash('Actor deleted successfully.', 'success')
    return redirect(url_for('year', year=year))

if __name__ == '__main__':
    app.run(debug=True)
