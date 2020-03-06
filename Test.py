import pymorphy2
from tkinter import *

morph = pymorphy2.MorphAnalyzer()


def vocabulary(word):
    vocab = {
        "NOUN": "существительное",
        "VERB": "глагол",
        "ADJF": "имя прилагательное(полное)",
        "ADJS": "имя прилагательное(краткое)",
        "INFN": "глагол(личная форма)",
        "PRTF": "причастие(полное)",
        "PRTS": "причастие(краткое)",
        "GRND": "деепричастие",
        "NUMR": "числительное",
        "ADVB": "наречие",
        "NPRO": "местоимение",
        "PREP": "предлог",
        "CONJ": "союз",
        "PRCL": "частица",
        "INTJ": "междометие",

        "anim": "одушевленное",
        "inan": "неодушевленное",

        "masc": "мужской род",
        "femn": "женский род",
        "neut": "средний род",
        "ms-f": "общий род",

        "sing": "единственное число",
        "plur": "множественное число",

        "nomn": "именительный падеж",
        "gent": "родительный падеж",
        "datv": "дательный падеж",
        "accs": "винительный падеж",
        "ablt": "творительный падеж",
        "loct": "преддложный падеж",

        "Name": "имя",
        "Surn": "фамилия",
        "Patr": "отчество",

        "perf": "совершенный вид",
        "impf": "несовершенный вид",

        "tran": "переходный",
        "intr": "непереходный",

        "1per": "1 лицо",
        "2per": "2 лицо",
        "3per": "3 лицо",

        "pres": "настоящее время",
        "past": "прошедшее время",
        "futr": "будущее время",

        "indc": "изъявительное наклонение",
        "impr": "повелительное наклонение",

        "actv": "действительный залог",
        "pssv": "страдательный залог"
    }
    return vocab.get(word, lambda: "Invalid month")


class WordInfo:
    def __init__(self, word, userInfo, properties):
        self.word = word
        self.userInfo = userInfo
        self.properties = properties


def constructBasicInfo(parseWord):
    properties = set()
    userInfo = set()
    for gramma in morph.parse(parseWord)[0][1].grammemes:
        properties.add(gramma)
        userInfo.add(vocabulary(gramma))
    word_info = WordInfo(parseWord, userInfo, properties)
    return word_info


def defineRules(properties: set):
    rules = {
        "Подлежащее": [{"NOUN", "nomn"}, {"NPRO", "nomn"}],
        "Сказуемое": [{"VERB"}, {"INFN"}, {"ADJS"}],
        "Дополнение": [{"NOUN", "gent"}, {"NOUN", "datv"}, {"NOUN", "accs"}, {"NOUN", "ablt"}, {"NOUN", "loct"},
                       {"NPRO", "gent"}, {"NPRO", "datv"}, {"NPRO", "accs"}, {"NPRO", "ablt"}, {"NPRO", "loct"},
                       {"NUMR"}],
        "Определение": [{"ADJF"}, {"ADJS"}, {"NPRO"}, {"NUMR"}, {"PRTF"}, {"PRTS"}],
        "Обстоятельство": [{"ADVB"}, {"NOUN"}]
    }
    result = "Возможные члены предложения:"
    for key, value in rules.items():
        for gramma_rule in value:
            if gramma_rule.issubset(properties):
                result = result + key + ","
    return result


window = Tk()
window.title("Welcome to LikeGeeks app")
window.geometry('650x500')
txt = Entry(window, width=60)
txt.grid(column=1, row=0)
resultTxt = Entry(window, width=50)


def listToString(s):
    str1 = " "
    return str1.join(s)


def clicked():
    text = txt.get()
    result = list()
    for word in text.split():
        info = constructBasicInfo(word)
        roles = defineRules(info.properties)
        word_info: set = info.userInfo
        word_info.add(roles)
        result.append([word, word_info])
    result.sort()
    count = 3
    for word in result:
        listResult = listToString(word[1])
        str = "Слово \"" + word[0] + "\":  " + listResult
        newTxt = Entry(window, width=100)
        newTxt.grid(column=0, row=count)
        count += 1
        newTxt.delete(0, END)
        newTxt.insert(0, str)


btn = Button(window, text="Разобрать предложение", command=clicked)
btn.grid(column=2, row=0)
window.mainloop()


