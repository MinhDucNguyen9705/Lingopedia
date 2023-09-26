from typing import Union
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "This is an API to contain data", "author":"Lingopedia"}

word_list = [
]

@app.get("/lingopedia/{prefix}")
def word_query(prefix : Union[str, None]=None):
    for word in word_list:
        if word["tu"] == prefix:
            return word

@app.post("/lingopedia/")
def add_word(word : dict):
    word_list.append(word)

@app.get("/all_words/")
def all_words():
    return word_list