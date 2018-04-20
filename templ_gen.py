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
        
        temp.append(pText[i])
    
    return temp[:]    

def find_var(text, i, searchS, strB = "'", strE = "'", disB = 1, disE = 0, errMes = "", replS = True, repeat = False, log = "log.txt"):
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
        if s.find(strB) == -1 or s.find(strE) == -1:
            continue
        s = get_quote(text[i], strB, disB, strE, disE)
        if repeat:
            s = get_quote(s, strB, disB, "", 0)
        if replS:
            s = s.replace(" ", "")
        return s, i
    
def templ_get_part(pText, f, partDel, delStr, searchStr, strB, strE, delB, delE, errMes, replS, repeat, multStr, multLine, multVar, delimList, varEnds, log):
    for i in range(len(partDel)):
        if partDel[i] == "":
            currPart = pText
        else:
            currPart = get_text_part(pText, partDel[i], log)
            
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
                s, k = find_var(currPart, k, searchStr[i], "", "", 0, 0, err, replS[i], False, log)
                
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
                s, k = find_var(currPart, k, searchStr[i], strB[i], strE[i], delB[i], delE[i], err, replS[i], repeat[i], log)
            
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
            f.write(s + "\n")
            
            if not multStr[i]:
                break
            
        if i == len(partDel) - 1 or delStr[i + 1] != "":
            f.write(block)
"""
#program name, creation date, designer, tu
partDel = ["//<head>", "//<head>", "//<head>", "//<head>"]
#adapter, ku, jumpers, last board
partDel += ["//<namestrings>", "//<namestrings>", "//<namestrings>", "//<namestrings>"]
delStr = ["//<strconst>\n", "", "", "", "", "", "", ""]
searchStr = ["program ", "data", "raz", "tu", "adap", "ku", "jamper", "pinlast"]
strB = ["program", ":", "'", "'", "'", "'", "'", "'"]
strE = [";", ";", "'", "'", "'", "'", "'", "'"]
delB = [7, 1, 1, 1, 1, 1, 1, 1]
delE = [0, -1, 0, 0, 0, 0, 0, 0]
errMes = ["No program name found", "No creation date found", "No designer name found"]
errMes += ["No TU found", "No adapter info found", "No contact device info found"]
errMes += ["No jumpers info found", "No last board info found"]
replS = [True, True, False, False, False, False, False, False]
repeat = [False, True, False, False, False, False, False, False]
multStr = [False, False, False, False, False, False, False, False]
multLine = [False, False, False, False, False, False, False, False]
multVar = [False, False, False, False, False, False, False, False]
delimList = {}
varEnds = {}

#fk names
partDel.append("//<namestrings>")
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
partDel += ["//<pinpart>", "//<const>", "//<const>", "//<const>", "//<const>"]
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
partDel += ["//<initpart>", "//<namestrings>", "//<namestrings>"]
delStr += ["//<boolconst>\n", "", ""]
searchStr += ["veeon", "adap60", "pins "]
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
partDel += ["//<initpart>", "//<initpart>", "//<initpart>", "//<initpart>"]
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
partDel.append("//<pins>")
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
partDel.append("//<inoutpins>")
delStr.append("//<ping>\n")
searchStr.append("tlargeset")
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
partDel.append("//<pinpart>")
delStr.append("//<boards>\n")
searchStr.append("boardlist")
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
partDel.append("//<namepin>")
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
partDel.append("//<vectorspart>")
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
partDel += ["//<initpart>", "//<initpart>", "//<initpart>"]
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
partDel += ["//<initpart>", "//<initpart>", "//<initpart>"]
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
partDel += ["//<finalpart>", "//<finalpart>"]
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
multVar += [False, False]5
"""
def templ_gen(fName, catalog, log):
    with open(fName + ".ptf", "r") as f:
        pText = f.read()
        fName = fName.split("/")[-1]
        f2 = open(catalog + fName + "_old.ptf", "w")
        f2.write(pText)            
        f2.close()
    
    pText = pText.split("\n")
    pText = clean_text(pText)

    f = open(catalog + fName + "_templ.ptf", "w")            
    templ_get_part(pText, f, partDel, delStr, searchStr, strB, strE, delB, delE, errMes, replS, repeat, multStr, multLine, multVar, delimList, varEnds, log)
    f.close()
    del(f)

def gen_var_csv():
    with open("vars.csv", "w") as f:
        varList = [partDel, delStr, searchStr, strB, strE, delB, delE, errMes, replS, repeat, multStr, multVar, multLine, delimList, varEnds]
        varNames = ["partDel", "delStr", "searchStr", "strB", "strE", "delB", "delE", "errMes", "replS", "repeat", "multStr", "multVar", "multLine", "delimList", "varEnds"]
        for n in range(len(varList)):
            s = varNames[n] + ";"
            for i in range(len(partDel)):
                if type(varList[n]) == list:
                    t = str(varList[n][i])
                else:
                    t = str(varList[n].get(i, ""))
                    
                t = t.replace("\n", "")
                t = t.replace(";", "€")
                s  += t + ";"
            s = s[:-1] + "\n"
            f.write(s)

def get_var_csv(fName):
    with open(fName, "r") as f:
        var = f.read().split("\n")
    for i in range(len(var)):  
        var[i] = var[i].split(";")[1:]
    var = var[:-1]
    for i in range(len(var)):
        for j in range(len(var[0])):
            var[i][j] = var[i][j].replace("€", ";")
            

    for i in range(len(var[0])):
        if var[1][i] != "":
            var[1][i] += "\n"
        var[5][i] = int(var[5][i])
        var[6][i] = int(var[6][i])
        for k in range(8, 13):
            if var[k][i] == "True":
                var[k][i] = True
            else:
                var[k][i] = False
        if var[13][i] != "":
            t = var[13][i].split(",")
            if t[0].find('"') == -1:
                t[0] = get_quote(t[0])
            else:
                t[0] = "'"
            t[1] = int(t[1])
            if t[2].find('"') == -1:
                t[2] = get_quote(t[2])
            else:
                t[2] = "'"
            t[3] = int(get_quote(t[3], "", 0, "]", 0))
            if t[4].find('"') == -1:
                t[4] = get_quote(t[4])
            else:
                t[4] = "'"
            t[5] = int(t[5])
            if t[6].find('"') == -1:
                t[6] = get_quote(t[6])
            else:
                t[6] = "'"
            t[7] = int(get_quote(t[7], "", 0, "]", 0))
            var[13][i] = [t[:4], t[4:]]
    t1 = {}
    t2 = {}
    for i in range(len(var[0])):
        if var[13][i] != "":
            t1[i] = var[13][i]
        if var[14][i] != "":
            t2[i] = var[14][i]
    var[13] = t1
    var[14] = t2
    return tuple(var[:15])

partDel = []
delStr = []
searchStr = []
strB = []
strE = []
delB = []
delE = []
errMes = []
replS = []
repeat = []
multStr = []
multVar = []
multLine = []
delimList = {}
varEnds = {}

partDel, delStr, searchStr, strB, strE, delB, delE, errMes, replS, repeat, multStr, multVar, multLine, delimList, varEnds = get_var_csv("vars.csv")

fName = "C:/_python/ims/transform/5514БЦ1Т1-08S_ТУ"    
log = open("C:/_python/ims/transform/log.txt", "w")
templ_gen(fName, "C:/_python/ims/transform/", log)
log.close()