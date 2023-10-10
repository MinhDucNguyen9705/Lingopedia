from typing import Union
from fastapi import FastAPI
from database import create_word, find_word, take_all_word, find_meaning, find_topic
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

word_list = [word for word in take_all_word()]
# meaning_list = [find_word(word) for word in take_all_word()]

@app.get("/")
def read_root():
    return {"message" : "This is an API to contain data", "author":"Lingopedia"}

@app.get("/find_word/{word}")
async def get_word(word :str):
    return [word,find_word(word)[0],find_word(word)[1]]

@app.get("/find_meaning/{meaning}")
async def get_word(meaning :str):
    lst = find_meaning(meaning)
    res = []
    for word in lst:
        res.append([word,find_word(word)[0],find_word(word)[1] ])
    return res

@app.get("/find_topic/{topic}")
async def get_from_topic(topic :str):
    lst = find_topic(topic)
    return lst

@app.get("/all_words/")
async def all_words():
    return word_list

@app.post("/find_word/")
async def post_word(new_word :dict):
    if new_word["tu"] in word_list and new_word['nghia'].lower() == find_word(new_word['tu'])[0].lower():
        return "This word has already been in our dictionary"
    else:
        word_list.append(new_word["tu"])
        create_word(new_word["tu"],new_word["nghia"],new_word["chu_de"])
        return "oke"

