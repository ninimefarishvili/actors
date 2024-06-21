import sqlite3

DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
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
                    CREATE TABLE  actors_1990 (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        year INTEGER NOT NULL,
                        movies TEXT NOT NULL,
                        photo_url TEXT NOT NULL
                    )
                ''')

    conn.commit()

    cursor.execute('''
                        CREATE TABLE  actors_1982 (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            year INTEGER NOT NULL,
                            movies TEXT NOT NULL,
                            photo_url TEXT NOT NULL
                        )
                    ''')
    conn.commit()

    cursor.execute('''
                            CREATE TABLE  actors_2002 (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                year INTEGER NOT NULL,
                                movies TEXT NOT NULL,
                                photo_url TEXT NOT NULL
                            )
                        ''')
    conn.commit()

    cursor.execute('''
                        INSERT INTO actors_1990 (name, year, movies, photo_url) VALUES
                        ('Emma Watson', 1990, 'Harry Potter, Beauty and the Beast', 'https://hips.hearstapps.com/hmg-prod/images/Emma-Watson_GettyImages-619546914.jpg?crop=1xw:1.0xh;center,top&resize=640:*'),
                        ('The Weeknd', 1990, 'Starboy, Blinding Lights', 'https://variety.com/wp-content/uploads/2023/03/GettyImages-1319690083.jpg?w=1000'),
                        ('Jennifer Lawrence', 1990, 'The Hunger Games, Silver Linings Playbook', 'https://goldenglobes.com/wp-content/uploads/2023/10/Jennifer-Lawrence-Photo.png'),
                        ('Kristen Stewart', 1990, 'Twilight, Snow White and the Huntsman', 'https://pics.filmaffinity.com/175654881279808-nm_200.jpg'),
                        ('Grant Gustin', 1990, 'The Flash, Glee', 'https://images.mubicdn.net/images/cast_member/483195/cache-201821-1487480877/image-w856.jpg')
                    ''')



if __name__ == '__main__':
    init_db()