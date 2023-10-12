import json
from xclass_sdk import request
import random
import asyncio


async def API_connect():
    url = "https://lingopedia-chi.vercel.app/"
    database = await request(f"{url}/all_words/")
    data = await database.json()
    return data


async def meaning_get_from_API(word):
    url = "https://lingopedia-chi.vercel.app/"
    database = await request(f"{url}/find_word/{word}")
    data = await database.json()
    return data

# print(meaning_get_from_API("Online Course")[1].strip(" "))


async def topic_get_from_API(word):
    url = "https://lingopedia-chi.vercel.app/"
    database = await request(f"{url}/find_topic/{word}")
    data = await database.json()
    return data

topic = ["y học", "công nghệ thông tin", "giáo dục", "lịch sử", "sinh học", "vật lý", "gia dụng", "ẩm thực", "công sở",
         "xây dựng", "nghệ thuật", "thể thao", "màu sắc", "động vật", "đại dương", "tiền sử", "phương tiện giao thông", "cơ thể"]


async def randomize(topic):
    lst = await topic_get_from_API(topic)
    random.shuffle(lst)
    words = lst[:4]
    ans = random.choice(words)
    return words, ans


def verify(word, ans):
    if word == ans:
        return True
    else:
        return False

# print(randomize("giáo dục"))
# print(verify("Academic Standards"))
# print(verify("Student Assessment"))
# print(verify("Distance Learning"))
# print(verify("Online Course"))
