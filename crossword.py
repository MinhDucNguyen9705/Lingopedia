from data_control import API_connect, meaning_get_from_API
import random
import asyncio

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
table = []
start = []
history = ""

async def create_table():
    global table,start
    start = []
    database = await API_connect()
    lst = []
    for i in range (len(database)):
        if all(database[i][j].isalpha() for j in range (0,len(database[i]))):
            lst.append(database[i])
    random.shuffle(lst)
    word_list = lst[:15]
    # print(word_list)
    word_list.sort(key=len,reverse=True)
    crossword.add_word(word_list[0],"down",3,3)
    for i in range (1,len(word_list)):
        current = 0
        index = find_collision_top(word_list[i])[0]
        row =  find_collision_top(word_list[i])[1]
        col = find_collision_top(word_list[i])[2]
        # print(index, row, col)
        if (crossword.board[row].count("-")>=len(crossword.board)-1):
            alpha = 0
            for j in range (0,len(word_list[i])):
                if crossword.board[row+1][col-index+j].isalpha():
                    alpha+=1
            # print(alpha)
            if alpha<=len(word_list[i]):
                start.append([word_list[i],row,col,"ngang"])
                crossword.add_word(word_list[i],"across",row, col-index)
                continue
        else:
            count=0
            for j in range (0,len(word_list[i])):
                if crossword.board[row+j][col].isalpha():
                    count+=1
            if count<=1 and crossword.board[row-1][col]=="-":
                start.append([word_list[i],row,col,"dọc"])
                crossword.add_word(word_list[i],"down",row-index,col)
                continue
        
        current = 0
        index = find_collision_bottom(word_list[i])[0]
        row =  find_collision_bottom(word_list[i])[1]
        col = find_collision_bottom(word_list[i])[2]

        # print(index, row, col)
        if (crossword.board[row].count("-")>=len(crossword.board)-1):
            alpha = 0
            for j in range (0,len(word_list[i])):
                if crossword.board[row+1][col-index+j].isalpha():
                    alpha+=1
            # print(alpha)
            if alpha<=len(word_list[i]):
                start.append([word_list[i],row,col,"ngang"])
                crossword.add_word(word_list[i],"across",row, col-index)
                continue
        else:
            count=0
            for j in range (0,len(word_list[i])):
                if crossword.board[row+j][col].isalpha():
                    count+=1
            if count<=1 and crossword.board[row-1][col]=="-":
                start.append([word_list[i],row,col,"dọc"])
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
    # crossword.display()
    for i in range (0,len(table)):
        for j in range (0,len(table[0])):
            if table[i][j].isalpha():
                table[i][j]=" "
    return start
# for i in range (0,len(table)):
#     print(table[i])
# for row in table:
#     print(" ".join(row))
# print("".join(crossword.board[4][3:3+len("necessary")]))

def guess(answer):
    global table, history
    right = False
    if len(answer)<=2:
        return False
    history+=answer
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
    # for row in table:
    #     print(" ".join(row))
    if right==True:
        return table
    else:
        return False
    
def clear_history():
    global history
    history = ""
    return history

async def hint_lookup():
    res = []
    global start
    for i in range (0,len(start)):
        res.append(f"{start[i][1],start[i][2]}, {start[i][3]}: {await meaning_get_from_API(start[i][0])[1]}")
    return res

def table_lookup():
    global table
    return table

# create_table()
# print(hint_lookup())
# print(table_lookup())
# print(start)
# print(create_table())
# while True:
#     res = input("Guess a word ")
#     print(guess(res))
#     print(table_lookup())
#     for row in table:
#         print(" ".join(row))
# print(find_collision_down("internet"))
# crossword.add_word("internet","across",2,3)
# crossword.add_word("evidence","down",2,3+3)

# game = crossword.display()
# print(game)