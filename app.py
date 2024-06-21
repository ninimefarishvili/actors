from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'database.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create tables if they don't exist
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

    # Insert data into actors_1990 table
    cursor.execute('''
        INSERT INTO actors_1990 (name, year, movies, photo_url) VALUES
        ('Emma Watson', 1990, 'Harry Potter, Beauty and the Beast', 'https://hips.hearstapps.com/hmg-prod/images/Emma-Watson_GettyImages-619546914.jpg?crop=1xw:1.0xh;center,top&resize=640:*'),
        ('The Weeknd', 1990, 'Starboy, Blinding Lights', 'https://variety.com/wp-content/uploads/2023/03/GettyImages-1319690083.jpg?w=1000'),
        ('Jennifer Lawrence', 1990, 'The Hunger Games, Silver Linings Playbook', 'https://goldenglobes.com/wp-content/uploads/2023/10/Jennifer-Lawrence-Photo.png'),
        ('Kristen Stewart', 1990, 'Twilight, Snow White and the Huntsman', 'https://pics.filmaffinity.com/175654881279808-nm_200.jpg'),
        ('Grant Gustin', 1990, 'The Flash, Glee', 'https://images.mubicdn.net/images/cast_member/483195/cache-201821-1487480877/image-w856.jpg')
    ''')
    conn.commit()

    # Insert data into actors_1982 table
    cursor.execute('''
        INSERT INTO actors_1982 (name, year, movies, photo_url) VALUES
        ('Anne Hathaway', 1982, 'The Witches, Interstellar', 'https://media.vogue.fr/photos/62b591fa8a4275dbe4097b25/2:3/w_2560%2Cc_limit/1240769828'),
        ('Sebastian Stan', 1982, 'Avengers: Endgame, Captain America: The First Avenger, A Different Man', 'https://static.wikia.nocookie.net/disney/images/7/74/Sebastian_Stan.jpg/revision/latest?cb=20230815150406'),
        ('Paul Wesley', 1982, 'The Vampire Diaries, Star Trek: Strange New Worlds', 'https://static.wikia.nocookie.net/roswell/images/d/da/Paul_Wesley.jpg/revision/latest?cb=20181212091508'),
        ('Eddie Redmayne', 1982, 'Les Misérables, The Theory of Everything', 'https://media.themoviedb.org/t/p/w500/Ll3cAE9RIsSX4cvTi5K1KNQizI.jpg'),
        ('Kirsten Dunst', 1982, 'Spider-Man, Jumanji', 'https://www.onthisday.com/images/people/kirsten-dunst.jpg?w=360')
    ''')
    conn.commit()

    # Insert data into actors_2002 table
    cursor.execute('''
        INSERT INTO actors_2002 (name, year, movies, photo_url) VALUES
        ('Caleb Logan LeBlanc', 2002, 'Annie LeBlanc: Photograph, YouTube Revolution', 'https://i.pinimg.com/1200x/7f/14/7f/7f147f3aafd425fd1bfe46c0aaed2472.jpg'),
        ('Skai Jackson', 2002, 'The Smurfs, My Dad\'s a Soccer Mom', 'https://www.j-14.com/wp-content/uploads/2017/07/skai-jackson-age-3.jpg?fit=800%2C1009&quality=86&strip=all'),
        ('Jenna Ortega', 2002, 'SCREAM, Elena of Avalor', 'https://www.onthisday.com/images/people/jenna-ortega.jpg?w=720'),
        ('Sophia Lillis', 2002, 'IT, It Chapter Two', 'https://deadline.com/wp-content/uploads/2019/10/sophia-lillis-credit-miles-schuster-e1572025016330.jpg'),
        ('Asher Angel', 2002, 'Shazam!, On Pointe', 'https://media.themoviedb.org/t/p/w500/9v1mS2Rrocl2hOtNe9Gte3SS4Ch.jpg')
    ''')
    conn.commit()

    # Close the database connection
    conn.close()

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
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            conn.close()
            flash('Username already exists. Please choose another one.', 'danger')
            return redirect(url_for('register'))
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
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
        cursor.execute(f'INSERT INTO {table_name} (name, year, movies, photo_url) VALUES (?, ?, ?, ?)',
                       (name, year, movies, photo_url))
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
        cursor.execute(f'UPDATE {table_name} SET name = ?, movies = ?, photo_url = ? WHERE id = ?',
                       (name, movies, photo_url, actor_id))
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
