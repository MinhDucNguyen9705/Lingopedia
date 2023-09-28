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

def find_word_1(prefix):
    database = lay_tu()
    response = []
    prefix = prefix.lower()
    # Prefix = word
    for word in database:
        if prefix == word or prefix==word.lower():
            response.append(word)
    # Longest common prefix
    # string_list = []
    # current=0
    # while current<len(database):
    #     string = ""
    #     prefix_cursor = 0
    #     temp_prefix = prefix+"1"
    #     for i in range (0,len(database[word])):
    #         if database[word][i]==temp_prefix[prefix_cursor]:
    #             word_cursor = i
    #             while (database[word][word_cursor]==temp_prefix[prefix_cursor] or database[word][word_cursor]==chr(ord(temp_prefix[prefix_cursor])-32)) and word_cursor<len(database[word])-1 and prefix_cursor<len(temp_prefix)-1:
    #                 word_cursor+=1
    #                 prefix_cursor+=1
    #             string += database[word][i:word_cursor]
    #     string_list.append(string)

    # Prefix in word
    for word in database:
        if prefix[0]==word[0] and prefix in word and len(response)<5 and word not in response:
            response.append(word)
    for word in database:
        if prefix in word and len(response)<5 and word not in response:
            response.append(word)
    count_list = []
    # Number of characters in prefix in each word
    for word in database:
        word_char = list(word)
        characters = list(prefix)
        i = 0
        j = 0
        count = 0
        while i<len(word_char) and j<len(characters):
            if word_char[i] == characters[j] or word_char[i] == chr(ord(characters[j])-32):
                count+=1
                word_char.pop(i)
                characters.pop(j)
            else:
                i+=1
            if i==len(word_char) and j<len(characters):
                i=0
                j+=1
        count_list.append(count)
    min_count = min(count_list)
    max_count = max(count_list)
    # print(min_count, max_count)
    for i in range (max_count, min_count-1,-1):
        for j in range (0,len(count_list)):
            if count_list[j]==i and database[j] not in response:
                response.append(database[j])
    answer = []
    for word in response[0:5]:
        answer.append(tra_tu_khoa(word, "tu"))
    return answer

def find_word_2(prefix):
    database = lay_tu()
    response = []
    prefix = prefix.lower()
    # Prefix = word
    for word in database:
        if prefix == word or prefix==word.lower():
            response.append(word)
    # Longest common prefix
    # string_list = []
    # current=0
    # while current<len(database):
    #     string = ""
    #     prefix_cursor = 0
    #     temp_prefix = prefix+"1"
    #     for i in range (0,len(database[word])):
    #         if database[word][i]==temp_prefix[prefix_cursor]:
    #             word_cursor = i
    #             while (database[word][word_cursor]==temp_prefix[prefix_cursor] or database[word][word_cursor]==chr(ord(temp_prefix[prefix_cursor])-32)) and word_cursor<len(database[word])-1 and prefix_cursor<len(temp_prefix)-1:
    #                 word_cursor+=1
    #                 prefix_cursor+=1
    #             string += database[word][i:word_cursor]
    #     string_list.append(string)

    # Prefix in word
    for word in database:
        if prefix[0]==word[0] and prefix in word and len(response)<5 and word not in response:
            response.append(word)
    for word in database:
        if prefix in word and len(response)<5 and word not in response:
            response.append(word)
    count_list = []
    # Number of characters in prefix in each word
    for word in database:
        word_char = list(word)
        characters = list(prefix)
        i = 0
        j = 0
        count = 0
        while i<len(word_char) and j<len(characters):
            if word_char[i] == characters[j] or word_char[i] == chr(ord(characters[j])-32):
                count+=1
                word_char.pop(i)
                characters.pop(j)
            else:
                i+=1
            if i==len(word_char) and j<len(characters):
                i=0
                j+=1
        count_list.append(count)
    min_count = min(count_list)
    max_count = max(count_list)
    # print(min_count, max_count)
    for i in range (max_count, min_count-1,-1):
        for j in range (0,len(count_list)):
            if count_list[j]==i and database[j] not in response:
                response.append(database[j])
    answer = []
    for word in response[5:10]:
        answer.append(tra_tu_khoa(word, "tu"))
    return answer
    # return response

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

# prefix = input("Input a prefix ")
# print(find_word_1(prefix)[0][0][0])
# print(find_word_2(prefix))