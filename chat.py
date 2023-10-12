# Chị nguyệt làm chỗ này
from data_control import answer_1, answer_2, word_get_from_API
import urllib.parse

#status 1: tính năng chào hỏi
async def greet_user(name):
    response = []
    response.append(f"Xin chào {name}. Mời bạn lựa chọn một trong những chức năng dưới đây:")
    response.append("1. Tìm nghĩa của từ cho trước")
    response.append("2. Chơi trò chơi để học từ mới")
    response.append("3. Đóng góp thêm vào từ điển hiện tại")
    response.append("4. Tìm từ qua nghĩa của từ")
    response.append("5. Xem lịch sử tìm kiếm")
    response.append("Nhấn QUIT để rời khỏi chương trình")
    return response

#status 2: tính năng tra từ
#2.1 Tra lần đầu tiên
async def lookup_word_1(keyword):
    word_list = await answer_1(keyword)
    answer = ["Những từ bạn cần tìm như sau: \n"]
    for word in word_list:
        answer.append("{0} : {1}\n".format(urllib.parse.unquote(word[0]), word[1]))
    answer.append("Bạn yêu có hài lòng với kết quả này không?")
    return answer

#2.2 Tra lần thứ 2 nếu chưa hài lòng
async def lookup_word_2(keyword):
    word_list = await answer_2(keyword)
    answer = ["Sau đây là kết quả tra cứu khác: "]
    for word in word_list:
        answer.append("{0} : {1}\n".format(urllib.parse.unquote(word[0]), word[1]))
    answer.append("Bạn yêu có hài lòng với kết quả này không?")
    return answer

#status 3: tìm từ thông qua nghĩa của từ
async def find_by_meaning(meaning):
    if len(await word_get_from_API(meaning))>=5:
        response =  [f"{_[0]} : {_[1]}" for _ in (await word_get_from_API(meaning))[0:5]]
        response.append("Nếu từ bạn cần tìm kiếm không có trong này thì hãy cố gắng nhập chi tiết hơn nhé!")
        return response
    elif len(await word_get_from_API(meaning))<5 and len(await word_get_from_API(meaning))>0 :
        response =  [f"{_[0]} : {_[1]}" for _ in (await word_get_from_API(meaning))[0:]]
        response.append("Nếu từ bạn cần tìm kiếm không có trong này thì hãy cố gắng nhập chi tiết hơn nhé!")
        return response
    elif len(await word_get_from_API(meaning))==0:
        return "Từ này hiện chưa có trong từ điển. Nếu bạn muốn thêm hãy nhấn phím 3"
    
