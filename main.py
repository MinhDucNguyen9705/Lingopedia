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

from data_control import find_word_1, find_word_2, them_tu_khoa
import crossword


status = "greeting"
count = 0
satisfaction = True
no_count = 0
word_asked = False
meaning_asked = False
# option = ""
def output(message):
    global status, count, satisfaction, no_count, word_asked, meaning_asked
    if status=="greeting":
        status = "option"
        return f"Xin chao {message}. Moi ban lua chon chuc nang tim tu hoac crossword"
    elif status=="option":
        if message=="1":
            status = "look up word"
            return "Moi nhap tu can tim"
        elif message=="2":
            status = "crossword"
            crossword.create_table()
            # status = "crossword_step2"
            res = crossword.hint_lookup()
            traloi = []
            table = crossword.table_lookup()
            for line in res:
                traloi.append(line+"\n")
            for row in table:
                traloi.append(row+"\n")
            return traloi
            # return "Tro choi bat dau"
        else:
            return "Moi ban nhap lai lenh"
    elif status=="look up word":
        status = "satisfaction_judge"
        if satisfaction == True:
            word_list = find_word_1(message)
            answer = ["Nhung tu ban can tim nhu sau: \n"]
            for word in word_list:
                answer.append("{0} : {1}\n".format(word[0][0], word[0][1]))
            answer.append("Ban co hai long voi ket qua ko? ")
            return answer
        else:
            satisfaction=True
            word_list = find_word_2(message)
            answer = ["5 tu gan nhat duoc tim thay: "]
            for word in word_list:
                answer.append("{0} : {1}\n".format(word[0][0], word[0][1]))
            answer.append("Tu ban tim kiem co trong nay ko? ")
            return answer
    elif status=="satisfaction_judge":
        if message == "Yes":
            status = "option"
            if no_count>0:
                no_count-=1
            # return chat.back_to_option
            return "Moi ban chon giua tim tu hoac crossword"
        elif message == "No":
            if no_count<1:
                satisfaction = False
                no_count+=1
                status = "look up word"
                return "Hay nhap lai dung tu vua nay ban tim"
            else:
                no_count = 0
                status = "add word"
                return "Co the tu nay chua co trong tu dien cua chung toi, ban hay giup chung toi them no vao nhe. "
    elif status == "add word":
        if word_asked == False and meaning_asked==False:
            tu = message
            word_asked==True
            return "Moi ban nhap nghia"
        elif word_asked==True and meaning_asked==False:
            nghia = message
            return "Moi ban nhap loai tu"
        elif word_asked==True and meaning_asked==True:
            status = "option"
            word_asked=False
            meaning_asked=False
            return them_tu_khoa(tu, nghia, message)
    # elif status == "crossword_step1":
    #     crossword.create_table()
    #     status = "crossword_step2"
    #     res = crossword.hint_lookup()
    #     traloi = []
    #     table = crossword.table_lookup()
    #     for line in res:
    #         traloi.append(line+"\n")
    #     for row in table:
    #         traloi.append(row+"\n")
    #     return traloi
    elif status == "crossword":
        if count<len(res):
            if crossword.guess(message)!=False:
                count+=1
                response = []
                response.append(f"Ban da tra loi dung, con lai {len(res)-count} tu \n")
                current = crossword.guess(message)
                for line in current:
                    response.append(line + "\n")
                return response
            else:
                return "Moi ban doan lai"
        else:
            status = "option"
            return "Ban da thang, tro choi ket thuc. Hay chon lai tinh nang de tiep tuc"
    
    
    # elif status == "crossword":

