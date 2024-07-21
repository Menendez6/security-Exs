import hashlib
import string

def generate_new(word,set_words):
    word_1 = word.title()
    if word_1 not in set_words:
        set_words.add(word_1)
        set_words = generate_new(word_1,set_words)
    if "i" in word:
        word_2 = word.replace("i","1")
        set_words.add(word_2)
        set_words = generate_new(word_2,set_words)
    if "e" in word:
        word_2 = word.replace("e",'3')
        set_words.add(word_2)
        set_words = generate_new(word_2,set_words)
    if 'o' in word:
        word_2 = word.replace("o","0")
        set_words.add(word_2)
        set_words = generate_new(word_2,set_words)
    return set_words

word = "windiw"
word = word.replace('i','1')
print(word)
with open("rockyou.txt","r", encoding="ISO-8859-1") as file:
    lista = file.read().splitlines()
    set_final = set()
    for element in lista:
        set_final.add(element)
        set_final = generate_new(element,set_final)
        