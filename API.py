from typing import Union
from fastapi import FastAPI
from database import lay_tu, them_tu_khoa, tra_tu_khoa

app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "This is an API to contain data", "author":"Lingopedia"}

word_list = [word for word in lay_tu()]
meaning_list = [tra_tu_khoa(word,"tu") for word in lay_tu()]

@app.get("/lingopedia/{prefix}")
def word_query(prefix : Union[str, None]=None):
    for word in meaning_list:
        if word[0][0] == prefix:
            return word

@app.post("/lingopedia/")
def add_word(word : str, meaning : str):
    meaning_list.append([[word, meaning]])

@app.get("/all_words/")
def all_words():
    return word_list

@app.get("/all_meaning/")
def all_meaning():
    return meaning_list