import sqlite3
import pandas as pd
import json
import requests

conn = sqlite3.connect('lingopedia.db')
cursor = conn.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS tu_vung (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tu TEXT NOT NULL,
                    nghia TEXT NOT NULL
    )
""")
conn.commit()

def csv_read(file):
    df = pd.read_csv(file)
    tu_list = list(df["tu"])
    nghia_list = list(df["nghia"])
    for i in range (len(tu_list)):
        cursor.execute("INSERT INTO tu_vung (tu, nghia) VALUES (?, ?)",(tu_list[i], nghia_list[i]))
        conn.commit()
    return "Them thanh cong"

def them_tu_khoa(word):
    url = "http://127.0.0.1:8000"
    database = requests.get(f"{url}/lingopedia/{word}")
    data = json.loads(database.text)
    tu = data[0][0]
    nghia = data[0][0]
    cursor.execute("INSERT INTO tu_vung (tu, nghia) VALUES (?, ?)",(tu, nghia))
    conn.commit()
    return "Da them thanh cong"

def tra_tu_khoa(tu_khoa, tim_theo="tat_ca"):
    if tim_theo == "tu":
        cursor.execute('SELECT tu, nghia FROM tu_vung WHERE tu LIKE ?', ('%' + tu_khoa + '%',))
        conn.commit()
    # elif tim_theo == "nghia":
    #     cursor.execute('SELECT tu, nghia FROM tu_vung WHERE nghia LIKE ?', ('%' + tu_khoa + '%',))
    #     conn.commit()
    # elif tim_theo == "loai":
    #     cursor.execute('SELECT tu, nghia FROM tu_vung WHERE loai_tu LIKE ?', ('%' + tu_khoa + '%',))
    #     conn.commit()
    else:
        cursor.execute('SELECT tu, nghia FROM tu_vung WHERE tu LIKE ? OR nghia LIKE ? OR loai_tu LIKE ?',
                       ('%' + tu_khoa + '%', '%' + tu_khoa + '%', '%' + tu_khoa + '%'))
        conn.commit()

    ket_qua = cursor.fetchall()
    # conn.close()
    return ket_qua

def lay_tu():
    cursor.execute("SELECT tu FROM tu_vung")
    conn.commit()
    list_of_words = cursor.fetchall()
    lst = []
    for i in range (len(list_of_words)):
        lst.append(list_of_words[i][0])
    return lst

# print(lay_tu())