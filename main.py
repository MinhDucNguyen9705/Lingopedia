# Đức làm chỗ này

# import data_control
# import chat

# from data_control import tra_tu_khoa
from data_control import lay_tu

database = lay_tu()
def find_word(prefix):
    response = []
    prefix = prefix.lower()
    # Prefix = word
    for word in database:
        if prefix == word or prefix==word.lower():
            response.append(word)
    # Longest common prefix
    # string_list = []
    # current=0
    # while current<len(database):
    #     string = ""
    #     prefix_cursor = 0
    #     temp_prefix = prefix+"1"
    #     for i in range (0,len(database[word])):
    #         if database[word][i]==temp_prefix[prefix_cursor]:
    #             word_cursor = i
    #             while (database[word][word_cursor]==temp_prefix[prefix_cursor] or database[word][word_cursor]==chr(ord(temp_prefix[prefix_cursor])-32)) and word_cursor<len(database[word])-1 and prefix_cursor<len(temp_prefix)-1:
    #                 word_cursor+=1
    #                 prefix_cursor+=1
    #             string += database[word][i:word_cursor]
    #     string_list.append(string)

    # Prefix in word
    for word in database:
        if prefix[0]==word[0] and prefix in word and len(response)<5 and word not in response:
            response.append(word)
    for word in database:
        if prefix in word and len(response)<5 and word not in response:
            response.append(word)
    count_list = []
    # Number of characters in prefix in each word
    for word in database:
        word_char = list(word)
        characters = list(prefix)
        i = 0
        j = 0
        count = 0
        while i<len(word_char) and j<len(characters):
            if word_char[i] == characters[j] or word_char[i] == chr(ord(characters[j])-32):
                count+=1
                word_char.pop(i)
                characters.pop(j)
            else:
                i+=1
            if i==len(word_char) and j<len(characters):
                i=0
                j+=1
        count_list.append(count)
    min_count = min(count_list)
    max_count = max(count_list)
    # print(min_count, max_count)
    for i in range (max_count, min_count-1,-1):
        for j in range (0,len(count_list)):
            if count_list[j]==i and len(response)<5 and database[j] not in response:
                response.append(database[j])
    return response
# print(string_list)
# print(count_list)
history_list = []

def history(word):
    global history_list 
    history_list.append(word)
    return history_list

while True:
    prefix = input("Input a word or a prefix: ")
    print(find_word(prefix))    
    print(history(prefix))
    

