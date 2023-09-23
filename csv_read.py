import pandas as pd
def csv_read(file):
    df = pd.read_csv(file)
    words = list(df["Words"])
    meanings = list(df["Meaning"])
    response = []
    for i in range (0,len(words)):
        response.append("'{0}' : '{1}'".format(words[i],meanings[i]))
    for i in range (0,len(response)):
        print(response[i])
    return response
print(csv_read("data.csv"))