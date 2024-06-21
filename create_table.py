import sqlite3

DATABASE = 'database.db'


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



    conn.close()




