#!/usr/bin/env python
import contextlib as __stickytape_contextlib

@__stickytape_contextlib.contextmanager
def __stickytape_temporary_dir():
    import tempfile
    import shutil
    dir_path = tempfile.mkdtemp()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)

with __stickytape_temporary_dir() as __stickytape_working_dir:
    def __stickytape_write_module(path, contents):
        import os, os.path

        def make_package(path):
            parts = path.split("/")
            partial_path = __stickytape_working_dir
            for part in parts:
                partial_path = os.path.join(partial_path, part)
                if not os.path.exists(partial_path):
                    os.mkdir(partial_path)
                    with open(os.path.join(partial_path, "__init__.py"), "wb") as f:
                        f.write(b"\n")

        make_package(os.path.dirname(path))

        full_path = os.path.join(__stickytape_working_dir, path)
        with open(full_path, "wb") as module_file:
            module_file.write(contents)

    import sys as __stickytape_sys
    __stickytape_sys.path.insert(0, __stickytape_working_dir)

    __stickytape_write_module('data_control.py', b'# Anh H\xe1\xba\xa3i l\xc3\xa0m ch\xe1\xbb\x97 n\xc3\xa0y\r\n\r\n# import database\r\n\r\n\r\nimport json\r\nfrom xclass_sdk import request\r\n# import requests\r\nimport asyncio\r\n\r\nasync def API_connect():\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/all_words/")\r\n    data = await database.json()\r\n    return data\r\n\r\nasync def meaning_get_from_API(word):\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/find_word/{word}")\r\n    data = await database.json()\r\n    return data\r\n\r\nasync def word_get_from_API(meaning):\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/find_meaning/{meaning}")\r\n    data = await database.json()\r\n    return data\r\n\r\n# def API_connect():\r\n#     url = "http://127.0.0.1:8000"\r\n#     database = requests.get(f"{url}/all_words/")\r\n#     data = json.loads(database.text)\r\n#     return data\r\n\r\n# print(API_connect())\r\n\r\n# def meaning_get_from_API(word):\r\n#     url = "http://127.0.0.1:8000"\r\n#     database = requests.get(f"{url}/find_word/{word}")\r\n#     data = json.loads(database.text)\r\n#     return data\r\n\r\nasync def post_word_to_API(word, meaning, topic):\r\n    url = "http://127.0.0.1:8000"\r\n    response = await request(f"{url}/find_word/", method = "POST", json = {"word" : {word}, "meaning" : {meaning}, "topic" : {topic}})\r\n    return await meaning_get_from_API(word)\r\n\r\n# print(await post_word_to_API("numerator", "t\xe1\xbb\xad s\xe1\xbb\x91"))\r\n# print(API_connect())\r\n# print(meaning_get_from_API("Consultant"))\r\n\r\nasync def find_word(prefix):\r\n    database = await API_connect()\r\n    response = []\r\n    prefix = prefix.lower()\r\n    # Prefix = word\r\n    for word in database:\r\n        if prefix == word or prefix==word.lower():\r\n            response.append(word)\r\n    # Longest common prefix\r\n    # string_list = []\r\n    # current=0\r\n    # while current<len(database):\r\n    #     string = ""\r\n    #     prefix_cursor = 0\r\n    #     temp_prefix = prefix+"1"\r\n    #     for i in range (0,len(database[word])):\r\n    #         if database[word][i]==temp_prefix[prefix_cursor]:\r\n    #             word_cursor = i\r\n    #             while (database[word][word_cursor]==temp_prefix[prefix_cursor] or database[word][word_cursor]==chr(ord(temp_prefix[prefix_cursor])-32)) and word_cursor<len(database[word])-1 and prefix_cursor<len(temp_prefix)-1:\r\n    #                 word_cursor+=1\r\n    #                 prefix_cursor+=1\r\n    #             string += database[word][i:word_cursor]\r\n    #     string_list.append(string)\r\n    # Prefix in word\r\n    for word in database:\r\n        if (prefix[0]==word[0] or prefix[0]==word[0].lower()) and (prefix in word or prefix in word.lower())  and len(response)<5 and word not in response:\r\n            response.append(word)\r\n    for word in database:\r\n        if (prefix in word or prefix in word.lower()) and len(response)<5 and word not in response:\r\n            response.append(word)\r\n    count_list = []\r\n    # Number of characters in prefix in each word\r\n    for word in database:\r\n        word_char = list(word)\r\n        characters = list(prefix)\r\n        i = 0\r\n        j = 0\r\n        count = 0\r\n        while i<len(word_char) and j<len(characters):\r\n            if word_char[i] == characters[j] or word_char[i] == chr(ord(characters[j])-32):\r\n                count+=1\r\n                word_char.pop(i)\r\n                characters.pop(j)\r\n            else:\r\n                i+=1\r\n            if i==len(word_char) and j<len(characters):\r\n                i=0\r\n                j+=1\r\n        count_list.append(count)\r\n    min_count = min(count_list)\r\n    max_count = max(count_list)\r\n    for i in range (max_count, min_count-1,-1):\r\n        for j in range (0,len(count_list)):\r\n            if count_list[j]==i and database[j] not in response:\r\n                response.append(database[j])\r\n    return response\r\n\r\nanswer = []\r\n\r\nasync def answer_1(prefix):\r\n    global answer\r\n    response = await find_word(prefix)\r\n    answer = []\r\n    for word in response:\r\n        if await meaning_get_from_API(word)!= {\'detail\': \'Not Found\'} and await meaning_get_from_API(word)!=None:\r\n            answer.append(await meaning_get_from_API(word))\r\n        else:\r\n            continue\r\n        if len(answer)>=5:\r\n            break\r\n    return answer\r\n\r\n\r\nasync def answer_2(prefix):\r\n    global answer\r\n    response = await find_word(prefix)\r\n    ans = []\r\n    for word in response:\r\n        if await meaning_get_from_API(word)!= {\'detail\': \'Not Found\'} and len(ans)<5 and await meaning_get_from_API(word) not in answer and await meaning_get_from_API(word)!=None:\r\n            ans.append(await meaning_get_from_API(word))\r\n        else:\r\n            continue\r\n        if len(ans)>=5:\r\n            break\r\n    answer = []\r\n    return ans\r\n\r\ndef history_write(history, word):\r\n    history.append(word)\r\n\r\ndef show_history(history):\r\n    return history')
    __stickytape_write_module('crossword.py', b'from data_control import API_connect, meaning_get_from_API\r\nimport random\r\nimport asyncio\r\n\r\nclass Crossword:\r\n    def __init__(self, row, col):\r\n        self.row = row\r\n        self.col = col\r\n        self.board = [["-" for i in range (row)] for j in range (col)]\r\n\r\n    def display(self):\r\n        for row in self.board:\r\n            print(" ".join(row))\r\n\r\n    def add_word(self, word, direction, start_row, start_col):\r\n        if direction == "across":\r\n            for i in range (0,len(word)):\r\n                self.board[start_row][start_col+i] = word[i]\r\n        if direction == "down":\r\n            for i in range (0,len(word)):\r\n                self.board[start_row+i][start_col] = word[i]\r\n\r\n    def mark(self):\r\n        number = 0\r\n        for i in range (0,len(self.board)):\r\n            self.board[i][0] = str(number)\r\n            number+=1\r\n            if i==len(self.board)-1:\r\n                number=0\r\n        for j in range (0,len(self.board)):\r\n            self.board[0][j] = str(number)\r\n            number+=1\r\n\r\ncrossword = Crossword(30,30)\r\n\r\n\r\n\r\ndef find_collision_top(word):\r\n    for c in word:\r\n        for i in range (0,len(crossword.board)):\r\n            for j in range (0,len(crossword.board[0])):\r\n                if crossword.board[i][j]==c:\r\n                    index = word.index(c)\r\n                    current_row = i\r\n                    current_col = j\r\n                    return [index, current_row, current_col]\r\n\r\ndef find_collision_bottom(word):\r\n    for c in word:\r\n        for i in range (len(crossword.board)-1,-1,-1):\r\n            for j in range (len(crossword.board[0])-1,-1,-1):\r\n                if crossword.board[i][j]==c:\r\n                    index = word.index(c)\r\n                    current_row = i\r\n                    current_col = j\r\n                    return [index, current_row, current_col]\r\n\r\n# index = find_collision_top(word_list[1])[0]\r\n# row =  find_collision_top(word_list[1])[1]\r\n# col = find_collision_top(word_list[1])[2]\r\n# crossword.add_word(word_list[1],"across",row, col-index)\r\n\r\n# index = find_collision_top(word_list[2])[0]\r\n# row =  find_collision_top(word_list[2])[1]\r\n# col = find_collision_top(word_list[2])[2]\r\n# crossword.add_word(word_list[2],"across",row-index, col)\r\ntable = []\r\nstart = []\r\nhistory = ""\r\n\r\nasync def create_table():\r\n    global table,start\r\n    start = []\r\n    database = await API_connect()\r\n    lst = []\r\n    for i in range (len(database)):\r\n        if all(database[i][j].isalpha() for j in range (0,len(database[i]))):\r\n            lst.append(database[i])\r\n    random.shuffle(lst)\r\n    word_list = lst[:15]\r\n    # print(word_list)\r\n    word_list.sort(key=len,reverse=True)\r\n    crossword.add_word(word_list[0],"down",3,3)\r\n    for i in range (1,len(word_list)):\r\n        current = 0\r\n        index = find_collision_top(word_list[i])[0]\r\n        row =  find_collision_top(word_list[i])[1]\r\n        col = find_collision_top(word_list[i])[2]\r\n        # print(index, row, col)\r\n        if (crossword.board[row].count("-")>=len(crossword.board)-1):\r\n            alpha = 0\r\n            for j in range (0,len(word_list[i])):\r\n                if crossword.board[row+1][col-index+j].isalpha():\r\n                    alpha+=1\r\n            # print(alpha)\r\n            if alpha<=len(word_list[i]):\r\n                start.append([word_list[i],row,col,"ngang"])\r\n                crossword.add_word(word_list[i],"across",row, col-index)\r\n                continue\r\n        else:\r\n            count=0\r\n            for j in range (0,len(word_list[i])):\r\n                if crossword.board[row+j][col].isalpha():\r\n                    count+=1\r\n            if count<=1 and crossword.board[row-1][col]=="-":\r\n                start.append([word_list[i],row,col,"d\xe1\xbb\x8dc"])\r\n                crossword.add_word(word_list[i],"down",row-index,col)\r\n                continue\r\n        \r\n        current = 0\r\n        index = find_collision_bottom(word_list[i])[0]\r\n        row =  find_collision_bottom(word_list[i])[1]\r\n        col = find_collision_bottom(word_list[i])[2]\r\n\r\n        # print(index, row, col)\r\n        if (crossword.board[row].count("-")>=len(crossword.board)-1):\r\n            alpha = 0\r\n            for j in range (0,len(word_list[i])):\r\n                if crossword.board[row+1][col-index+j].isalpha():\r\n                    alpha+=1\r\n            # print(alpha)\r\n            if alpha<=len(word_list[i]):\r\n                start.append([word_list[i],row,col,"ngang"])\r\n                crossword.add_word(word_list[i],"across",row, col-index)\r\n                continue\r\n        else:\r\n            count=0\r\n            for j in range (0,len(word_list[i])):\r\n                if crossword.board[row+j][col].isalpha():\r\n                    count+=1\r\n            if count<=1 and crossword.board[row-1][col]=="-":\r\n                start.append([word_list[i],row,col,"d\xe1\xbb\x8dc"])\r\n                crossword.add_word(word_list[i],"down",row-index,col)\r\n                continue\r\n    for i in range (0,len(crossword.board)):\r\n        if all(crossword.board[j]=="-" for j in range (0,len(crossword.board[0]))):\r\n            crossword.board[i]=""\r\n    crossword.mark()\r\n    table = []\r\n    for i in range (0,len(crossword.board)):\r\n        lst = []\r\n        for j in range (0,len(crossword.board[0])):\r\n            lst.append(crossword.board[i][j])\r\n        table.append(lst)\r\n    \r\n    number = 0\r\n    for i in range (0,len(table)):\r\n        table[i][0] = str(number)\r\n        number+=1\r\n        if i==len(table)-1:\r\n            number=0\r\n    for j in range (0,len(table)):\r\n        table[0][j] = str(number)\r\n        number+=1\r\n    # crossword.display()\r\n    for i in range (0,len(table)):\r\n        for j in range (0,len(table[0])):\r\n            if table[i][j].isalpha():\r\n                table[i][j]=" "\r\n    return start\r\n# for i in range (0,len(table)):\r\n#     print(table[i])\r\n# for row in table:\r\n#     print(" ".join(row))\r\n# print("".join(crossword.board[4][3:3+len("necessary")]))\r\n\r\ndef guess(answer):\r\n    global table, history\r\n    right = False\r\n    if len(answer)<=2:\r\n        return False\r\n    history+=answer\r\n    for i in range (0,len(crossword.board)):\r\n        for j in range (0,len(crossword.board[0])-len(answer)):\r\n            if "".join(crossword.board[i][j:j+len(answer)])==answer:\r\n               table[i][j:j+len(answer)]=list(answer)\r\n               right=True\r\n    for i in range (0,len(crossword.board)):\r\n        for j in range (0,len(crossword.board[0])-len(answer)):\r\n            if crossword.board[i][j].isalpha():\r\n                s = crossword.board[i][j]\r\n                current=i+1\r\n                while crossword.board[current][j].isalpha():\r\n                    s+=crossword.board[current][j]\r\n                    current+=1\r\n                    if s==answer:\r\n                        now =0\r\n                        for k in range (i,current):\r\n                            table[k][j] = answer[now]\r\n                            now+=1\r\n                        right=True\r\n    # for row in table:\r\n    #     print(" ".join(row))\r\n    if right==True:\r\n        return table\r\n    else:\r\n        return False\r\n    \r\ndef clear_history():\r\n    global history\r\n    history = ""\r\n    return history\r\n\r\nasync def hint_lookup():\r\n    res = []\r\n    global start\r\n    for i in range (0,len(start)):\r\n        res.append(f"{start[i][1],start[i][2]}, {start[i][3]}: {await meaning_get_from_API(start[i][0])[1]}")\r\n    return res\r\n\r\ndef table_lookup():\r\n    global table\r\n    return table\r\n\r\n# create_table()\r\n# print(hint_lookup())\r\n# print(table_lookup())\r\n# print(start)\r\n# print(create_table())\r\n# while True:\r\n#     res = input("Guess a word ")\r\n#     print(guess(res))\r\n#     print(table_lookup())\r\n#     for row in table:\r\n#         print(" ".join(row))\r\n# print(find_collision_down("internet"))\r\n# crossword.add_word("internet","across",2,3)\r\n# crossword.add_word("evidence","down",2,3+3)\r\n\r\n# game = crossword.display()\r\n# print(game)')
    __stickytape_write_module('game.py', b'import json\r\nfrom xclass_sdk import request\r\nimport random\r\nimport asyncio\r\n\r\nasync def API_connect():\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/all_words/")\r\n    data = await database.json()\r\n    return data\r\n\r\nasync def meaning_get_from_API(word):\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/find_word/{word}")\r\n    data = await database.json()\r\n    return data\r\n\r\n# print(meaning_get_from_API("Online Course")[1].strip(" "))\r\n\r\nasync def topic_get_from_API(word):\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/find_topic/{word}")\r\n    data = await database.json()\r\n    return data\r\n\r\ntopic = ["y h\xe1\xbb\x8dc","c\xc3\xb4ng ngh\xe1\xbb\x87 th\xc3\xb4ng tin","gi\xc3\xa1o d\xe1\xbb\xa5c","l\xe1\xbb\x8bch s\xe1\xbb\xad","sinh h\xe1\xbb\x8dc","v\xe1\xba\xadt l\xc3\xbd","gia d\xe1\xbb\xa5ng","\xe1\xba\xa9m th\xe1\xbb\xb1c","c\xc3\xb4ng s\xe1\xbb\x9f","x\xc3\xa2y d\xe1\xbb\xb1ng","ngh\xe1\xbb\x87 thu\xe1\xba\xadt", "th\xe1\xbb\x83 thao","m\xc3\xa0u s\xe1\xba\xafc","\xc4\x91\xe1\xbb\x99ng v\xe1\xba\xadt","\xc4\x91\xe1\xba\xa1i d\xc6\xb0\xc6\xa1ng","ti\xe1\xbb\x81n s\xe1\xbb\xad","ph\xc6\xb0\xc6\xa1ng ti\xe1\xbb\x87n giao th\xc3\xb4ng","c\xc6\xa1 th\xe1\xbb\x83"]\r\n\r\nasync def randomize(topic):\r\n    lst = await topic_get_from_API(topic)\r\n    random.shuffle(lst)\r\n    words = lst[:4]\r\n    ans = random.choice(words)\r\n    return words, ans\r\n\r\ndef verify(word, ans):\r\n    if word == ans:\r\n        return True\r\n    else:\r\n        return False\r\n\r\n# print(randomize("gi\xc3\xa1o d\xe1\xbb\xa5c"))\r\n# print(verify("Academic Standards"))\r\n# print(verify("Student Assessment"))\r\n# print(verify("Distance Learning"))\r\n# print(verify("Online Course"))')
    from data_control import find_word, answer_1, answer_2, post_word_to_API, word_get_from_API, history_write, show_history, meaning_get_from_API
    import crossword
    from game import randomize, verify
    import asyncio
    
    status = "greeting"
    count = 0
    satisfaction = True
    no_count = 0
    word_asked = False
    meaning_asked = False
    tu = ""
    nghia = ""
    res = ""
    finding = ""
    ans = ""
    answer_map = {"A": "", "B":"","C": "", "D":""}
    
    history = []
    async def output(message):
        global status, count, satisfaction, no_count, word_asked, tu, res, finding, history, ans, answer_map, meaning_asked, nghia
        accept = ["ok","có","được","đồng ý","yes"]
        deny = ["ko","không","no","từ chối"]
        look_up_cases = ["tim tu", "tìm từ", "tìm kiếm", "tìm từ","1"]
        topics = ["y học","công nghệ thông tin","giáo dục","lịch sử","sinh học","vật lý","gia dụng","ẩm thực","công sở","xây dựng","nghệ thuật", "thể thao","màu sắc","động vật","đại dương","tiền sử","phương tiện giao thông","cơ thể"]
        mapping = {"1": "y học", "2":"công nghệ thông tin", "3":"giáo dục","4":"lịch sử","5":"sinh học","6":"vật lý","7":"gia dụng","8":"ẩm thực","9":"công sở","10":"xây dựng","11":"nghệ thuật","12":"thể thao","13":"màu sắc","14":"động vật","15":"đại dương","16":"tiền sử","17":"phương tiện giao thông","18":"cơ thể"}
        if message.lower() == "quit":
            status = "greeting"
            return "Xin chào và hẹn gặp lại"
        if status=="greeting":
            status = "option"
            response = []
            response.append(f"Xin chào {message}. Mời bạn lựa chọn một trong những chức năng dưới đây:")
            response.append("1. Tìm nghĩa của từ cho trước")
            response.append("2. Chơi trò chơi để học từ mới")
            response.append("3. Đóng góp thêm vào từ điển hiện tại")
            response.append("4. Tìm từ qua nghĩa của từ")
            response.append("5. Xem lịch sử tìm kiếm")
            return response
        elif status=="option":
            if message in look_up_cases:
                status = "look up word"
                return "Mời nhập từ bạn cần tìm"
            elif message=="2":
                status = "topic"
                response = []
                response.append("Mời bạn chọn một trong những chủ đề sau:")
                for i in range (len(topics)):
                    response.append("{0}. {1}".format(i+1, topics[i]))
                return response
                # try:
                #     status = "crossword"
                #     await crossword.create_table()
                #     # status = "crossword_step2"
                #     res = await crossword.hint_lookup()
                #     traloi = []
                #     table = crossword.table_lookup()
                #     for line in res:
                #         traloi.append(line+"\n")
                #     for row in table:
                #         traloi.append(" ".join(row)+"\n")
                #     return traloi
                # except IndexError:
                #     status = "crossword"
                #     await crossword.create_table()
                #     # status = "crossword_step2"
                #     res = await crossword.hint_lookup()
                #     traloi = []
                #     table = crossword.table_lookup()
                #     for line in res:
                #         traloi.append(line+"\n")
                #     for row in table:
                #         traloi.append(" ".join(row)+"\n")
                #     return traloi
                # return "Tro choi bat dau"
            elif message == "3":
                status = "add word"
                return "Nhập từ bạn muốn thêm"
            elif message == "4":
                status = "find meaning"
                return "Hãy nhập nghĩa của từ mà bạn muốn tìm"
            elif message == "5":
                if len(history)==0:
                    return "Hiện chưa có gì ở trong lịch sử cả. Hãy bắt đầu tìm kiếm ngay nhé!"
                else:
                    return show_history(history)
            else:
                return "Mời bạn nhập lại lệnh"
        elif status == "topic":
            status = "guess"
            response = []
            random = await randomize(mapping[str(message)])
            words = random[0]
            ans = random[1]
            response.append("Từ nào mang ý nghĩa sau: {0}".format((await meaning_get_from_API(ans))[1]))
            for i in range (len(words)):
                response.append("{0}. {1}".format(chr(65+i),words[i]))
                answer_map[chr(65+i)]=words[i]
            return response
        elif status == "guess":
            if message not in list(answer_map.keys()):
                return "Vui lòng chọn đáp án hợp lệ"
            else:
                if verify(answer_map[message], ans):
                    status = "option"
                    ans = ""
                    return "Câu trả lời rất chính xác. Để tiếp tục hãy chọn lại tính năng (1-5)"
                else:
                    return "Chưa chính xác, hãy thử lại nhé!"
        elif status == "find meaning":
            status = "option"
            history_write(history, message)
            try:
                if len(await word_get_from_API(message))>=5:
                    response =  [f"{_[0]} : {_[1]}" for _ in (await word_get_from_API(message))[0:5]]
                    return response
                elif len(await word_get_from_API(message))<5:
                    response =  [f"{_[0]} : {_[1]}" for _ in (await word_get_from_API(message))[0:]]
                    return response
                elif len(await word_get_from_API(message))==0:
                    return "Từ này hiện chưa có trong từ điển"
            except OSError:
                return "Lỗi nhập từ hoặc từ này chưa có trong từ điển. Hãy chọn lại lệnh để tiếp tục (1-5)"
        elif status == "look up word":
            status = "satisfaction_judge"
            if satisfaction == True:
                finding = message
                history_write(history, message)
                word_list = await answer_1(message)
                answer = ["Những từ bạn cần tìm như sau: \n"]
                for word in word_list:
                    answer.append("{0} : {1}\n".format(word[0].replace("%20"," "), word[1]))
                answer.append("Bạn có hài lòng với kết quả không? ")
                return answer
            else:
                satisfaction=True
                word_list = await answer_2(finding)
                finding = ""
                answer = ["5 từ gần nhất được tìm thấy: "]
                for word in word_list:
                    answer.append("{0} : {1}\n".format(word[0].replace("%20"," "), word[1]))
                answer.append("Từ bạn tìm kiếm có trong này ko?")
                return answer
        elif status=="satisfaction_judge":
            if message.lower() in accept:
                status = "option"
                if no_count>0:
                    no_count-=1
                # return chat.back_to_option
                return "Hãy chọn tính năng để tiếp tục (1-5)"
            elif message.lower() in deny:
                if no_count<1:
                    satisfaction = False
                    no_count+=1
                    status = "look up word"
                    return "Nhấn ENTER để bắt đầu tìm kiếm tiếp"
                else:
                    no_count = 0
                    status = "add word pending"
                    return "Có thể từ này hiện chưa có trong từ điển của chúng tôi. Bạn có thể giúp chúng tôi thêm nó vào không?"
            else:
                return "Hãy trả lời có hoặc không để chúng tôi biết nhé!"
        elif status == "add word pending":
            if message.lower() in accept:
                status = "add word"
                return "Vui lòng nhập từ bạn muốn thêm"
            elif message.lower() in deny:
                status = "option"
                return "Vậy thì hãy nhập lại lệnh để tiếp tục (1-5)"
        elif status == "add word":
            if word_asked == False and meaning_asked == False:
                tu = ""
                tu = message
                word_asked = True
                return "Mời bạn nhập nghĩa"
            elif word_asked == True and meaning_asked == False:
                meaning_asked = True
                nghia = message
                return "Mời bạn nhập chủ đề của từ"
            else:
                word_asked = False
                meaning_asked = False
                status = "option"
                return await post_word_to_API(tu, nghia, message)
        # elif status == "crossword":
        #     if count<len(res):
        #         if crossword.guess(message)!=False:
        #             count+=1
        #             response = []
        #             response.append(f"Ban da tra loi dung, con lai {len(res)-count} tu \n")
        #             current = crossword.guess(message)
        #             for line in current:
        #                 response.append(" ".join(line) + "\n")
        #             return response
        #         else:
        #             return "Moi ban doan lai"
        #     else:
        #         status = "option"
        #         count = 0
        #         crossword.clear_history()
        #         return "Ban da thang, tro choi ket thuc. Hay chon lai tinh nang de tiep tuc"
        else:
            return "Sai cú pháp. Vui lòng nhập lệnh hợp lệ"
        # elif status == "crossword"
    # while True:
    #     message = input()
    #     print(output(message))