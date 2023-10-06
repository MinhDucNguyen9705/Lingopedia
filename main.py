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
        if word_asked == False:
            tu = ""
            tu = message
            word_asked=True
            return "Mời bạn nhập nghĩa"
        else:
            word_asked=False
            status = "option"
            return await post_word_to_API(tu, message)
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