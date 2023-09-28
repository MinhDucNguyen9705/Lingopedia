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

from data_control import find_word
import crossword

status = "greeting"
count = 0
# option = ""
def output(message):
    global status, count
    if status=="greeting":
        status = "option"
        return "Xin chao. Moi ban lua chon chuc nang tim tu hoac crossword"
    elif status=="option":
        if message=="1":
            status = "look up word"
            return "Moi nhap tu can tim"
        elif message=="2":
            status = "crossword_step1"
            return "Tro choi bat dau ... "
        else:
            return "Moi ban nhap lai lenh"
    elif status=="look up word":
        status = "satisfaction_judge"
        # word_list = [ ]
        # return chat.word_found(word_list)
        return "Nhung tu ban can tim nhu sau: ... Ban co hai long voi ket qua ko?"
    elif status=="satisfaction_judge":
        if message == "Yes":
            status = "option"
            # return chat.back_to_option
            return "Moi ban chon giua tim tu hoac crossword"
        elif message == "No":
            status = "look up word"
            return "Day la tin nhan khi ma chua thoa man"
    elif status == "crossword_step1":
        crossword.create_table()
        status = "crossword_step2"
        res = crossword.hint_lookup()
        traloi = []
        table = crossword.table_lookup()
        for line in res:
            traloi.append(line+"\n")
        for row in table:
            traloi.append(row+"\n")
        return traloi
    elif status == "crossword_step2":
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
            return "Ban da thang, tro choi ket thuc"

    
    
    # elif status == "crossword":

