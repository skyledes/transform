# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 10:58:04 2018

@author: edino
"""

from str_work import *

def clean_text(pText):
    temp = []
    i = -1
    while True:
        
        i += 1
        if i == len(pText):
            break
        
        s = pText[i]
        if s == "":
            continue
        s = s.replace(" ", "")
        s = s.replace("\t", "")
        if s == "":
            continue
        if s.lower().find("initialization.inc") != -1:
            temp.append("LoadFKFile(FileName,False);")
            temp.append("Time_to_FKRec(FileName,FileName);")
            temp.append("ActivateFileFK(FileName,True);")
            continue
        
        temp.append(pText[i].replace("\t", " "))
    
    return temp[:]    

def replace_funcs(pText, search, replace, log):
    n = 0
    for i in range(len(pText)):
        s = pText[i]
        s = s.lower()
        k = s.find(search)
        if k != -1:
            s = pText[i]
            pText[i] = s[:k] + replace + s[k + len(search):]
            n += 1
    log.write(str(n) + " " + search + " replaced by " + replace + "\n")
    return pText[:]
    
def replace_second_level(st):
    s = get_quote(st, "(", 1, ")", 0).replace(" ", "").split(",")
        
    ret = "ConfChnlN(" + s[0] + ", " + s[2] + ", "
    if s[1].lower() == "true":
        ret += "[SecondLevels]);"
    else:
        ret += "[]);"
            
    return ret

def replace_uo(st):
    st = get_quote(st, "(", 1, ")", 0)
    name = get_quote(st)
    s = st[:st.find(name) - 1]
    while s[-1] != ",":
        s = s[:-1]
    s = s[:-1]
    s += st[st.find(name) + len(name) + 1:]
    s = s.replace(" ", "").split(",")
    
    ret = "  WTFVar := UO("
    
    if len(s) == 15:
        if s[-1].lower() == "false" or s[-1].lower() == "true":
            s = s[:11] + s[12:-1]
            s.append("!0000")
    elif s[11] == "1" or s[11] == "0":
        r = s[11]
        s = s[:11] + s[12:]
        s.append("!000" + r)
    
    p = float(s[1]) / 2
    d1 = abs(float(s[8]) - p)
    d2 = abs(float(s[10]) - p)
    
    if d1 > d2:
        s = s[:8] + [s[10]] + s[8:10] + s[11:]
    
    for i in range(len(s) - 1):
        ret += s[i] + ", "
    
    ret += "'" + name + "', " + s[-1] + ");"
    
    return ret

def replace_ili(st):
    st = get_quote(st, "(", 1, ")", 0)
    name = get_quote(st)
    s = st[:st.find(name) - 1]
    while s[-1] != ",":
        s = s[:-1]
    s = s[:-1]
    s += st[st.find(name) + len(name) + 1:]
    s = s.replace(" ", "").split(",")
    ret = "  WTFVar := ILI("
    for i in range(len(s)):
        ret += s[i] + ", "
    ret += "'" + name + "', !0000);"
    return ret

def replace_ios(st):
    st = get_quote(st, "(", 1, ")", 0)
    name = get_quote(st)
    s = st[:st.find(name) - 1]
    while s[-1] != ",":
        s = s[:-1]
    s = s[:-1]
    s += st[st.find(name) + len(name) + 1:]
    s = s.replace(" ", "").split(",")
    ret = "  IOS("
    for i in range(len(s)):
        ret += s[i] + ", "
    ret += "'" + name + "');"
    return ret    

def replace_tp(st):
    st = get_quote(st, "(", 1, ")", 0)
    name = get_quote(st)
    s = st[:st.find(name) - 1]
    while s[-1] != ",":
        s = s[:-1]
    s = s[:-1]
    s += st[st.find(name) + len(name) + 1:]
    s = s.replace(" ", "").split(",")
    
    if len(s) == 15:
        s = s[:10] + s[11:]
        if s[-1].lower() == "sfp_":
            s[-1] = "true"
        else:
            s[-1] = "false"
    ret = "  TP("
    for i in range(len(s) - 1):
        ret += s[i] + ", "
    
    ret += "'" + name + "', " + s[-1] + ");"
    return ret    

def replace_updown(st):
    st = get_quote(st, "(", 1, ")", 0)
    s = st.replace(" ", "").split(",")
    if s[0].lower().find("board") == -1:
        s.insert(0, "BoardList")
    ret = "  UpDown("
    for i in range(len(s)):
        ret += s[i] + ", "
    ret = ret[:-2] + ");"
    return ret

def replace_smth(pText, log, search, func, message, debug = False):
    n = 0
    for i in range(len(pText)):
        s = pText[i].lower().replace(" ", "")
        k = s.find(search.lower().replace(" ", ""))
        if k == -1:
            continue
        n += 1
        if debug:
            print(pText[i])
            log.write(pText[i] + "\n")
        pText[i] = func(pText[i])
        if debug:
            log.write(pText[i] + "\n")
    
    log.write(str(n) + " " + search + "'s replaced by " + message + "\n")
    if debug:
        print(str(n) + " " + search + "'s replaced by " + message)
    return pText

def del_comments(pText, log):
    ret = []
    ret = get_text_part(pText, "(****", log, "****)")
    if len(ret) == len(pText):
        ret = []
    i = 0
    while True:
        if i >= len(pText):
            break
        s = pText[i]
        
        def find_first(s, chs):
            ch = ""
            ind = len(s)
            for c in chs:
                i = s.find(c)
                if i < ind and i != -1:
                    ind = i
                    ch = c
            if ind == len(s):
                ind = -1
            return ch, ind
        
        if s.replace(" ", "")[:3] != "//<":
            chs = ["//", "{", "(*"]
            while True:
                ch, ind = find_first(s, chs)
                if ind == -1:
                    break
                else:
                    if ch == "//":
                        s = s[:ind]
                        break
                    if ch == "(*":
                        r = s[:ind]
                        s = s[ind + 2:]
                        ind = s.find("*)")
                        while ind == -1:
                            i += 1
                            s = pText[i]
                            ind = s.find("*)")
                        s = r + s[ind + 2:]
                        continue
                    if ch == "{":
                        r = s[:ind]
                        s = s[ind + 1:]
                        ind = s.find("}")
                        while ind == -1:
                            i += 1
                            s = pText[i]
                            ind = s.find("}")
                        s = r + s[ind + 1:]
                        continue
            
            ts = s.replace(" ", "")
            
#            print(ts)
            if ts != "":
                ret.append(s)
        else:
            ret.append(s)
        i += 1
        continue
        
    return ret[:]

def find_var(text, i, searchS, strB = "'", strE = "'", disB = 1, disE = 0, errMes = "", replS = True, repeat = False, log = "log.txt", searchS2 = ""):
    while True:
        i += 1
        if i >= len(text):
            if errMes != "":
                log.write(errMes + "\n")
            i -= 1
            return "", i
        s = text[i].lower()
        if s.find(searchS) == -1:
            continue
        if searchS2 != "" and s.find(searchS2) == -1:
            continue
        if s.find(strB) == -1 or s.find(strE) == -1:
            continue
        s = get_quote(text[i], strB, disB, strE, disE)
        if repeat:
            s = get_quote(s, strB, disB, "", 0)
        if replS:
            s = s.replace(" ", "")
        return s, i
    
def templ_get_part(pText, f, partDel, delStr, searchStr, strB, strE, delB, delE, errMes, replS, repeat, multStr, multLine, multVar, delimList, varEnds, log, partDel2, searchStr2):
    for i in range(len(partDel)):
        if partDel[i] == "":
            currPart = pText
        else:
            currPart = get_text_part(pText, partDel[i], log, partDel2.get(i, ""))
            
        if delStr[i] != "":
            block = delStr[i]
            f.write(delStr[i])
        
        findF = False
        k = -1
        if multStr[i]:
            err = ""
        else:
            err = errMes[i]
        while True:
            
            if multLine[i]:
                s, k = find_var(currPart, k, searchStr[i], "", "", 0, 0, err, replS[i], False, log, searchStr2.get(i, ""))
                if s != "":
                    while s.find(varEnds[i]) == -1:
                        k += 1
                        if replS[i]:
                            s += currPart[k].replace(" ", "")
                        else:
                            s += currPart[k]
                    if not multVar[i]:
                        s = get_quote(s, strB[i], delB[i], strE[i], delE[i])
            else:
                s, k = find_var(currPart, k, searchStr[i], strB[i], strE[i], delB[i], delE[i], err, replS[i], repeat[i], log, searchStr2.get(i, ""))
            
            if s == "":
                if not findF:
                    f.write("\n")
                    if multStr[i]:
                        log.write(errMes[i] + "\n")
                break
            
            if multVar[i]:
                if s.find(delimList[i][0][0]) == -1 or s.find(delimList[i][0][2]) == -1 or s.find(delimList[i][1][0]) == -1 or s.find(delimList[i][1][2]) == -1:
                    continue
            
            findF = True
            if multVar[i]:
                s1 = get_quote(s, delimList[i][0][0], delimList[i][0][1], delimList[i][0][2], delimList[i][0][3]).replace(" ", "")
                s2 = get_quote(s, delimList[i][1][0], delimList[i][1][1], delimList[i][1][2], delimList[i][1][3])
                s = s1 + "€" + s2
            s = s.replace("\t", "")
            if s.replace(" ", "") != "":
                while s[0] == " ":
                    s = s[1:]
            f.write(s + "\n")
            
            
            if not multStr[i]:
                break
            
        if i == len(partDel) - 1 or delStr[i + 1] != "":
            f.write(block)

def insert_xml(pText, beg, end, delim, delimE = "", add = False):
    i = 0
    fB = False
    fE = False
    if delimE == "":
        delimE = delim
    while True:
        if i >= len(pText):
            print("No " + beg + " found")
            if add:
                pText.insert(0, delim)
                pText.insert(0, " ")
                pText.insert(0, delimE)
            break
        s = pText[i].lower()
        if s.find(beg) != -1:
            pText.insert(i, delim)
            i += 1
            fB = True
            break
        i += 1
    if fB:
        while True:
            if i >= len(pText):
                print("No " + end + " found")
                break
            s = pText[i].lower()
            if type(end) == str:
                if s.find(end) != -1:
                    pText.insert(i, delimE)
                    break
            else:
                for e in end:
                    if s.find(e) != -1:
                        pText.insert(i, delimE)
                        fE = True
                        break
            if fE:
                break
            i += 1
    log.write(delimE + " succesfully inserted\n")
    return pText[:]


def insert_xml2(pText, log, beg, end, disB = 0, disE = 1, delB = "", delE = "", add = False):
    i = 0
    fB = False
    fE = False
    while True:
        if i >= len(pText):
            print("No " + beg + " found")
            log.write("No " + beg + " found")
            if add:
                pText.insert(0, delB)
                pText.insert(0, " ")
                pText.insert(0, delE)
            break
        s = pText[i].lower()
        


#program name, creation date, designer, tu
partDel = ["", "", "", ""]
partDel2 = {}
for i in range(4):
    partDel2[i] = "program"
#adapter, ku, jumpers, last board
partDel += ["const", "const", "const", "const"]
for i in range(4, 8):
    partDel2[i] = "delta"
delStr = ["//<strconst>\n", "", "", "", "", "", "", ""]
searchStr = ["program ", "дата отладки", "автор", "набор тестов", "adap", "ku", "jamper", "pin2"]
searchStr2 = {}
strB = ["program", "отладки", ":", "для", "'", "'", "'", "'"]
strE = [";", "", "", "", "'", "'", "'", "'"]
delB = [7, 8, 1, 4, 1, 1, 1, 1]
delE = [0, 0, 0, 0, 0, 0, 0, 0]
errMes = ["No program name found", "No creation date found", "No designer name found"]
errMes += ["No TU found", "No adapter info found", "No contact device info found"]
errMes += ["No jumpers info found", "No last board info found"]
replS = [True, True, False, False, False, False, False, False]
repeat = [False, False, False, False, False, False, False, False]
multStr = [False, False, False, False, False, False, False, False]
multLine = [False, False, False, False, False, False, False, False]
multVar = [False, False, False, False, False, False, False, False]
delimList = {}
varEnds = {}

#fk names
partDel.append("const")
partDel2[len(partDel) - 1] = "adap"
delStr.append("//<filenames>\n")
searchStr.append("filename")
strB.append("")
strE.append("")
delB.append(0)
delE.append(0)
errMes.append("No FK names found")
replS.append(False)
repeat.append(False)
multStr.append(True)
multLine.append(False)
multVar.append(True)
delimList[len(partDel) - 1] = [["", 0, ":", 0], ["'", 1, "'", 0]]

#real consts
#number of IMS pins, source current, voltage meas time, current meas time, tins for time measurements
partDel += ["adap60", "namepin", "namepin", "namepin", "namepin"]
partDel2[9] = "inpins"
for i in range(10, 14):
    partDel2[i] = "initialization"
delStr += ["//<realvars>\n", "", "", "", "//<tins>\n"]
searchStr += ["numofpin", "ilimpwr", "timemeasu", "timemeasi", "tin"]
strB += ["=", "=", "=", "=", ""]
strE += [";", ";", ";", ";", ""]
delB += [1, 1, 1, 1, 0]
delE += [0, 0, 0, 0, 0]
errMes += ["No number of pins found", "No ilimpwr found", "No timemeasu found", "No timemeasi found", "No tins found"]
replS += [True, True, True, True, True]
repeat += [False, False, False, False, False]
multStr += [False, False, False, False, True]
multLine += [False, False, False, False, False]
multVar += [False, False, False, False, True]
delimList[len(partDel) - 1] = [["", 0, "=", 0],["=", 1, ";", 0]]

#bool const
partDel += ["initialization", "const", "const"]
partDel2[14] = "measbegin"
partDel2[15] = "inpins"
partDel2[16] = "adap60"
delStr += ["//<boolconst>\n", "", ""]
searchStr += ["veeon", "adap60", "deltaboard135"]
strB += ["=", "=", "="]
strE += [";", ";", ";"]
delB += [1, 1, 1]
delE += [0, 0, 0]
errMes += ["No vee info found", "No adap60 info found", "No repin info found"]
replS += [True, True, True]
repeat += [False, False, False]
multStr += [False, False, False]
multLine += [False, False, False]
multVar += [False, False, False]

#add consts
for i in range(17, 21):
    partDel.append("initialization")
    partDel2[i] = "pinchange"
delStr += ["//<addconst>\n", "", "", ""]
searchStr += ["pwr", "gnd", "comdcmpwr", "comdcmgnd"]
strB += ["=", "=", "=", "="]
strE += [";", ";", ";", ";"]
delB += [1, 1, 1, 1]
delE += [0, 0, 0, 0]
errMes += ["No power source info found", "No gnd source info found", "No power connect info founs", "No gnd connect info found"]
replS += [True, True, True, True]
repeat += [False, False, False, False]
multStr += [False, False, False, False]
multLine += [False, False, False, False]
multVar += [False, False, False, False]

#pin as tlargesets
partDel.append("numofpin")
partDel2[21] = "inpins"
delStr.append("//<pins>\n")
searchStr.append("tlargeset")
strB.append("")
strE.append("")
delB.append(0)
delE.append(0)
errMes.append("No pin sets found")
replS.append(True)
repeat.append(False)
multStr.append(True)
multLine.append(False)
multVar.append(True)
delimList[len(partDel) - 1] = [["", 0, ":", 0], ["[", 1, "]", 0]]

#pin groups
partDel.append("numofpin")
partDel2[22] = "tin"
delStr.append("//<ping>\n")
searchStr.append("tlargeset")
searchStr2[len(partDel) - 1] = "pins"
strB.append("")
strE.append("")
delB.append(0)
delE.append(0)
errMes.append("No pin groups found")
replS.append(True)
repeat.append(False)
multStr.append(True)
multLine.append(True)
multVar.append(True)
delimList[len(partDel) - 1] = [["", 0, ":", 0], ["[", 1, "]", 0]]
varEnds[len(partDel) - 1] = "]"
    
#board lists
partDel.append("numofpin")
partDel2[23] = "tin"
delStr.append("//<boards>\n")
searchStr.append("tlargeset")
searchStr2[len(partDel) - 1] = "board"
strB.append("")
strE.append("")
delB.append(0)
delE.append(0)
errMes.append("No board list found")
replS.append(True)
repeat.append(False)
multStr.append(True)
multLine.append(True)
multVar.append(True)
delimList[len(partDel) - 1] = [["", 0, ":", 0], ["[", 1, "]", 0]]
varEnds[len(partDel) - 1] = "]"

#pin names
partDel.append("numofpin")
partDel2[24] = "tin"
delStr.append("//<pinnames>\n")
searchStr.append("tnamepin")
strB.append("(")
strE.append(")")
delB.append(1)
delE.append(0)
errMes.append("No pin names array found")
replS.append(True)
repeat.append(False)
multStr.append(False)
multLine.append(True)
multVar.append(False)
varEnds[len(partDel) - 1] = ")"

#test vectors
partDel.append("const")
partDel2[25] = "initialization"
delStr.append("//<vectors>\n")
searchStr.append("tvectors")
strB.append("")
strE.append("")
delB.append(1)
delE.append(0)
errMes.append("No vectors info found")
replS.append(True)
repeat.append(False)
multStr.append(True)
multLine.append(True)
multVar.append(True)
delimList[len(partDel) - 1] = [["", 0, ":", 0], ["(", 1, ")", 0]]
varEnds[len(partDel) - 1] = ")"

#additional procedures
partDel.append("//<strangefuncs>")
delStr.append("//<addproc>\n")
searchStr.append("")
strB.append("")
strE.append("")
delB.append(0)
delE.append(0)
errMes.append("No additional procedures info found")
replS.append(False)
repeat.append(False)
multStr.append(True)
multLine.append(False)
multVar.append(False)

#init file loads
for i in range(27, 30):
    partDel.append("initialization")
    partDel2[i] = "measbegin"
delStr += ["//<loadfki>\n", "//<loadtmei>\n", "//<activatefki>\n"]
searchStr += ["loadfkfile", "time_to_fkrec", "activatefilefk"]
strB += ["(", "(", "("]
strE += [")", ")", ")"]
delB += [1, 1, 1]
delE += [0, 0, 0]
errMes += ["No fk file load found in init", "No time connection found in init", "No fk activation found in init"]
replS += [True, True, True]
repeat += [False, False, False]
multStr += [True, True, True]
multLine += [False, False, False]
multVar += [False, False, False]

#all pins & unconnect & transparant
for i in range(30, 33):
    partDel.append("initialization")
    partDel2[i] = "measbegin"
delStr += ["//<allpins>\n", "//<unconnecti>\n", "//<transp>\n"]
searchStr += ["allpins", "unconnectalll", "transparant"]
strB += ["=", "(", "'"]
strE += [";", ")", "'"]
delB += [1, 1, 1]
delE += [0, 0, 0]
errMes += ["No all pins variable found", "No unconnect found", "No transparant found"]
replS += [False, True, False]
repeat += [False, False, False]
multStr += [True, False, False]
multLine += [False, False, False]
multVar += [False, False, False]

#main part unconnect, fk and contact
partDel += ["//<mainpart>", "//<mainpart>", "//<mainpart>", "//<mainpart>", "//<mainpart>"]
delStr += ["//<unconnectm>\n", "//<loadfkm>\n", "//<loadtmem>\n", "//<activatefkm>\n", "//<contact>\n"]
searchStr += ["unconnectalll", "loadfkfile", "time_to_fkrec", "activatefilefk", "contact"]
strB += ["(", "(", "(", "(", "("]
strE += [")", ")", ")", ")", ")"]
delB += [1, 1, 1, 1, 1]
delE += [0, 0, 0, 0, 0]
errMes += ["No unconnect found in main", "No fk file load found in main", "No time connection found in main", "No fk activation found in main", "No contact func found"]
replS += [True, True, True, True, False]
repeat += [False, False, False, False, False]
multStr += [False, True, True, True, False]
multLine += [False, False, False, False, False]
multVar += [False, False, False, False, False]

#power connect part
partDel.append("//<mainpart>")
delStr.append("//<pwrson>\n")
searchStr.append("setpower")
strB.append("(")
strE.append(")")
delB.append(1)
delE.append(0)
errMes.append("No power settings found")
replS.append(False)
repeat.append(False)
multStr.append(True)
multLine.append(False)
multVar.append(False)

#program body with procedures
partDel.append("//<diffpart>")
delStr.append("//<funcspart>\n")
searchStr.append("")
strB.append("")
strE.append("")
delB.append(0)
delE.append(0)
errMes.append("No program body found")
replS.append(False)
repeat.append(False)
multStr.append(True)
multLine.append(False)
multVar.append(False)

#icc_off and unconnect
partDel += ["finalization", "finalization"]
partDel2[40] = "end."
partDel2[41] = "end."
delStr += ["//<iccoff>\n", "//<unconnectf>\n"]
searchStr += ["icc_off", "unconnectalll"]
strB += ["", "("]
strE += [";", ")"]
delB += [0, 1]
delE += [0, 0]
errMes += ["No icc off found", "No unconnect found in fin"]
replS += [True, True]
repeat += [False, False]    
multStr += [True, False]
multLine += [False, False]
multVar += [False, False]

def templ_gen(fName, catalog, log):
    with open(fName + ".ptf", "r") as f:
        pText = f.read()
        fName = fName.split("/")[-1]
        f2 = open(catalog + fName + "_old.ptf", "w")
        f2.write(pText)            
        f2.close()
    
    pText = pText.split("\n")
    pText = clean_text(pText)
    pText = del_comments(pText, log)
    pText = replace_smth(pText, log, "SecondLevelOn", replace_second_level, "ConfChnlN")
    pText = replace_smth(pText, log, "UO(", replace_uo, "UO")
    pText = replace_smth(pText, log, "ILI(", replace_ili, "ILI")
    pText = replace_smth(pText, log, "IO(", replace_ili, "ILI")
    pText = replace_smth(pText, log, "I0S(", replace_ios, "IOS")
    pText = replace_smth(pText, log, "TP(", replace_tp, "TP")
    pText = replace_smth(pText, log, "UpDown(", replace_updown, "UpDown")
    pText = insert_xml(pText, "procedure", "initialization", "//<strangefuncs>", add = True)
    pText = insert_xml(pText, "measbegin", ["uo(", "ili(", "icc_on", "updown(", " fk(", "tp("], "//<mainpart>", "//<mainpart>\n//<diffpart>")
    pText = insert_xml(pText, "//<diffpart>", "programmbrake", "", "//<diffpart>")
    pText = replace_funcs(pText, "connectpin(", "ConnectPinN(", log)
    pText = replace_funcs(pText, "connectpins(", "ConnectPinsN(", log)
    pText = replace_funcs(pText, "conf_chnl_hand(", "ConfChnl(", log)
    pText = replace_funcs(pText, "conf_levels_hand(", "ConfChnlN(", log)
    f = open(catalog + fName + "_templ.ptf", "w")
    templ_get_part(pText, f, partDel, delStr, searchStr, strB, strE, delB, delE, errMes, replS, repeat, multStr, multLine, multVar, delimList, varEnds, log, partDel2, searchStr2)
    f.close()
    del(f)
    
fName = "D:/_python/ims/transform/533 ИЕ15_ТУ/533ИЕ15_ТУ"
log = open("D:/_python/ims/transform/533 ИЕ15_ТУ/log.txt", "w")

def test(fName, catalog, log):
    with open(catalog + fName.split("/")[-1] + ".ptf", "r") as f:
        pText = f.read().split("\n")
    
    pText = clean_text(pText)
    pText = del_comments(pText, log)
    with open(catalog + fName.split("/")[-1] + "_new.ptf", "w") as f:
        for s in range(len(pText) - 1):
            f.write(pText[s] + "\n")
        f.write(pText[-1])

templ_gen(fName, "D:/_python/ims/transform/533 ИЕ15_ТУ/", log)
log.close()
with open("D:/_python/ims/transform/533 ИЕ15_ТУ/log.txt", "r") as f:
    seq = f.read().split("\n")
    
for i in seq:
    print(i)
print("New program generated: 533 ИЕ15_ТУ_new.ptf")