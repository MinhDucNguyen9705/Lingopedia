string = """"""

lst = list(string.split("\n"))
words = []
meaning = []
for word in lst:
    words.append(word[:word.index(":")])
    meaning.append(word[word.index(":")+1:])
print(lst)
for i in range (0,len(words)):
    print("'{0}' : '{1}'".format(words[i],meaning[i]))
