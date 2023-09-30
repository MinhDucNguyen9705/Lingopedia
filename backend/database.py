
import sqlite3
import json

# check_same_thread set to off
connect = sqlite3.connect('lingopedia.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS tu_dien (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               tu TEXT NOT NULL,
               nghia TEXT NOT NULL
               )
""")
connect.commit()

def create_word(word,definition):
    cursor.execute(f"""
        INSERT INTO tu_dien (tu, nghia) VALUES ('{word}','{definition}')
    """)
    connect.commit()

def find_word(word):
    cursor.execute(f"""
        SELECT * FROM tu_dien WHERE tu LIKE '%{word}%'
    """)
    result = cursor.fetchall()
    print(result)
    return result

import sqlite3
import json

connect = sqlite3.connect('lingopedia.db')
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS tu_dien (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               tu TEXT NOT NULL,
               nghia TEXT NOT NULL
               )
""")
connect.commit()

def create_word(word,definition):
    cursor.execute(f"""
        INSERT INTO tu_dien (tu, nghia) VALUES ('{word}','{definition}')
""")
    connect.commit()

def find_word(word):
    cursor.execute(f"""
        SELECT * FROM tu_dien WHERE tu LIKE '%{word}%'
""")
    result = cursor.fetchall()
    print(result)
    return result