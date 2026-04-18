import sqlite3

def init_db():
    # Connect to SQLite database (this creates a file named grabpic.db in your folder)
    conn = sqlite3.connect('grabpic.db')
    cursor = conn.cursor()

    # 1. Create Images Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE NOT NULL
        )
    ''')

    # 2. Create Faces Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Faces (
            grab_id INTEGER PRIMARY KEY AUTOINCREMENT,
            face_encoding BLOB NOT NULL
        )
    ''')

    # 3. Create Image_Faces Mapping Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Image_Faces (
            image_id INTEGER,
            grab_id INTEGER,
            FOREIGN KEY(image_id) REFERENCES Images(image_id),
            FOREIGN KEY(grab_id) REFERENCES Faces(grab_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Success! Database and tables created perfectly.")

if __name__ == '__main__':
    init_db()