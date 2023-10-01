from typing import Union
from fastapi import FastAPI
from database import create_word, find_word, take_all_word

app = FastAPI()

word_list = [word for word in take_all_word()]
# meaning_list = [find_word(word) for word in take_all_word()]

@app.get("/")
def read_root():
    return {"message" : "This is an API to contain data", "author":"Lingopedia"}

@app.get("/find_word/{word}")
async def get_word(word :str):
    return [word,find_word(word)]

@app.get("/all_words/")
async def all_words():
    return word_list

@app.post("/create_word")
async def post_word(new_word :dict):
    try:
        create_word(new_word["word"],new_word["definition"])
        return "oke"
    except:
        return "not oke"