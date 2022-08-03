import re
import json

#BASES DE COMPARAÇÃO
conj = ["nem", "contudo", "entretanto", "mas", "no entanto", "porém",
"todavia", "já", "ou", "ora", "quer", "assim", "então", "logo", "pois",
"por isso", "portanto", "porquanto", "porque", "que"]

prep = ["a", "ante", "após", "até", "com", "contra", "de", "desde", "em", "entre", "para", "per",
"perante", "por", "sem", "sob", "sobre", "trás"]

pont = ['\"', '\'', '!', '?', '!?', ',', ';', ':', '.', '-', '(', ')', "..."]

#OBJETOS
class Word:
    def __init__(self, content, start_time, end_time, type):
        self.content = content
        self.start_time = start_time
        self.end_time = end_time
        self.type = type
        self.size = len(content)

class Caption:
    def __init__(self, content, start_time, end_time):
        self.content = content
        self.start_time = start_time
        self.end_time = end_time

def jsonToWords(file):

    text = []

    for i in range(len(file["results"]["items"])):

        content = file["results"]["items"][i]["alternatives"][0]["content"]
        tipe = file["results"]["items"][i]['type']

        if tipe == "pronunciation":
            start_time = float(file["results"]["items"][i]["start_time"])
            end_time = float(file["results"]["items"][i]["end_time"])

        else:
            start_time = end_time

        text.append(Word(content, start_time, end_time, tipe))

    return text

#Verifica quais as palavras e se é possível separar em alguma conjunção ou preposição
#Return 0 - Normal Word
#Return 1 - Break Word
def BreakWord(s):

    word = re.sub('[^A-Za-z0-9]+', '', s)

    if word in conj:
        return 1

    else:
        return 0

#Transformar lista de palavras em string
def toString(sentence):

    i = 0
    toString = []

    while sentence[i] != '':

        if sentence[i] in pont:
            toString[i - 1] = toString[i - 1] + sentence[i]
            print("toString[i - 1]")
            i += 1
            continue

        toString.append(sentence[i])

        if (i + 1 == 41) or (i + 1 == len(sentence)):
            break
        else:
            i += 1

    return ' '.join(toString)

#Limpar lista que forma string
def Reset(sentence):

    for j in range(41):
        sentence[j] = ''

    sentence[41] = 0

#CÓDIGO PRINCIPAL
def CaptionsSplitter(fileName):

    #Lista com objetos Caption
    caption = []

    #Lista que forma a strings
    #posição 41 soma a quantidade de caracteres
    sentence = ['' for x in range(42)]
    Reset(sentence)

    #Lista com as palavras
    file = jsonToWords(fileName)

    i = 0
    start_time = 0.0

    for j in range(len(file)):

        if sentence[0] == "":
            start_time = file[j].start_time

        if (file[j].type == "punctuation" and not (file[j].content == "," and sentence[1] == "")) or ((j < (len(file) - 1)) and (float(file[j+1].start_time) - float(file[j].end_time)) >= 1):

            content = toString(sentence) + file[j].content
            end_time = file[j].end_time
            sentence[41] += file[j].size
            caption.append(Caption(content, start_time, end_time))
            Reset(sentence)
            i = 0
            continue

        elif BreakWord(file[j].content):

            if (sentence[0] == "") or (sentence[3] == ""):
                sentence[i] = file[j].content
                sentence[41] += file[j].size
                start_time = file[j].start_time
                i += 1
                continue

            content = toString(sentence)
            end_time = file[j-1].end_time
            caption.append(Caption(content, start_time, end_time))
            Reset(sentence)

            sentence[0] = file[j].content
            sentence[41] += file[j].size
            start_time = file[j].start_time
            i = 1
            continue

        if sentence[41] < 26:

            sentence[i] = file[j].content
            sentence[41] += file[j].size
            i += 1
            continue

        #O que fazer caso passe os 42 caracteres
        else:
             content = toString(sentence)
             end_time = file[j-1].end_time
             caption.append(Caption(content, start_time, end_time))
             Reset(sentence)

             sentence[0] = file[j].content
             sentence[41] += file[j].size
             start_time = file[j].start_time
             i = 1
             continue

    return caption
