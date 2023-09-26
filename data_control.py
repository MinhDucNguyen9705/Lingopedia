# Anh Hải làm chỗ này

# import database

import sqlite3
import requests
import json
import pandas as pd
conn = sqlite3.connect('lingopedia.db')
cursor = conn.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS tu_vung (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tu TEXT NOT NULL,
                    nghia TEXT NOT NULL,
                    loai_tu TEXT NOT NULL
        )
""")
conn.commit()

def csv_read(file):
    df = pd.read_csv(file)
    tu_list = list(df["tu"])
    nghia_list = list(df["nghia"])
    loai_list = list(df["loai tu"])
    for i in range (len(tu_list)):
        cursor.execute("INSERT INTO tu_vung (tu, nghia, loai_tu) VALUES (?, ?, ?)",(tu_list[i], nghia_list[i], loai_list[i]))
        conn.commit()
    return "Them thanh cong"

def them_tu_khoa(tu, nghia, loai):
    cursor.execute("INSERT INTO tu_vung (tu, nghia, loai_tu) VALUES (?, ?, ?)",(tu, nghia, loai))
    conn.commit()
    return "Da them thanh cong"

def tra_tu_khoa(tu_khoa, tim_theo="tat_ca"):
    if tim_theo == "tu":
        cursor.execute('SELECT tu, nghia FROM tu_vung WHERE tu LIKE ?', ('%' + tu_khoa + '%',))
        conn.commit()
    elif tim_theo == "nghia":
        cursor.execute('SELECT tu, nghia FROM tu_vung WHERE nghia LIKE ?', ('%' + tu_khoa + '%',))
        conn.commit()
    elif tim_theo == "loai":
        cursor.execute('SELECT tu, nghia FROM tu_vung WHERE loai_tu LIKE ?', ('%' + tu_khoa + '%',))
        conn.commit()
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

# print(csv_read("data.csv"))
# print(lay_tu())

# url = "http://127.0.0.1:8000"
# tu = input("Tu ban can them ")
# nghia = input("Nghia cua tu do ")
# loai = input("Loai tu cua tu da them ")
# add = requests.post(f"{url}/lingopedia/",json = {"tu": tu, "nghia":nghia, "loai_tu":loai})
# res = requests.get(f"{url}/lingopedia/{tu}")
# data = json.loads(res.text)

# them_tu_khoa(data["tu"],data["nghia"],data["loai_tu"])

# Sử dụng hàm này để tra từ theo nhiều kiểu


# tu_khoa = input("Nhập từ khóa cần tra: ")
# tuy_chon_tra = input("Chọn kiểu tra (tu/nghia/loai/tat_ca): ")
# ket_qua_tra = tra_tu_khoa(tu_khoa, tuy_chon_tra)

# cursor.execute("SELECT * FROM tu_vung")
# conn.commit()
# read_all = cursor.fetchall()
# for tu in read_all:
#     print(tu)

# if ket_qua_tra:
#     for tu, nghia in ket_qua_tra:
#         print(f'Từ: {tu}, Nghĩa: {nghia}')
# else:
#     print("Không tìm thấy từ nào phù hợp.")

# print(tra_tu_khoa("A general practitioner (GP)","tu"))