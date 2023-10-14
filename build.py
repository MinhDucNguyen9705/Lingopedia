from xclass_sdk.chat_bot_app import ChatBotApp

app = ChatBotApp("tomQ1oEpZv")
# app = ChatBotApp("45d799cfb6")
app.name = "Lingopedia"
app.author = "Lingopedia Team"
app.slug = "dictionary"
app.description = "Rất vui vì được gặp bạn. Bạn có thể cho chúng tôi biết tên của bạn được không?"
app.greetingMessage = "Đây là một chương trình do Lingopedia tạo ra để phục vụ nhu cầu tra cứu từ của người dùng."
app.appLogo = "https://scontent.fhan5-9.fna.fbcdn.net/v/t1.15752-9/385419569_626401129566711_7154167082755885902_n.png?_nc_cat=109&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=JldnBaJgnHEAX8pG_5Y&_nc_ht=scontent.fhan5-9.fna&oh=03_AdQPY8z2M69axmIImHqiObjMGP5DO4Fe2R4LzzqJIvpEug&oe=65520E7E"

app.build("output.py")