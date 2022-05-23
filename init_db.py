import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ('Noman', 'noman@gmail.com', 'password')
            )

cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ('Noman1', 'noman1@gmail.com', 'password123')
            )

connection.commit()
connection.close()
