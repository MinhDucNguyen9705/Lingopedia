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

    __stickytape_write_module('data_control.py', b'import json\r\nfrom xclass_sdk import request\r\nimport asyncio\r\n\r\nasync def API_connect():\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/all_words/")\r\n    data = await database.json()\r\n    return data\r\n\r\nasync def meaning_get_from_API(word):\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/find_word/{word}")\r\n    data = await database.json()\r\n    return data\r\n\r\nasync def word_get_from_API(meaning):\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/find_meaning/{meaning}")\r\n    data = await database.json()\r\n    return data\r\n\r\nasync def post_word_to_API(word, meaning, topic):\r\n    url = "http://127.0.0.1:8000"\r\n    info = {\'tu\': "", \'nghia\': "", "chu_de" : ""}\r\n    info[\'tu\'] = word\r\n    info[\'nghia\']= meaning\r\n    info[\'chu_de\'] = topic\r\n    header = {\'Content-Type\':\'application/json\'}\r\n    response = await request(f"{url}/find_word/", method = "POST", body = json.dumps(info), headers = header)\r\n    # find = word.replace("%20"," ")\r\n    return "\xc4\x90\xc3\xa3 th\xc3\xaam th\xc3\xa0nh c\xc3\xb4ng!"\r\n\r\n\r\nasync def find_word(prefix):\r\n    database = await API_connect()\r\n    response = []\r\n    prefix = prefix.lower()\r\n    # Prefix = word\r\n    for word in database:\r\n        if prefix == word or prefix==word.lower():\r\n            response.append(word)\r\n    # Prefix in word\r\n    for word in database:\r\n        if (prefix[0]==word[0] or prefix[0]==word[0].lower()) and (prefix in word or prefix in word.lower())  and len(response)<5 and word not in response:\r\n            response.append(word)\r\n    for word in database:\r\n        if (prefix in word or prefix in word.lower()) and len(response)<5 and word not in response:\r\n            response.append(word)\r\n    count_list = []\r\n    # Number of characters in prefix in each word\r\n    for word in database:\r\n        word_char = list(word)\r\n        characters = list(prefix)\r\n        i = 0\r\n        j = 0\r\n        count = 0\r\n        while i<len(word_char) and j<len(characters):\r\n            if word_char[i] == characters[j] or word_char[i] == chr(ord(characters[j])-32):\r\n                count+=1\r\n                word_char.pop(i)\r\n                characters.pop(j)\r\n            else:\r\n                i+=1\r\n            if i==len(word_char) and j<len(characters):\r\n                i=0\r\n                j+=1\r\n        count_list.append(count)\r\n    min_count = min(count_list)\r\n    max_count = max(count_list)\r\n    for i in range (max_count, min_count-1,-1):\r\n        for j in range (0,len(count_list)):\r\n            if count_list[j]==i and database[j] not in response:\r\n                response.append(database[j])\r\n    return response\r\n\r\nanswer = []\r\n\r\nasync def answer_1(prefix):\r\n    global answer\r\n    response = await find_word(prefix)\r\n    answer = []\r\n    for word in response:\r\n        if await meaning_get_from_API(word)!= {\'detail\': \'Not Found\'} and await meaning_get_from_API(word)!=None:\r\n            answer.append(await meaning_get_from_API(word))\r\n        else:\r\n            continue\r\n        if len(answer)>=5:\r\n            break\r\n    return answer\r\n\r\n\r\nasync def answer_2(prefix):\r\n    global answer\r\n    response = await find_word(prefix)\r\n    ans = []\r\n    for word in response:\r\n        if await meaning_get_from_API(word)!= {\'detail\': \'Not Found\'} and len(ans)<5 and await meaning_get_from_API(word) not in answer and await meaning_get_from_API(word)!=None:\r\n            ans.append(await meaning_get_from_API(word))\r\n        else:\r\n            continue\r\n        if len(ans)>=5:\r\n            break\r\n    answer = []\r\n    return ans\r\n\r\ndef history_write(history, word):\r\n    history.append(word)\r\n\r\ndef show_history(history):\r\n    return history')
    __stickytape_write_module('crossword.py', b'from data_control import API_connect, meaning_get_from_API\r\nimport random\r\nimport asyncio\r\n\r\nclass Crossword:\r\n    def __init__(self, row, col):\r\n        self.row = row\r\n        self.col = col\r\n        self.board = [["-" for i in range (row)] for j in range (col)]\r\n\r\n    def display(self):\r\n        for row in self.board:\r\n            print(" ".join(row))\r\n\r\n    def add_word(self, word, direction, start_row, start_col):\r\n        if direction == "across":\r\n            for i in range (0,len(word)):\r\n                self.board[start_row][start_col+i] = word[i]\r\n        if direction == "down":\r\n            for i in range (0,len(word)):\r\n                self.board[start_row+i][start_col] = word[i]\r\n\r\n    def mark(self):\r\n        number = 0\r\n        for i in range (0,len(self.board)):\r\n            self.board[i][0] = str(number)\r\n            number+=1\r\n            if i==len(self.board)-1:\r\n                number=0\r\n        for j in range (0,len(self.board)):\r\n            self.board[0][j] = str(number)\r\n            number+=1\r\n\r\ncrossword = Crossword(30,30)\r\n\r\n\r\n\r\ndef find_collision_top(word):\r\n    for c in word:\r\n        for i in range (0,len(crossword.board)):\r\n            for j in range (0,len(crossword.board[0])):\r\n                if crossword.board[i][j]==c:\r\n                    index = word.index(c)\r\n                    current_row = i\r\n                    current_col = j\r\n                    return [index, current_row, current_col]\r\n\r\ndef find_collision_bottom(word):\r\n    for c in word:\r\n        for i in range (len(crossword.board)-1,-1,-1):\r\n            for j in range (len(crossword.board[0])-1,-1,-1):\r\n                if crossword.board[i][j]==c:\r\n                    index = word.index(c)\r\n                    current_row = i\r\n                    current_col = j\r\n                    return [index, current_row, current_col]\r\n\r\n# index = find_collision_top(word_list[1])[0]\r\n# row =  find_collision_top(word_list[1])[1]\r\n# col = find_collision_top(word_list[1])[2]\r\n# crossword.add_word(word_list[1],"across",row, col-index)\r\n\r\n# index = find_collision_top(word_list[2])[0]\r\n# row =  find_collision_top(word_list[2])[1]\r\n# col = find_collision_top(word_list[2])[2]\r\n# crossword.add_word(word_list[2],"across",row-index, col)\r\ntable = []\r\nstart = []\r\nhistory = ""\r\n\r\nasync def create_table():\r\n    global table,start\r\n    start = []\r\n    database = await API_connect()\r\n    lst = []\r\n    for i in range (len(database)):\r\n        if all(database[i][j].isalpha() for j in range (0,len(database[i]))):\r\n            lst.append(database[i])\r\n    random.shuffle(lst)\r\n    word_list = lst[:15]\r\n    # print(word_list)\r\n    word_list.sort(key=len,reverse=True)\r\n    crossword.add_word(word_list[0],"down",3,3)\r\n    for i in range (1,len(word_list)):\r\n        current = 0\r\n        index = find_collision_top(word_list[i])[0]\r\n        row =  find_collision_top(word_list[i])[1]\r\n        col = find_collision_top(word_list[i])[2]\r\n        # print(index, row, col)\r\n        if (crossword.board[row].count("-")>=len(crossword.board)-1):\r\n            alpha = 0\r\n            for j in range (0,len(word_list[i])):\r\n                if crossword.board[row+1][col-index+j].isalpha():\r\n                    alpha+=1\r\n            # print(alpha)\r\n            if alpha<=len(word_list[i]):\r\n                start.append([word_list[i],row,col,"ngang"])\r\n                crossword.add_word(word_list[i],"across",row, col-index)\r\n                continue\r\n        else:\r\n            count=0\r\n            for j in range (0,len(word_list[i])):\r\n                if crossword.board[row+j][col].isalpha():\r\n                    count+=1\r\n            if count<=1 and crossword.board[row-1][col]=="-":\r\n                start.append([word_list[i],row,col,"d\xe1\xbb\x8dc"])\r\n                crossword.add_word(word_list[i],"down",row-index,col)\r\n                continue\r\n        \r\n        current = 0\r\n        index = find_collision_bottom(word_list[i])[0]\r\n        row =  find_collision_bottom(word_list[i])[1]\r\n        col = find_collision_bottom(word_list[i])[2]\r\n\r\n        # print(index, row, col)\r\n        if (crossword.board[row].count("-")>=len(crossword.board)-1):\r\n            alpha = 0\r\n            for j in range (0,len(word_list[i])):\r\n                if crossword.board[row+1][col-index+j].isalpha():\r\n                    alpha+=1\r\n            # print(alpha)\r\n            if alpha<=len(word_list[i]):\r\n                start.append([word_list[i],row,col,"ngang"])\r\n                crossword.add_word(word_list[i],"across",row, col-index)\r\n                continue\r\n        else:\r\n            count=0\r\n            for j in range (0,len(word_list[i])):\r\n                if crossword.board[row+j][col].isalpha():\r\n                    count+=1\r\n            if count<=1 and crossword.board[row-1][col]=="-":\r\n                start.append([word_list[i],row,col,"d\xe1\xbb\x8dc"])\r\n                crossword.add_word(word_list[i],"down",row-index,col)\r\n                continue\r\n    for i in range (0,len(crossword.board)):\r\n        if all(crossword.board[j]=="-" for j in range (0,len(crossword.board[0]))):\r\n            crossword.board[i]=""\r\n    crossword.mark()\r\n    table = []\r\n    for i in range (0,len(crossword.board)):\r\n        lst = []\r\n        for j in range (0,len(crossword.board[0])):\r\n            lst.append(crossword.board[i][j])\r\n        table.append(lst)\r\n    \r\n    number = 0\r\n    for i in range (0,len(table)):\r\n        table[i][0] = str(number)\r\n        number+=1\r\n        if i==len(table)-1:\r\n            number=0\r\n    for j in range (0,len(table)):\r\n        table[0][j] = str(number)\r\n        number+=1\r\n    # crossword.display()\r\n    for i in range (0,len(table)):\r\n        for j in range (0,len(table[0])):\r\n            if table[i][j].isalpha():\r\n                table[i][j]=" "\r\n    return start\r\n# for i in range (0,len(table)):\r\n#     print(table[i])\r\n# for row in table:\r\n#     print(" ".join(row))\r\n# print("".join(crossword.board[4][3:3+len("necessary")]))\r\n\r\ndef guess(answer):\r\n    global table, history\r\n    right = False\r\n    if len(answer)<=2:\r\n        return False\r\n    history+=answer\r\n    for i in range (0,len(crossword.board)):\r\n        for j in range (0,len(crossword.board[0])-len(answer)):\r\n            if "".join(crossword.board[i][j:j+len(answer)])==answer:\r\n               table[i][j:j+len(answer)]=list(answer)\r\n               right=True\r\n    for i in range (0,len(crossword.board)):\r\n        for j in range (0,len(crossword.board[0])-len(answer)):\r\n            if crossword.board[i][j].isalpha():\r\n                s = crossword.board[i][j]\r\n                current=i+1\r\n                while crossword.board[current][j].isalpha():\r\n                    s+=crossword.board[current][j]\r\n                    current+=1\r\n                    if s==answer:\r\n                        now =0\r\n                        for k in range (i,current):\r\n                            table[k][j] = answer[now]\r\n                            now+=1\r\n                        right=True\r\n    # for row in table:\r\n    #     print(" ".join(row))\r\n    if right==True:\r\n        return table\r\n    else:\r\n        return False\r\n    \r\ndef clear_history():\r\n    global history\r\n    history = ""\r\n    return history\r\n\r\nasync def hint_lookup():\r\n    res = []\r\n    global start\r\n    for i in range (0,len(start)):\r\n        res.append(f"{start[i][1],start[i][2]}, {start[i][3]}: {await meaning_get_from_API(start[i][0])[1]}")\r\n    return res\r\n\r\ndef table_lookup():\r\n    global table\r\n    return table\r\n\r\n# create_table()\r\n# print(hint_lookup())\r\n# print(table_lookup())\r\n# print(start)\r\n# print(create_table())\r\n# while True:\r\n#     res = input("Guess a word ")\r\n#     print(guess(res))\r\n#     print(table_lookup())\r\n#     for row in table:\r\n#         print(" ".join(row))\r\n# print(find_collision_down("internet"))\r\n# crossword.add_word("internet","across",2,3)\r\n# crossword.add_word("evidence","down",2,3+3)\r\n\r\n# game = crossword.display()\r\n# print(game)')
    __stickytape_write_module('game.py', b'import json\r\nfrom xclass_sdk import request\r\nimport random\r\nimport asyncio\r\n\r\nasync def API_connect():\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/all_words/")\r\n    data = await database.json()\r\n    return data\r\n\r\nasync def meaning_get_from_API(word):\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/find_word/{word}")\r\n    data = await database.json()\r\n    return data\r\n\r\n# print(meaning_get_from_API("Online Course")[1].strip(" "))\r\n\r\nasync def topic_get_from_API(word):\r\n    url = "http://127.0.0.1:8000"\r\n    database = await request(f"{url}/find_topic/{word}")\r\n    data = await database.json()\r\n    return data\r\n\r\ntopic = ["y h\xe1\xbb\x8dc","c\xc3\xb4ng ngh\xe1\xbb\x87 th\xc3\xb4ng tin","gi\xc3\xa1o d\xe1\xbb\xa5c","l\xe1\xbb\x8bch s\xe1\xbb\xad","sinh h\xe1\xbb\x8dc","v\xe1\xba\xadt l\xc3\xbd","gia d\xe1\xbb\xa5ng","\xe1\xba\xa9m th\xe1\xbb\xb1c","c\xc3\xb4ng s\xe1\xbb\x9f","x\xc3\xa2y d\xe1\xbb\xb1ng","ngh\xe1\xbb\x87 thu\xe1\xba\xadt", "th\xe1\xbb\x83 thao","m\xc3\xa0u s\xe1\xba\xafc","\xc4\x91\xe1\xbb\x99ng v\xe1\xba\xadt","\xc4\x91\xe1\xba\xa1i d\xc6\xb0\xc6\xa1ng","ti\xe1\xbb\x81n s\xe1\xbb\xad","ph\xc6\xb0\xc6\xa1ng ti\xe1\xbb\x87n giao th\xc3\xb4ng","c\xc6\xa1 th\xe1\xbb\x83"]\r\n\r\nasync def randomize(topic):\r\n    lst = await topic_get_from_API(topic)\r\n    random.shuffle(lst)\r\n    words = lst[:4]\r\n    ans = random.choice(words)\r\n    return words, ans\r\n\r\ndef verify(word, ans):\r\n    if word == ans:\r\n        return True\r\n    else:\r\n        return False\r\n\r\n# print(randomize("gi\xc3\xa1o d\xe1\xbb\xa5c"))\r\n# print(verify("Academic Standards"))\r\n# print(verify("Student Assessment"))\r\n# print(verify("Distance Learning"))\r\n# print(verify("Online Course"))')
    __stickytape_write_module('chat.py', b'# Ch\xe1\xbb\x8b nguy\xe1\xbb\x87t l\xc3\xa0m ch\xe1\xbb\x97 n\xc3\xa0y\r\nfrom data_control import answer_1, answer_2, word_get_from_API\r\n#status 1: t\xc3\xadnh n\xc4\x83ng ch\xc3\xa0o h\xe1\xbb\x8fi\r\nasync def greet_user(name):\r\n    response = []\r\n    response.append(f"Xin ch\xc3\xa0o {name}. M\xe1\xbb\x9di b\xe1\xba\xa1n l\xe1\xbb\xb1a ch\xe1\xbb\x8dn m\xe1\xbb\x99t trong nh\xe1\xbb\xafng ch\xe1\xbb\xa9c n\xc4\x83ng d\xc6\xb0\xe1\xbb\x9bi \xc4\x91\xc3\xa2y:")\r\n    response.append("1. T\xc3\xacm ngh\xc4\xa9a c\xe1\xbb\xa7a t\xe1\xbb\xab cho tr\xc6\xb0\xe1\xbb\x9bc")\r\n    response.append("2. Ch\xc6\xa1i tr\xc3\xb2 ch\xc6\xa1i \xc4\x91\xe1\xbb\x83 h\xe1\xbb\x8dc t\xe1\xbb\xab m\xe1\xbb\x9bi")\r\n    response.append("3. \xc4\x90\xc3\xb3ng g\xc3\xb3p th\xc3\xaam v\xc3\xa0o t\xe1\xbb\xab \xc4\x91i\xe1\xbb\x83n hi\xe1\xbb\x87n t\xe1\xba\xa1i")\r\n    response.append("4. T\xc3\xacm t\xe1\xbb\xab qua ngh\xc4\xa9a c\xe1\xbb\xa7a t\xe1\xbb\xab")\r\n    response.append("5. Xem l\xe1\xbb\x8bch s\xe1\xbb\xad t\xc3\xacm ki\xe1\xba\xbfm")\r\n    response.append("Nh\xe1\xba\xa5n QUIT \xc4\x91\xe1\xbb\x83 r\xe1\xbb\x9di kh\xe1\xbb\x8fi ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh")\r\n    return response\r\n\r\n#status 2: t\xc3\xadnh n\xc4\x83ng tra t\xe1\xbb\xab\r\n#2.1 Tra l\xe1\xba\xa7n \xc4\x91\xe1\xba\xa7u ti\xc3\xaan\r\nasync def lookup_word_1(keyword):\r\n    word_list = await answer_1(keyword)\r\n    answer = ["Nh\xe1\xbb\xafng t\xe1\xbb\xab b\xe1\xba\xa1n c\xe1\xba\xa7n t\xc3\xacm nh\xc6\xb0 sau: \\n"]\r\n    for word in word_list:\r\n        answer.append("{0} : {1}\\n".format(word[0].replace("%20"," "), word[1]))\r\n    answer.append("B\xe1\xba\xa1n y\xc3\xaau c\xc3\xb3 h\xc3\xa0i l\xc3\xb2ng v\xe1\xbb\x9bi k\xe1\xba\xbft qu\xe1\xba\xa3 n\xc3\xa0y kh\xc3\xb4ng?")\r\n    return answer\r\n\r\n#2.2 Tra l\xe1\xba\xa7n th\xe1\xbb\xa9 2 n\xe1\xba\xbfu ch\xc6\xb0a h\xc3\xa0i l\xc3\xb2ng\r\nasync def lookup_word_2(keyword):\r\n    word_list = await answer_2(keyword)\r\n    answer = ["Sau \xc4\x91\xc3\xa2y l\xc3\xa0 k\xe1\xba\xbft qu\xe1\xba\xa3 tra c\xe1\xbb\xa9u kh\xc3\xa1c: "]\r\n    for word in word_list:\r\n        answer.append("{0} : {1}\\n".format(word[0].replace("%20"," "), word[1]))\r\n    answer.append("B\xe1\xba\xa1n y\xc3\xaau c\xc3\xb3 h\xc3\xa0i l\xc3\xb2ng v\xe1\xbb\x9bi k\xe1\xba\xbft qu\xe1\xba\xa3 n\xc3\xa0y kh\xc3\xb4ng?")\r\n    return answer\r\n\r\n#status 3: t\xc3\xacm t\xe1\xbb\xab th\xc3\xb4ng qua ngh\xc4\xa9a c\xe1\xbb\xa7a t\xe1\xbb\xab\r\nasync def find_by_meaning(meaning):\r\n    if len(await word_get_from_API(meaning))>=5:\r\n        response =  [f"{_[0]} : {_[1]}" for _ in (await word_get_from_API(meaning))[0:5]]\r\n        response.append("N\xe1\xba\xbfu t\xe1\xbb\xab b\xe1\xba\xa1n c\xe1\xba\xa7n t\xc3\xacm ki\xe1\xba\xbfm kh\xc3\xb4ng c\xc3\xb3 trong n\xc3\xa0y th\xc3\xac h\xc3\xa3y c\xe1\xbb\x91 g\xe1\xba\xafng nh\xe1\xba\xadp chi ti\xe1\xba\xbft h\xc6\xa1n nh\xc3\xa9!")\r\n        return response\r\n    elif len(await word_get_from_API(meaning))<5 and len(await word_get_from_API(meaning))>0 :\r\n        response =  [f"{_[0]} : {_[1]}" for _ in (await word_get_from_API(meaning))[0:]]\r\n        response.append("N\xe1\xba\xbfu t\xe1\xbb\xab b\xe1\xba\xa1n c\xe1\xba\xa7n t\xc3\xacm ki\xe1\xba\xbfm kh\xc3\xb4ng c\xc3\xb3 trong n\xc3\xa0y th\xc3\xac h\xc3\xa3y c\xe1\xbb\x91 g\xe1\xba\xafng nh\xe1\xba\xadp chi ti\xe1\xba\xbft h\xc6\xa1n nh\xc3\xa9!")\r\n        return response\r\n    elif len(await word_get_from_API(meaning))==0:\r\n        return "T\xe1\xbb\xab n\xc3\xa0y hi\xe1\xbb\x87n ch\xc6\xb0a c\xc3\xb3 trong t\xe1\xbb\xab \xc4\x91i\xe1\xbb\x83n. N\xe1\xba\xbfu b\xe1\xba\xa1n mu\xe1\xbb\x91n th\xc3\xaam h\xc3\xa3y nh\xe1\xba\xa5n ph\xc3\xadm 3"\r\n    \r\n')
    from data_control import find_word, answer_1, answer_2, post_word_to_API, word_get_from_API, history_write, show_history, meaning_get_from_API
    import crossword
    from game import randomize, verify
    import asyncio
    from chat import greet_user, lookup_word_1, lookup_word_2, find_by_meaning
    
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
    point = 0
    history = []
    questions = 0
    topic = ""
    played = []
    
    async def output(message):
        global status, count, satisfaction, no_count, word_asked, tu, res, finding, history, ans, answer_map, meaning_asked, nghia, point, questions, topic, played
        accept = ["ok","có","được","đồng ý","yes"]
        deny = ["ko","không","no","từ chối"]
        look_up_cases = ["tim tu", "tìm từ", "tìm kiếm","1"]
        game_cases = ["choi", "chơi", "2", "game"]
        add_cases = ["thêm", "3"]
        meaning_cases = ["nghĩa", "4"]
        history_cases = ["lịch sử", "5"]
        stop = ["quit", "thoát", "out", "rời", "back", "dừng", "ngừng"]
        topics = ["y học","công nghệ thông tin","giáo dục","lịch sử","sinh học","vật lý","gia dụng","ẩm thực","công sở","xây dựng","nghệ thuật", "thể thao","màu sắc","động vật","đại dương","tiền sử","phương tiện giao thông","cơ thể"]
        mapping = {"1": "y học", "2":"công nghệ thông tin", "3":"giáo dục","4":"lịch sử","5":"sinh học","6":"vật lý","7":"gia dụng","8":"ẩm thực","9":"công sở","10":"xây dựng","11":"nghệ thuật","12":"thể thao","13":"màu sắc","14":"động vật","15":"đại dương","16":"tiền sử","17":"phương tiện giao thông","18":"cơ thể"}
        menu = ["1. Tìm nghĩa của từ cho trước", "2. Chơi trò chơi để học từ mới", "3. Đóng góp thêm vào từ điển hiện tại", "4. Tìm từ qua nghĩa của từ", "5. Xem lịch sử tìm kiếm"]
        if ("option" in message.lower()) or ("menu" in message.lower()):
            return menu 
        if any(case in message.lower() for case in stop):
            status = "greeting"
            return "Cảm ơn bạn thân mến đã sử dụng Lingo Dictionary. Xin chào và hẹn gặp lại nha!"
        if status=="greeting":
            status = "option"
            return await greet_user(message)
        elif status=="option":
            if any(case in message.lower() for case in look_up_cases):
                status = "look up word"
                return "Mời nhập từ bạn cần tìm"
            elif any(case in message.lower() for case in game_cases):
                status = "topic"
                response = []
                response.append("Luật chơi: Bạn được phép chọn chủ đề mà bạn muốn chơi để học từ. Trò chơi sẽ gồm 10 câu hỏi trắc nghiệm với những từ ngữ xoay quanh chủ đề đó, mỗi câu hỏi sẽ có 4 phương án để lựa chọn.")
                response.append("Mời bạn chọn một trong những chủ đề sau:")
                for i in range (len(topics)):
                    response.append("{0}. {1}".format(i+1, topics[i]))
                response.append("Nếu muốn kết thúc trò chơi, hãy nhấn EXIT")
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
            elif any(case in message.lower() for case in add_cases):
                status = "add word"
                return "Nhập từ bạn muốn thêm"
            elif any(case in message.lower() for case in meaning_cases):
                status = "find meaning"
                return "Hãy nhập nghĩa của từ mà bạn muốn tìm"
            elif any(case in message.lower() for case in history_cases):
                if len(history)==0:
                    return "Hiện chưa có gì ở trong lịch sử cả. Hãy bắt đầu tìm kiếm ngay nhé!"
                else:
                    return show_history(history)
            else:
                return "Mời bạn nhập lại lệnh"
        elif status == "topic":
            status = "generate"
            topic = message
            return "Chọn chủ đề thành công! Hãy nhấn ENTER để bắt đầu ngay thôi!"
        elif status == "generate":
            if questions<10:
                status = "guess"
                response = []
                random = await randomize(mapping[str(topic)])
                while random[1] in played:
                    random = await randomize(mapping[str(topic)])
                played.append(random[1])
                words = random[0]
                ans = random[1]
                response.append("Câu {0}:Từ nào mang ý nghĩa sau: {1}".format(questions+1,(await meaning_get_from_API(ans))[1]))
                for i in range (len(words)):
                    response.append("{0}. {1}".format(chr(65+i),words[i]))
                    answer_map[chr(65+i)]=words[i]
                return response
            else:
                status = "option"
                result = point
                point = 0
                questions = 0
                played = []
                return f"Chúc mừng bạn đã hoàn thành trò chơi với {result}/10 câu chính xác. Hãy chọn chức năng để tiếp tục (nhập MENU để xem chi tiết)"
        elif status == "guess":
            status = "generate"
            if message.lower() == "exit":
                status = "option"
                result = point
                point = 0
                current = questions
                questions = 0
                return f"Trò chơi kết thúc. Bạn đạt được {result}/{current} câu trả lời chính xác. Hãy chọn chức năng để tiếp tục (nhập MENU để xem chi tiết)"
            if message not in list(answer_map.keys()) and message.upper() not in list(answer_map.keys()):
                status = "guess"
                return "Vui lòng chọn đáp án hợp lệ (A-D)"
            else:
                if verify(answer_map[message.upper()], ans):
                    point+=1
                    ans = ""
                    questions+=1
                    return "Câu trả lời rất chính xác. Nhấn ENTER để tiếp tục"
                else:
                    questions+=1
                    return f"Tiếc quá sai mất rồi. {ans} mới là câu trả lời chính xác. Nhấn ENTER để tiếp tục"
        elif status == "find meaning":
            status = "option"
            history_write(history, message)
            try:
                return await find_by_meaning(message)
            except:
                return "Lỗi nhập từ hoặc từ này chưa có trong từ điển. Hãy chọn lại lệnh để tiếp tục (nhập MENU để xem chi tiết)"
        elif status == "look up word":
            if message.isalpha() == False and message!="":
                return "Hãy nhập lại chính xác từ cần tìm kiếm"
            status = "satisfaction_judge"
            if satisfaction == True:
                finding = message
                history_write(history, message)
                return await lookup_word_1(message)
            else:
                satisfaction=True
                answer = await lookup_word_2(finding)
                finding = ""
                return answer
        elif status=="satisfaction_judge":
            if any(case in message.lower() for case in accept):
                status = "option"
                if no_count>0:
                    no_count-=1
                # return chat.back_to_option
                return "Cảm ơn đánh giá của bạn yêu! Hãy chọn tính năng để tiếp tục (nhập MENU để xem chi tiết)"
            elif any(case in message.lower() for case in deny):
                if no_count<1:
                    satisfaction = False
                    no_count+=1
                    status = "look up word"
                    return "Nhấn ENTER để bắt đầu tìm kiếm tiếp"
                else:
                    no_count = 0
                    status = "add word pending"
                    return "Rất tiếc, từ khoá này hiện chưa có trong từ điển. Lingo Dictionary sẽ cập nhật trong thời gian sớm nhất bạn yêu nhé! Bạn có muốn đề xuất từ mới nào ngay tại đây ko?"
            else:
                return "Hãy trả lời có hoặc không để chúng tôi biết nhé!"
        elif status == "add word pending":
            if any(case in message.lower() for case in accept):
                status = "add word"
                return "Vui lòng nhập từ bạn muốn thêm"
            elif any(case in message.lower() for case in deny):
                status = "option"
                return "Vậy thì hãy nhập lại lệnh để tiếp tục (nhập MENU để xem chi tiết)"
            else:
                return "Hãy trả lời có hoặc không để chúng tôi biết nhé!"
        elif status == "add word":
            if word_asked == False and meaning_asked == False:
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
        else:
            return "Sai cú pháp. Vui lòng nhập lệnh hợp lệ (nhập MENU để xem chi tiết)"
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
        # elif status == "crossword"
    # while True:
    #     message = input()
    #     print(output(message))