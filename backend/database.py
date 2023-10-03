
import sqlite3
import json
import pandas as pd

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

# def find_word(word):
#     cursor.execute(f"SELECT * FROM tu_dien WHERE tu == {word}")
#     result = cursor.fetchall()
#     # print(result)
#     return result

def find_word(word):
    cursor.execute(f"""
        SELECT * FROM tu_dien WHERE tu LIKE '%{word}%'
    """)
    result = cursor.fetchall()
    # print(result)
    return result[0][2]

# import sqlite3
# import json

# connect = sqlite3.connect('lingopedia.db')
# cursor = connect.cursor()
# cursor.execute("""
#         CREATE TABLE IF NOT EXISTS tu_dien (
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                tu TEXT NOT NULL,
#                nghia TEXT NOT NULL
#                )
# """)
# connect.commit()

# def create_word(word,definition):
#     cursor.execute(f"""
#         INSERT INTO tu_dien (tu, nghia) VALUES ('{word}','{definition}')
# """)
#     connect.commit()

# def find_word(word):
#     cursor.execute(f"""
#         SELECT * FROM tu_dien WHERE tu LIKE '%{word}%'
# """)
#     result = cursor.fetchall()
#     # print(result)
#     return result

def csv_read(file):
    df = pd.read_csv(file)
    tu_list = list(df["tu"])
    nghia_list = list(df["nghia"])
    for i in range (len(tu_list)):
        cursor.execute("INSERT INTO tu_dien (tu, nghia) VALUES (?, ?)",(tu_list[i], nghia_list[i]))
        connect.commit()
    return "Them thanh cong"

def take_all_word():
    cursor.execute("SELECT tu FROM tu_dien")
    connect.commit()
    list_of_words = cursor.fetchall()
    lst = []
    for i in range (len(list_of_words)):
        lst.append(list_of_words[i][0])
    return lst

# print(csv_read("data.csv"))
# print(find_word("allergen"))
# print(take_all_word())