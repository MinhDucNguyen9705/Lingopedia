import requests 
res = requests.get("http://127.0.0.1:8000/find_meaning/điê")
print(res.text)