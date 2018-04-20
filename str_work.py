# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:34:45 2018

@author: edino
"""

asciiChgDict = {"А":"A",   "Б":"B", "В":"V",  "Г":"G",  "Д":"D",  "Е":"E", 
                "Ж":"ZH",  "З":"Z", "И":"I",  "К":"K",  "Л":"L",  "М":"M",
                "Н":"N",   "О":"O", "П":"P",  "Р":"R",  "С":"S",  "Т":"T",
                "У":"U",   "Ф":"F", "Х":"KH", "Ц":"C",  "Ч":"CH", "Ш":"SH",
                "Щ":"SCH", "Э":"E", "Ю":"YU", "Я":"YA", "1":"1",  "2":"2",
                "3":"3",   "4":"4", "5":"5",  "6":"6",  "7":"7",  "8":"8",
                "9":"9",   "_":"_", "A":"A",  "B":"B",  "C":"C",  "D":"D",
                "E":"E",   "F":"F", "G":"G",  "H":"H",  "I":"I",  "J":"J",
                "K":"K",   "L":"L", "M":"M",  "N":"N",  "O":"O",  "P":"P",
                "Q":"Q",   "R":"R", "S":"S",  "T":"T",  "U":"U",  "V":"V",
                "W":"W",   "X":"X", "Y":"Y",  "Z":"Z",  "-":"_",  "0":"0"}

def eqStr(s1, s2, mode = "begin"):
    if mode == "begin":
        s1 = " " * (len(s2) - len(s1)) + s1
        s2 = " " * (len(s1) - len(s2)) + s2
    else:
        s1 += " " * (len(s2) - len(s1))
        s2 += " " * (len(s1) - len(s2))
    return s1, s2

def getParamList(s):
    sNew = []
    cont = 0
    for i in range(len(s)):
        if cont > 0:
            cont -= 1
            continue
        sNew.append(s[i])
        if sNew[-1].find("'") != -1 and sNew[-1][sNew[-1].find("'") + 1:].find("'") == -1:
            while sNew[-1].find("'") != -1 and sNew[-1][sNew[-1].find("'") + 1:].find("'") == -1:
                i += 1
                sNew[-1] += "," + s[i]
                cont += 1
        if sNew[-1].find("'") == -1:
            sNew[-1] = sNew[-1].replace(" ", "")
        else:
            index1 = sNew[-1].find("'")
            index2 = sNew[-1][index1 + 1:].find("'") + index1
            sNew[-1] = sNew[-1][:index1].replace(" ", "") + sNew[-1][index1:index2] + sNew[-1][index2:].replace(" ", "")
    print(sNew)
    return sNew

def get_quote(s, begin = "'", displb = 1, end = "'", disple = 0):
    """
    s - str
    begin, end - char or str
    displb, disple - int
    returns part of s from index of begin + displb to index of end + disple
    by default begin = "'", end = "'", displb = 1, disple = 0
    if begin = "" starts from displb, if end = "" finishes at disple
    """
    if begin == "":
        i = displb
    else:
        i = s.lower().index(begin) + displb
    ret = s[i:]
    if end == "":
        i = len(ret) + disple
    else:
        i = ret.lower().index(end) + disple
    ret = ret[:i]
    return ret

def getQuote(s, begin = "'", displb = 1, end = "'", disple = 0):
    """
    s - str
    begin, end - char or str
    displb, disple - int
    returns part of s from index of begin + displb to index of end + disple
    by default begin = "'", end = "'", displb = 1, disple = 0
    if begin = "" starts from displb, if end = "" finishes at disple
    """
    if begin == "":
        i = displb
    else:
        i = s.lower().index(begin) + displb
    ret = s[i:]
    if end == "":
        i = len(ret) + disple
    else:
        i = ret.lower().index(end) + disple
    ret = ret[:i]
    return ret

def get_text_part(pText, delim, log = 0, delim2 = ""):
    """
    pText - list of str
    delim - str
    delim2 - str, optional (if "" equals to delim)
    log - file to save log
    get part of pText between delims,
    if delim not found prints error message in file and returns all text
    """
    i = -1
    f = False
    partText = []
    while True:
        i += 1
        if i >= len(pText):
            if log != 0:
                if f:
                    log.write(delim + " end not found\n")
                else:
                    log.write(delim + " not found\n")
            break
        s = pText[i].lower()
        if delim == "//<head>":
            s = s.replace("а", "a")
        if not f:
            if s.find(delim) == -1:
                continue
            else:
                f = True
                if delim2 != "":
                    delim = delim2
                continue
        if s.find(delim) != -1:
#            print(delim)
            break
        partText.append(pText[i])
    if partText == []:
        return pText[:]
    return partText

def convert_to_eng(s):
    """
    s - string of asciichar
    returns string transcribed into english
    """
    ret = ""
    for ch in s:
        ret += asciiChgDict.get(ch, "")
    return ret