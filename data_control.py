# Anh Hải làm chỗ này

# import database


import json
from xclass_sdk import request
# import requests
import asyncio

async def API_connect():
    url = "http://127.0.0.1:8000"
    database = await request(f"{url}/all_words/")
    data = await database.json()
    return data

async def meaning_get_from_API(word):
    url = "http://127.0.0.1:8000"
    database = await request(f"{url}/find_word/{word}")
    data = await database.json()
    return data

async def word_get_from_API(meaning):
    url = "http://127.0.0.1:8000"
    database = await request(f"{url}/find_meaning/{meaning}")
    data = await database.json()
    return data

# def API_connect():
#     url = "http://127.0.0.1:8000"
#     database = requests.get(f"{url}/all_words/")
#     data = json.loads(database.text)
#     return data

# print(API_connect())

# def meaning_get_from_API(word):
#     url = "http://127.0.0.1:8000"
#     database = requests.get(f"{url}/find_word/{word}")
#     data = json.loads(database.text)
#     return data

async def post_word_to_API(word, meaning, topic):
    url = "http://127.0.0.1:8000"
    response = await request(f"{url}/find_word/", method = "POST", json = {"word" : {word}, "meaning" : {meaning}, "topic" : {topic}})
    return await meaning_get_from_API(word)

# print(await post_word_to_API("numerator", "tử số"))
# print(API_connect())
# print(meaning_get_from_API("Consultant"))

async def find_word(prefix):
    database = await API_connect()
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
        if (prefix[0]==word[0] or prefix[0]==word[0].lower()) and (prefix in word or prefix in word.lower())  and len(response)<5 and word not in response:
            response.append(word)
    for word in database:
        if (prefix in word or prefix in word.lower()) and len(response)<5 and word not in response:
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
    for i in range (max_count, min_count-1,-1):
        for j in range (0,len(count_list)):
            if count_list[j]==i and database[j] not in response:
                response.append(database[j])
    return response

answer = []

async def answer_1(prefix):
    global answer
    response = await find_word(prefix)
    answer = []
    for word in response:
        if await meaning_get_from_API(word)!= {'detail': 'Not Found'} and await meaning_get_from_API(word)!=None:
            answer.append(await meaning_get_from_API(word))
        else:
            continue
        if len(answer)>=5:
            break
    return answer


async def answer_2(prefix):
    global answer
    response = await find_word(prefix)
    ans = []
    for word in response:
        if await meaning_get_from_API(word)!= {'detail': 'Not Found'} and len(ans)<5 and await meaning_get_from_API(word) not in answer and await meaning_get_from_API(word)!=None:
            ans.append(await meaning_get_from_API(word))
        else:
            continue
        if len(ans)>=5:
            break
    answer = []
    return ans

def history_write(history, word):
    history.append(word)

def show_history(history):
    return history