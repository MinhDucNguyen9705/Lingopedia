import requests
url = "http://127.0.0.1:8000"
word = input()
meaning = input()
topic = input()
info = {'tu': "", 'nghia': "", "chu_de" : ""}
info['tu'] = word
info['nghia']= meaning
info['chu_de'] = topic
print(info)
res = requests.post(f"{url}/find_word/", json = info)
traloi = requests.get(f'{url}/find_word/{word}')
print(traloi.text)