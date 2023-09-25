class Crossword:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = [["-" for i in range (row)] for j in range (col)]

    def display(self):
        for row in self.board:
            print(" ".join(row))

    def add_word(self, word, direction, start_row, start_col):
        if direction == "across":
            for i in range (0,len(word)):
                self.board[start_row][start_col+i] = word[i]
        if direction == "down":
            for i in range (0,len(word)):
                self.board[start_row+i][start_col] = word[i]

    def mark(self):
        number = 0
        for i in range (0,len(self.board)):
            self.board[i][0] = str(number)
            number+=1
            if i==len(self.board)-1:
                number=0
        for j in range (0,len(self.board)):
            self.board[0][j] = str(number)
            number+=1

crossword = Crossword(30,30)

word_list = ["internet","evidence","neuron","television","season","environment","telephone","necessary","love","cross","entry","hate","among","network","short","long","theorem"]

word_list.sort(key=len,reverse=True)

crossword.add_word(word_list[0],"down",3,3)

def find_collision_top(word):
    for c in word:
        for i in range (0,len(crossword.board)):
            for j in range (0,len(crossword.board[0])):
                if crossword.board[i][j]==c:
                    index = word.index(c)
                    current_row = i
                    current_col = j
                    return [index, current_row, current_col]

def find_collision_bottom(word):
    for c in word:
        for i in range (len(crossword.board)-1,-1,-1):
            for j in range (len(crossword.board[0])-1,-1,-1):
                if crossword.board[i][j]==c:
                    index = word.index(c)
                    current_row = i
                    current_col = j
                    return [index, current_row, current_col]

# index = find_collision_top(word_list[1])[0]
# row =  find_collision_top(word_list[1])[1]
# col = find_collision_top(word_list[1])[2]
# crossword.add_word(word_list[1],"across",row, col-index)

# index = find_collision_top(word_list[2])[0]
# row =  find_collision_top(word_list[2])[1]
# col = find_collision_top(word_list[2])[2]
# crossword.add_word(word_list[2],"across",row-index, col)
start = []

for i in range (1,len(word_list)):
    current = 0
    index = find_collision_top(word_list[i])[0]
    row =  find_collision_top(word_list[i])[1]
    col = find_collision_top(word_list[i])[2]
    print(index, row, col)
    if (crossword.board[row].count("-")>=len(crossword.board)-1):
        alpha = 0
        for j in range (0,len(word_list[i])):
            if crossword.board[row+1][col-index+j].isalpha():
                alpha+=1
        print(alpha)
        if alpha<=len(word_list[i]):
            start.append([word_list[i],row,col,"across"])
            crossword.add_word(word_list[i],"across",row, col-index)
            continue
    else:
        count=0
        for j in range (0,len(word_list[i])):
            if crossword.board[row+j][col].isalpha():
                count+=1
        if count<=1 and crossword.board[row-1][col]=="-":
            start.append([word_list[i],row,col,"down"])
            crossword.add_word(word_list[i],"down",row-index,col)
            continue
    
    current = 0
    index = find_collision_bottom(word_list[i])[0]
    row =  find_collision_bottom(word_list[i])[1]
    col = find_collision_bottom(word_list[i])[2]

    print(index, row, col)
    if (crossword.board[row].count("-")>=len(crossword.board)-1):
        alpha = 0
        for j in range (0,len(word_list[i])):
            if crossword.board[row+1][col-index+j].isalpha():
                alpha+=1
        print(alpha)
        if alpha<=len(word_list[i]):
            start.append([word_list[i],row,col,"across"])
            crossword.add_word(word_list[i],"across",row, col-index)
            continue
    else:
        count=0
        for j in range (0,len(word_list[i])):
            if crossword.board[row+j][col].isalpha():
                count+=1
        if count<=1 and crossword.board[row-1][col]=="-":
            start.append([word_list[i],row,col,"down"])
            crossword.add_word(word_list[i],"down",row-index,col)
            continue
for i in range (0,len(crossword.board)):
    if all(crossword.board[j]=="-" for j in range (0,len(crossword.board[0]))):
        crossword.board[i]=""
crossword.mark()
table = []
for i in range (0,len(crossword.board)):
    lst = []
    for j in range (0,len(crossword.board[0])):
        lst.append(crossword.board[i][j])
    table.append(lst)

number = 0
for i in range (0,len(table)):
    table[i][0] = str(number)
    number+=1
    if i==len(table)-1:
        number=0
for j in range (0,len(table)):
    table[0][j] = str(number)
    number+=1
crossword.display()
print(start)

for i in range (0,len(table)):
    for j in range (0,len(table[0])):
        if table[i][j].isalpha():
            table[i][j]=" "
# for i in range (0,len(table)):
#     print(table[i])

# print("".join(crossword.board[4][3:3+len("necessary")]))

def guess(answer):
    right = False
    for i in range (0,len(crossword.board)):
        for j in range (0,len(crossword.board[0])-len(answer)):
            if "".join(crossword.board[i][j:j+len(answer)])==answer:
               table[i][j:j+len(answer)]=list(answer)
               right=True
    for i in range (0,len(crossword.board)):
        for j in range (0,len(crossword.board[0])-len(answer)):
            if crossword.board[i][j].isalpha():
                s = crossword.board[i][j]
                current=i+1
                while crossword.board[current][j].isalpha():
                    s+=crossword.board[current][j]
                    current+=1
                    if s==answer:
                        now =0
                        for k in range (i,current):
                            table[k][j] = answer[now]
                            now+=1
                        right=True
    for row in table:
        print(" ".join(row))
    if right==True:
        return "Nice guess"
    else:
        return "Wrong! Try another word"

while True:
    res = input("Guess a word ")
    print(guess(res))
    # for row in table:
    #     print(" ".join(row))
# print(find_collision_down("internet"))
# crossword.add_word("internet","across",2,3)
# crossword.add_word("evidence","down",2,3+3)

# game = crossword.display()
# print(game)