# Anh Hải làm chỗ này

# import database


import json
# from xclass_sdk import request
import requests
import asyncio

import sqlite3
import pandas as pd

def API_connect():
    url = "http://127.0.0.1:8000"
    database = requests.get(f"{url}/all_words/")
    data = json.loads(database.text)
    return data

def meaning_get_from_API(word):
    url = "http://127.0.0.1:8000"
    database = requests.get(f"{url}/lingopedia/{word}")
    data = json.loads(database.text)
    return data

def post_word_to_API(word, meaning):
    url = "http://127.0.0.1:8000"
    response = requests.post(f"{url}/lingopedia/", json = [[word,meaning]])
    return "Them thanh cong"
# print(API_connect())
# print(meaning_get_from_API("Consultant"))

def find_word(prefix):
    database = API_connect()
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
    return response

answer = []

def answer_1(prefix):
    global answer
    response = find_word(prefix)
    answer = []
    for word in response:
        if meaning_get_from_API(word)!= {'detail': 'Not Found'} and meaning_get_from_API(word)!=None:
            answer.append(meaning_get_from_API(word))
        else:
            continue
        if len(answer)>=5:
            break
    return answer


def answer_2(prefix):
    global answer
    response = find_word(prefix)
    ans = []
    for word in response:
        if meaning_get_from_API(word)!= {'detail': 'Not Found'} and len(ans)<5 and meaning_get_from_API(word) not in answer and meaning_get_from_API(word)!=None:
            ans.append(meaning_get_from_API(word))
        else:
            continue
        if len(ans)>=5:
            break
    answer = []
    return ans

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

prefix = input("Input a prefix ")
print(answer_1(prefix))
print(answer_2(prefix))