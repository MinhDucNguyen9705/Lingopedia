# Đức làm chỗ này

# import data_control
# import chat

# from data_control import tra_tu_khoa
# print(string_list)
# print(count_list)
# history_list = []

# def history(word):
#     global history_list 
#     history_list.append(word)
#     return history_list

# while True:
# prefix = input("Input a word or a prefix: ")
# word_found = (find_word(prefix))
# for word in word_found:
#     res = tra_tu_khoa(word,"tu")
#     string = f"{res[0][0]} : {res[0][1]}"
#     print(string)

# print(history(prefix))

from data_control import find_word, answer_1, answer_2, post_word_to_API, word_get_from_API, history_write, show_history, meaning_get_from_API
import crossword
from game import randomize, verify
import asyncio

status = "greeting"
count = 0
satisfaction = True
no_count = 0
word_asked = False
tu = ""
res = ""
finding = ""
ans = ""
answer_map = {"A": "", "B":"","C": "", "D":""}
# option = ""
history = []
async def output(message):
    global status, count, satisfaction, no_count, word_asked, tu, res, finding, history, ans, answer_map
    accept = ["ok","có","được","đồng ý","yes"]
    deny = ["ko","không","no","từ chối"]
    look_up_cases = ["tim tu", "tìm từ", "tìm kiếm", "tìm từ","1"]
    topics = ["y học","công nghệ thông tin","giáo dục","lịch sử","sinh học","vật lý","gia dụng","ẩm thực","công sở","xây dựng","nghệ thuật", "thể thao","màu sắc","động vật","đại dương","tiền sử","phương tiện giao thông","cơ thể"]
    mapping = {"1": "y học", "2":"công nghệ thông tin", "3":"giáo dục","4":"lịch sử","5":"sinh học","6":"vật lý","7":"gia dụng","8":"ẩm thực","9":"công sở","10":"xây dựng","11":"nghệ thuật","12":"thể thao","13":"màu sắc","14":"động vật","15":"đại dương","16":"tiền sử","17":"phương tiện giao thông","18":"cơ thể"}
    if message.lower() == "quit":
        status = "greeting"
        return "Xin chao va hen gap lai"
    if status=="greeting":
        status = "option"
        response = []
        response.append(f"Xin chao {message}. Moi ban lua chon mot trong nhung chuc nang sau:")
        response.append("1. Tim nghia cua tu cho truoc")
        response.append("2. Choi tro choi de hoc tu moi")
        response.append("3. Dong gop them tu moi vao tu dien hien tai")
        response.append("4. Tim tu qua nghia cua tu")
        response.append("5. Xem lich su tim kiem")
        return response
    elif status=="option":
        if message in look_up_cases:
            status = "look up word"
            return "Moi nhap tu can tim"
        elif message=="2":
            status = "topic"
            response = []
            response.append("Moi ban chon mot trong nhung chu de sau:")
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
            return "Nhap tu ban muon them"
        elif message == "4":
            status = "find meaning"
            return "Hay nhap nghia cua tu ma ban muon tim"
        elif message == "5":
            if len(history)==0:
                return "Hien chua co gi o trong lich su ca. Hay bat dau tim kiem ngay nhe!"
            else:
                return show_history(history)
        else:
            return "Moi ban nhap lai lenh"
    elif status == "topic":
        status = "guess"
        response = []
        random = await randomize(mapping[str(message)])
        words = random[0]
        ans = random[1]
        print(words)
        print(ans)
        response.append("Tu nao mang y nghia sau: {0}".format((await meaning_get_from_API(ans))[1]))
        for i in range (len(words)):
            response.append("{0}. {1}".format(chr(65+i),words[i]))
            answer_map[chr(65+i)]=words[i]
        return response
    elif status == "guess":
        if verify(answer_map[message], ans):
            status = "option"
            ans = ""
            return "Ban da tra loi dung. Moi chon tinh nang de tiep tuc"
        else:
            return "Sai roi, moi ban doan lai"
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
                return "Tu nay hien chua co trong tu dien"
        except OSError:
            return "Loi nhap tu hoac tu nay chua co trong tu dien. Hay chon lai lenh de tiep tuc"
    elif status == "look up word":
        status = "satisfaction_judge"
        if satisfaction == True:
            finding = message
            history_write(history, message)
            word_list = await answer_1(message)
            answer = ["Nhung tu ban can tim nhu sau: \n"]
            for word in word_list:
                answer.append("{0} : {1}\n".format(word[0].replace("%20"," "), word[1]))
            answer.append("Ban co hai long voi ket qua ko? ")
            return answer
        else:
            satisfaction=True
            word_list = await answer_2(finding)
            finding = ""
            answer = ["5 tu gan nhat duoc tim thay: "]
            for word in word_list:
                answer.append("{0} : {1}\n".format(word[0].replace("%20"," "), word[1]))
            answer.append("Tu ban tim kiem co trong nay ko? ")
            return answer
    elif status=="satisfaction_judge":
        if message.lower() in accept:
            status = "option"
            if no_count>0:
                no_count-=1
            # return chat.back_to_option
            return "Moi ban chon giua tim tu hoac crossword"
        elif message.lower() in deny:
            if no_count<1:
                satisfaction = False
                no_count+=1
                status = "look up word"
                return "Nhan ENTER de bat dau tim kiem lai"
            else:
                no_count = 0
                status = "add word pending"
                return "Co the tu nay chua co trong tu dien cua chung toi, ban co the giup chung toi them no vao ko?"
        else:
            return "Hay tra loi co hoac khong de chung toi biet nhe!"
    elif status == "add word pending":
        if message.lower() in accept:
            status = "add word"
            return "Vui long nhap tu ban muon them"
        elif message.lower() in deny:
            status = "option"
            return "Vay thi ban hay vui long nhap lai lenh de tiep tuc (1 - 3)"
    elif status == "add word":
        if word_asked == False:
            tu = ""
            tu = message
            word_asked=True
            return "Moi ban nhap nghia"
        else:
            word_asked=False
            status = "option"
            return await post_word_to_API(tu, message)
    elif status == "crossword":
        if count<len(res):
            if crossword.guess(message)!=False:
                count+=1
                response = []
                response.append(f"Ban da tra loi dung, con lai {len(res)-count} tu \n")
                current = crossword.guess(message)
                for line in current:
                    response.append(" ".join(line) + "\n")
                return response
            else:
                return "Moi ban doan lai"
        else:
            status = "option"
            count = 0
            crossword.clear_history()
            return "Ban da thang, tro choi ket thuc. Hay chon lai tinh nang de tiep tuc"
    else:
        return "Sai cu phap. Vui long nhap lenh hop le"
    # elif status == "crossword"
# while True:
#     message = input()
#     print(output(message))