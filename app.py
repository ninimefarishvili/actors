from flask import Flask, render_template, redirect, url_for, request, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Your account has been created!', 'success')
        conn.close()
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/actors/<int:year>')
def actors(year):
    conn = get_db_connection()
    actors_1990 = conn.execute('SELECT * FROM actors_1990 WHERE year = ?', (year,)).fetchall()
    actors_1982 = conn.execute('SELECT * FROM actors_1982 WHERE year = ?', (year,)).fetchall()
    actors_2002 = conn.execute('SELECT * FROM actors_2002 WHERE year = ?', (year,)).fetchall()
    conn.close()
    actors = actors_1990 + actors_1982 + actors_2002
    return render_template('actors.html', actors=actors, year=year)

@app.route('/add_actor', methods=['GET', 'POST'])
def add_actor():
    if 'user_id' not in session:
        flash('Please log in to add an actor.', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        year = request.form.get('year')
        movies = request.form.get('movies')
        photo_url = request.form.get('photo_url')
        conn = get_db_connection()
        conn.execute('INSERT INTO actors (name, year, movies, photo_url) VALUES (?, ?, ?, ?)',
                     (name, year, movies, photo_url))
        conn.commit()
        conn.close()
        flash('Actor added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_actor.html')


if __name__ == '__main__':
    app.run(debug=True)
