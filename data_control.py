import json
from xclass_sdk import request
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

async def post_word_to_API(word, meaning, topic):
    url = "http://127.0.0.1:8000"
    response = await request(f"{url}/find_word/", method = "POST", json = {"tu" : {word}, "nghia" : {meaning}, "chu_de" : {topic}})
    return "Đề xuất thành công. Hãy chờ từ ngữ được kiểm duyệt trước khi được đưa vào từ điển bạn nhé!"

async def find_word(prefix):
    database = await API_connect()
    response = []
    prefix = prefix.lower()
    # Prefix = word
    for word in database:
        if prefix == word or prefix==word.lower():
            response.append(word)
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