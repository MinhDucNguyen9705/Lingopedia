from typing import Union
from fastapi import FastAPI
from database import create_word, find_word

app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "This is an API to contain data", "author":"Lingopedia"}

@app.get("/find_word/{word}")
async def get_word(word :str):
    return find_word(word)

@app.post("/create_word")
async def post_word(new_word :dict):
    try:
        create_word(new_word["word"],new_word["definition"])
        return "oke"
    except:
        return "not oke"