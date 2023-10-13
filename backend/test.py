import requests
url = "https://lingopedia-chi.vercel.app"
word = input()
meaning = input()
topic = input()
info = {'tu': "", 'nghia': "", "chu_de" : ""}
info['tu'] = word
info['nghia']= meaning
info['chu_de'] = topic
print(info)
res = requests.post(f"{url}/find_word/", json = info)
print("1")
traloi = requests.get(f'{url}/find_word/{word}')
print(traloi.text)