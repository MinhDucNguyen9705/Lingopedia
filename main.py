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
            return "Cảm ơn đánh giá của bạn yêu! Hãy chọn tính năng để tiếp tục (1-5)"
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