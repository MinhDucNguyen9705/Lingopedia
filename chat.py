# Chị nguyệt làm chỗ này

#status 1: tính năng chào hỏi
def greet_user():
    return "Chào mừng bạn thân mến đến với Chatbot Từ điển Lingo Dictionary!"

#status 2: option
def option():
    return "Bạn thân mến muốn TRA TỪ hay CHƠI CROSSWORD?"
    # Lựa chọn tính năng thành công
    return "Bạn thân mến đã lựa chọn tính tăng {user option} thành công!"

#status 3: tính năng tra từ
def lookup_word(keyword: str):
    return "Mời bạn thân mến NHẬP TỪ KHOÁ muốn tra cứu: "
    # Từ khoá có sẵn
        return "Kết quả tra cứu : [...] "
            # Satisfaction Review (Có phần này không í nhỉ)
                return "Bạn yêu có hài lòng với kết quả này không? "
                    # Hài lòng
                    return "Cảm ơn đánh giá của bạn yêu!"
                    # Không hài lòng
                    return "Sau đây là kết quả tra cứu khác: [...]"
    # Từ khoá không có sẵn
        return "Rất tiếc, từ khoá này hiện chưa có trong từ điển. Lingo Dictionary sẽ cập nhật trong thời gian sớm nhất bạn yêu nhé!"

#status 4: Crossword
def play_crossword():
    # Hiện gợi ý 
    return "Bạn thân mến, dưới đây là GỢI Ý CROSSWORD của bạn: [..]"
    # Mời user đoán
    return "Mời bạn yêu đoán CROSSWORD"
    # Đáp án chính xác nhưng chưa kết thúc
    return "Đáp án CHÍNH XÁC! Mời bạn yêu đoán ô chữ tiếp theo: "
    # Đáp án chính xác và kết thúc
    return "Tuyệt cà là vời, đáp án CHÍNH XÁC! Chúc mừng bạn yêu đã HOÀN THÀNH CROSSWORD"
    # Đáp án sai
    return "Rất tiếc bạn yêu à, đáp án CHƯA CHÍNH XÁC! Mời bạn đoán lại nha: "

#status 5: Pending selection
def pending_selection():
    return "Bạn đã hoàn thành TRA TỪ/ CHƠI CROSSWORD. Bạn thân mến có muốn TIẾP TỤC không?"
    # Tiếp tục --> Về status 2
    # Không tiếp tục
    return "Cảm ơn bạn thân mến đã sử dụng Lingo Dictionary. Xin chào và hẹn gặp lại nha!"
# import main