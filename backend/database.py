
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
               nghia TEXT NOT NULL,
               chu_de TEXT NOT NULL
               )
""")
connect.commit()

def create_word(word, definition, topic):
    cursor.execute(f"""
        INSERT INTO tu_dien (tu, nghia, chu_de) VALUES ('{word}','{definition}','{topic}')
    """)
    connect.commit()

def find_word(word):
    cursor.execute(f"""
        SELECT * FROM tu_dien WHERE tu = '{word}'
    """)
    result = cursor.fetchall()
    return [result[0][2], result[0][3]]


def find_meaning(meaning):
    cursor.execute(f"""
        SELECT tu FROM tu_dien WHERE nghia LIKE '%{meaning}%'
    """)
    result = cursor.fetchall()
    response = []
    for i in range (0,len(result)):
        response.append(result[i][0])
    return response

def find_topic(topic):
    cursor.execute(f"""
        SELECT tu FROM tu_dien WHERE chu_de = '{topic}'
    """)
    result = cursor.fetchall()
    response = []
    for word in result:
        response.append(word[0])
    return response

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
    chu_de_list = list(df["chu_de"])
    for i in range (len(tu_list)):
        cursor.execute("INSERT INTO tu_dien (tu, nghia, chu_de) VALUES (?, ?, ?)",(tu_list[i], nghia_list[i], chu_de_list[i]))
        connect.commit()
    return "Them thanh cong"

def csv_read_and_add_topic(file):
    df = pd.read_csv(file)
    tu_list = list(df["tu"])
    nghia_list = list(df["nghia"])
    for i in range (len(tu_list)):
        cursor.execute("INSERT INTO tu_dien (tu, nghia, chu_de) VALUES (?, ?, ?)",(tu_list[i], nghia_list[i], 'chung'))
        connect.commit()
    return "Them thanh cong"

# print(csv_read_and_add_topic("data.csv"))

def take_all_word():
    cursor.execute("SELECT tu FROM tu_dien")
    connect.commit()
    list_of_words = cursor.fetchall()
    lst = []
    for i in range (len(list_of_words)):
        lst.append(list_of_words[i][0])
    return lst

# csv_read("word_data.csv")