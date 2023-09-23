import random
lst = []
sequence = ["hello","event","open","ban"]
for i in range (0,15):
    lst.append(["."]*15)
sequence = sorted(sequence,key=len,reverse=True)
start = random.randint(0,len(lst[0])//2)
i=2
j=0
while i < len(lst) and j<len(sequence[0]):
    lst[i][8] = sequence[0][j]
    i+=1
    j+=1
# print(sequence)
# print(start)
stop = False
for c in sequence[0]:
    for word in sequence[1:]:
        if c in word:
            current_char = c
            index = word.index(c)
            sequence[0]=word
            sequence.pop(sequence.index(word))
            stop = True
            break
    if stop ==True:
        break
# print(sequence)
# print(current_char)
# print(index)
for row in range (0,len(lst)):
    for col in range (0,len(lst[0])):
        if lst[row][col]==current_char:
            current_row = row
            current_col = col
# print(sequence)
# print(current_row,current_col)
i=current_col-index
j=0
if all(lst[current_row][k] == "." for k in range (i+1, i+len(sequence[0])-1)):
    while i<len(lst[0]) and j<len(sequence[0]):
        lst[current_row][i] = sequence[0][j]
        i+=1
        j+=1
stop = False
for c in sequence[0]:
    for word in sequence[1:]:
        if c in word:
            current_char = c
            index = word.index(c)
            sequence[0]=word
            sequence.pop(sequence.index(word))
            stop = True
            if index>0:
                check_char = sequence[0][index-1]
            if index<len(word)-1:
                check_char = sequence[0][index+1]
            break
    if stop == True:
        break
print(check_char, current_char)
for row in range (0,len(lst)):
    for col in range (0,len(lst[0])):
        if lst[row][col]==current_char and (lst[row][col-1]==check_char or lst[row][col+1]==check_char):
            current_row = row
            current_col = col
print(current_col)
print(current_row)
i=current_row-index
j=0
if all(lst[k][current_col]=="." for k in range (i+1, i+len(sequence[0])-1)):
    while i<len(lst[0]) and j<len(sequence[0]):
        lst[i][current_col] = sequence[0][j]
        i+=1
        j+=1
print(check_char)
print(check_char, current_char)
print(sequence)

for row in range(0,len(lst)):
    print(lst[row])
