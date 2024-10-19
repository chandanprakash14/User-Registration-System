# create_db.py
import sqlite3

conn = sqlite3.connect('registration.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Registration (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL,
    DateOfBirth TEXT NOT NULL,
    PhoneNumber TEXT,
    Address TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

print("Table created successfully.")
conn.commit()
conn.close()
