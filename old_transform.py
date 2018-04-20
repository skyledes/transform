# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:45:12 2017

@author: edino

"""

from str_work import *


def load_file(fileName):
    """
    filename - string, name of existing ptf file
    returns text from file as string
    """
    with open(fileName, "r") as f:
        ret = f.read()
    return ret

def break_file(fileStr):
    """
    fileStr - string, text from loaded file
    returns list of strings - fileStr broken by \n
    """
    brList = fileStr.split("\n")
    return brList

def clean_list(fileList):
    """
    fileList - list of strings
    clear list from empty strings
    """
    for s in range(len(fileList) - 1, -1,-1):
        if fileList[s] == "":
            del(fileList[s])
        elif fileList[s].replace(" ", "").replace("\t", "") == "":
            del(fileList[s])
        else:
            fileList[s] = fileList[s].replace("\t", " ")


def getPName(fileName, params):
    """
    fileName - string, name of file,
    params - dict, parameters of program
    returns string like "PROGRAM IMS%fileName transcribed into english%"
    """
    if fileName.find("_ТУ") != -1:
        pName = fileName[:fileName.index("_ТУ")]
    else:
        pName = fileName[:fileName.index(".")]
    pName = pName.upper()
    params["pname"] = "IMS" + convert_to_eng(pName)
    ret = "  PROGRAM IMS" + convert_to_eng(pName)
    return ret
        
def getVer(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  Ver  : PChar = 'Версия ПП: ver.0VP';"
    if ver found - ver = ver + 1, else ver = 2.0
    adds VP if not already there
    """
    ret = ""
    for s in fileList:
        if s.lower().find("ver  : pchar") != -1:
            ret = s
            break
    if ret == "":
        ret = "  Ver  : PChar = 'Версия ПП: 2.0VP';"
        params["ver"] = "2.0VP"
    else:
        ver = str(int(getQuote(ret, displb = 12, end = ".")) + 1)
        params["ver"] = ver + ".0VP"
        ret = "  Ver  : PChar = 'Версия ПП: " + ver + ".0VP';"
    return ret

def getDate(params):
    """
    params - dict, parameters of program
    return string like "  Data : PChar = 'Дата отладки: %currentDate%';
    """
    import datetime
    now = datetime.datetime.now()
    date = now.strftime("%d.%m.%y")
    params["date"] = date
    ret = "  Data : PChar = 'Дата отладки: " + date + "';"
    return ret

def getDesigner(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  Raz  : PChar = razr';"
    if razr not found razr = Virtual Programmer :)
    """
    ret = ""
    name = ""
    for s in fileList:
        if s.lower().find("raz  : pchar") != -1:
            ret = s
            params["designer"] = getQuote(ret)
            break
        elif s.lower().find("автор") != -1:
            s = getQuote(s, begin = ":", displb = 2, end = "")
            if s.find(" ") == -1:
                name = s
            else:
                name = getQuote(s, "", 0, " ")
                s = getQuote(s, begin = " ", displb = 0, end = "")
                if s.find(" ") != -1:
                    s = s[1:]
                    name += " " + s[0] + "."
                    if s.find(" ") != -1:    
                        s = getQuote(s, begin = " ", displb = 0, end = "")
                        name += s[1] + "."
            break
    if ret == "":
        if name == "":
            print("No designer name :(")
            ret = "  Raz  : PChar = 'Virtual Programmer';"
            params["designer"] = ""
        else:
            ret = "  Raz  : PChar = '" + name + "';"
            params["designer"] = name
    return ret

def getTU(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  TU   : PChar = 'TU';"
    if TU not found TU = ''
    """
    ret = ""
    TU = ""
    for s in fileList:
        if s.lower().find("tu   : pchar") != -1:
            ret = s
            break
        elif s.lower().find("набор тестов") != -1:
            TU = getQuote(s, "для", 4, "")
            break
    if ret == "":
        if TU == "":
            ret = "  TU   : PChar = ''; // !!!! NO TU !!!!"
            print("No TU found")
        else:
            ret = "  TU   : PChar = '" + TU + "';"
    params["tu"] = getQuote(ret)
    return ret

def getTypes(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  TNamePin = Array[0..pinNum"] of String;\n"
                        "  TVectors = Array[0..pinNum"] of Integer;"
    if pinNum not found pinNum = 0
    """    
    ret = ""
    pinNum = 0
    for s in fileList:
        if s.lower().find("tnamepin") != -1:
            s = getQuote(getQuote(s, begin = "[", end = "]"), "..", 2, "")
            pinNum = int(s)
            break
    if pinNum == 0:
        print("No pinNum found")
    ret  = "  TNamePin = Array[0.." + str(pinNum) + "] of String;\n"
    ret += "  TVectors = Array[0.." + str(pinNum) + "] of Integer;"
    params["pinnum"] = pinNum
    return ret

def writeDebug():
    """
    returns string with debug part of program
    """
    ret = "//<Debugpart>\n"
    ret += "Const\n"
    ret += "//включение режима отладки\n"
    ret += "(*)\n"
    ret += "DEBUG  : Boolean = true;\n"
    ret += "(*)\n"
    ret += "DEBUG  : Boolean = false;\n"
    ret += "(**)\n"
    ret += "//<Debugpart>"
    return ret

def getFileNames(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns strings like "  FileName : String = 'name';"
    for each FileName found,
    if FileName not found FileName = ""
    """
    ret = ""
    curr = ""
    params["filenames"] = {}
    for s in fileList:
        if s.lower().find("filename") != -1:
            if s.find(":") != -1:
                ch = ":"
            else:
                if s.find("=") != -1:
                    ch = "="
                else:
                    continue
            curr = getQuote(s)
            ret += "  " + getQuote(s, "", 0, ch).replace(" ", "") + " : String = '" + curr + "';\n"
            params["filenames"][getQuote(s, "", 0, ch).replace(" ", "")] = curr
    if ret == "":
        print("No fileName found")
        ret = "  FileName : String = ''; // !!! NO FILENAME !!!\n"
    ret = ret[:-1]
    return ret

def getAdapter(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  Adap     : PChar   = 'adap';"
    if adap not found adap = ""
    if adap like "ФРМИ4.448.001" then adap = "Адаптер ФРМИ4.448.001(-01/-02/-03)"
    """
    ret = ""
    for s in fileList:
        if  s.replace(" ", "").lower().find("adap:") != -1 or s.replace(" ", "").lower().find("adap=") != -1:
            adap = getQuote(s)
            if adap.upper().index("ФРМИ4.448.001") != -1:
                adap = "Адаптер ФРМИ4.448.001(-01/-02/-03)"
            params["adap"] = adap
            ret = "  Adap     : PChar   = '" + adap + "';"
            break
    if ret == "":
        print("No adapter found")
        ret = "  Adap     : PChar   = ''; // !!! NO ADAPTER !!!"
        params["adap"] = ""
    return ret

def getKU(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  KU       : PChar   = 'ku';"
    if ku not found ku = ""
    """
    ret = ""
    for s in fileList:
        if s.lower().find("ku") != -1:
            ku = s
            if ku.replace(" ", "").lower().index("ku") != 0:
                continue
            ku = getQuote(s)
            params["ku"] = ku
            ret = "  KU       : PChar   = '" + ku + "';"
            break
    if ret == "":
        print("No KU found")
        ret = "  KU       : PChar   = ''; // !!! NO KU !!!"
        params["ku"] = ""
    return ret

def getJumper(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  Jamper   : PChar   = 'jump';"
    if jump not found jump = ""
    """
    ret = ""
    
    for s in fileList:
        if s.lower().find("jamper") != -1:
            jump = s
            if jump.find("(**)") > jump.find("(*)"):
                jump = getQuote(jump, "*", 2, "")
                jump = getQuote(jump, "*", 2, "")
            jump = getQuote(jump)
            ret = "  Jamper   : PChar   = '" + jump + "';"
            params["jumper"] = jump
            break
    
    if ret == "":
        print("No jumpers found")
        ret = "  Jamper   : PChar   = ''; // !!! NO JUMPERS"
        params["jumper"] = ""
    return ret

def getPinLast(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  PinLast  : PChar   = 'pin';"
    if pin not found pin = "Pin1"
    """
    ret = ""
    
    for s in fileList:
        if s.lower().find("pinlast") != -1:
            pin = getQuote(s)
            ret = "  PinLast  : PChar   = '" + pin + "';"
            params["pinlast"] = pin
            break
        if s.lower().find("pin2") != -1:
            if s.lower().find("pchar") > s.lower().find("pin2"):
                pin = s
                if pin.find("(**)") > pin.find("(*)"):
                    pin = getQuote(pin, "*", 2, "")
                    pin = getQuote(pin, "*", 2, "")
                pin = getQuote(pin)
                if len(pin) == 0:
                    pin = "Pin1"
                else:
                    while pin.lower().find("pin") != -1:
                        pin = pin[pin.lower().index("pin") + 3:]
                    pin = "Pin" + pin[0]
                print("Check PinLast")
                ret = "  PinLast  : PChar   = '" + pin + "';"
                params["pinlast"] = pin
                break
    if ret == "":
        print("No last pin found")
        ret = "  PinLast  : PChar   = 'Pin1'; // NO PIN LAST"
        params["pinlast"] = ""
    return ret
     
def getAdap60(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  Adap60   : Boolean = adap60;"
    if adap60 not found adap60 = false
    """
    ret = ""
    
    for s in fileList:
        if s.lower().find("adap60") != -1:
            adap60 = getQuote(s, begin = "=", end = ";").replace(" ", "").lower()
            ret = "  Adap60   : Boolean = " + adap60 + ";"
            if adap60 == "false":
                params["adap60"] = False
            else:
                params["adap60"] = True
            break
    
    if ret == "":
        print("No adap60 found")
        ret = "  Adap60   : Boolean = false;"
        params["adap60"] = False
    return ret

def getBoardType(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  PinS     : Boolean = bType;"
    if bType not found bType = true
    """
    ret = ""
    bType = ""
    
    for s in range(len(fileList)):
        if fileList[s].lower().find("pins") != -1 and fileList[s].lower().find("boolean") != -1:
            bType = fileList[s]
            bType = getQuote(bType, "=", end = ";").replace(" ", "")
            ret = "  PinS     : Boolean = " + bType.lower() + ";"
            break
        if fileList[s].lower().find("deltaboard135") != -1:
            if fileList[s - 1].find("(**)") != -1:
                bType = "true"
            else:
                bType = "false"
                
            ret = "  PinS     : Boolean = " + bType + ";"
            break
        if fileList[s].lower().find("{$i") != -1 and fileList[s].lower().find("pincofig") != -1:
            bType = fileList[s]
            bType = getQuote(bType, "pincofig", 0, ".inc")
            if bType[-1] < "0" or bType[-1] > "9":
                bType = "true"
            else:
                bType = "false"
    
    if ret == "":
        if bType == "":
            print("No board type found")
            ret = "  PinS     : Boolean = true;"
            bType = "true"
        else:
            print("Check board type")
            ret = "  PinS     : Boolean = " + bType + ";"
    if bType == "true":
        params["bType"] = True
    else:
        params["bType"] = False
    return ret

def getPinNum(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    returns string like "  NumOfPin = pNum;"
    if pNum not found pNum = 256
    """
    ret = ""
    for s in fileList:
        if s.lower().find("numofpin") != -1:
            pNum = getQuote(s, "=", end = ";").replace(" ", "")
            if pNum == "13":
                pNum = "14"
            if pNum == "15":
                pNum = "16"
            ret = "  NumOfPin = " + pNum + ";"
            break
    
    if ret == "":
        print("No num of pins found")
        ret = "  NumOfPin = 256;"
        pNum = 256
    params["pNum"] = 256
    return ret

def getPinNames(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    return strings like "  pName          : TLargeSet = [pNum];"
    if no pName found return ""
    """
    ret = ""
    size = len("A1          ")
    pName = []
    pNum = []
    for s in range(len(fileList)):
        if fileList[s].lower().find("tlargeset") != -1 and fileList[s].lower().find("pins") == -1 and fileList[s].lower().find("list") == -1:
            while fileList[s].lower().find("tlargeset") != -1:
                pName.append(fileList[s])
                pNum.append(pName[-1])
                pName[-1] = getQuote(pName[-1], "", 0, ":").replace(" ", "")
                pNum[-1] = getQuote(pNum[-1], "[", end = "]")
                if len(pName[-1]) > size:
                    size = len(pName[-1])
                s += 1
            break
    # is it really necessary?
    if len(pName) == 0:
        for s in range(len(fileList)):
            if fileList[s].lower().find("tnamepin") != -1 and fileList[s].lower().find("array") == -1:
                print("Check pin names")
                curr = fileList[s]
                while fileList[s].find(")") == -1:
                    s += 1
                    curr += fileList[s]
                curr = getQuote(curr, "(", end = ")").lower().replace(" ", "")
                pName = curr.split(",")
                n = 0
                for k in range(len(pName)):
                    n += 1
                    p = getQuote(pName[k])
                    pName[k] = p
                    if (p == "nc") or (p == "gnd") or (p == "vcc") or (p == "vdd") or (p == "vee") or (p == "") or (p == "0"):
                        pNum.append("0")
                    else:
                        if n < 10:
                            pNum.append("Pin0" + str(n))
                        else:
                            pNum.append("Pin" + str(n))
                break
            
    if len(pName) > 0:
        for p in range(len(pName)):
            pName[p] = pName[p] + " " * (size - len(pName[p]))
            if pNum[p] != "0":
                if "0" <= pName[p][0] <= "9":
                    print("Wrong pin name: " + pName[p])
                ret += "  " + pName[p].upper() + ": TLargeSet = [" + pNum[p] + "];\n"
        ret = ret[:-1]
    else:
        print("No pin names found")
        
    params["pNames"] = {}
    for i in range(len(pName)):
        params["pNames"][pName[i]] = pNum[i]
    return ret

def getGroupNames(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    return strings like "  pName          : TLargeSet = [pNum];"
    if no pName found return "  InPins     : TLargeSet = [ ]; //!!! NO IN PINS\n
                                OutPins    :TLargeSet = [ ]; //!!! NO OUT PINS"
    """
    ret = ""
    size = len("OutPins    ")
    pName = []
    pNums = []
    cont = 0
    for s in range(len(fileList)):
        if cont > 0:
            cont -= 1
            continue
        if fileList[s].lower().find("tlargeset") != -1 and fileList[s].lower().find("pins") != -1:
            pName.append(fileList[s])
            while pName[-1].find("]") == -1:
                s += 1
                cont += 1
                pName[-1] += fileList[s]
            pNums.append(pName[-1])
            pName[-1] = getQuote(pName[-1], "", 0, ":",).replace(" ", "")
            pNums[-1] = getQuote(pNums[-1], "[", end = "]")
            if len(pName[-1]) > size:
                size = len(pName[-1])
            
    if len(pName) > 0:
        for p in range(len(pName)):
            pName[p] = pName[p] + " " * (size - len(pName[p]))
            ret += "  " + pName[p] + ": TLargeSet = [" + pNums[p] + "];\n"
        ret = ret[:-1]
    else:
        print("No pin groups found")
        ret = "  InPins     : TLargeSet = [ ]; //!!! NO IN PINS\n"
        ret += "  OutPins    :TLargeSet = [ ]; //!!! NO OUT PINS"
    params["gNames"] = {}
    for i in range(len(pName)):
        params["gNames"][pName[i]] = pNums[i]
    return ret
        
def getBoardLists(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    return strings like "  bName  : TLargeSet = [bList];"
    if no bName found return "  BoardList  : TLargeSet = [Board1]; //!!! NO BOARD LIST FOUND"
    """
    ret = ""
    size = len("BoardList   ")
    bName = []
    bList = []
    cont = 0
    for s in range(len(fileList)):
        if cont > 0:
            cont -= 1
            continue
        if fileList[s].lower().find("tlargeset") != -1 and fileList[s].lower().find("boardlist") != -1:
            bName.append(fileList[s])
            while bName[-1].find("]") == -1:
                s += 1
                cont += 1
                bName[-1] += fileList[s]
            bList.append(bName[-1])
            bName[-1] = getQuote(bName[-1], "", 0, ":").replace(" ", "")
            bList[-1] = getQuote(bList[-1], "[", end = "]")
            if len(bName[-1]) > size:
                size = len(bName[-1])
            
    if len(bName) > 0:
        for p in range(len(bName)):
            bName[p] = bName[p] + " " * (size - len(bName[p]))
            ret += "  " + bName[p] + ": TLargeSet = [" + bList[p] + "];\n"
        ret = ret[:-1]
    else:
        print("No board lists found")
        ret = "  BoardList  : TLargeSet = [Board1]; //!!! NO BOARD LIST FOUND"
        
    params["bLists"] = {}
    for i in range(len(bName)):
        params["bLists"][bName[i]] = bList[i]
    return ret

def getFirstPin(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    return strings like "  FirstPin   : Integer = pin;"
    if no pin found return "  FirstPin   : Integer = Pin01; //!!! NO FIRST PIN FOUND"
    """
    ret = ""
    
    for s in fileList:
        if s.lower().find("firstpin") != -1:
            pin = getQuote(s, "=", end = ";").replace(" ", "")
            ret = "  FirstPin   : Integer = " + pin + ";"
            break
    
    if ret == "":
        print("No first pin found")
        ret = "  FirstPin   : Integer = Pin01; //!!! NO FIRST PIN FOUND"
        pin = "Pin01"
    params["fPin"] = pin
    return ret

def getLastPin(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    return strings like "  LastPin    : Integer = pin;"
    if no pin found return "  LastPin    : Integer = NumOfPin; //!!! NO LAST PIN FOUND"
    
    """
    ret = ""
    
    for s in fileList:
        if s.lower().find("lastpin") != -1:
            pin = getQuote(s, "=", end = ";").replace(" ", "")
            ret = "  LastPin    : Integer = " + pin + ";"
            break
    
    if ret == "":
        print("No last pin found")
        ret = "  LastPin    : Integer = NumOfPin; //!!! NO LAST PIN FOUND"
        pin = "NumOfPin"
    params["lPin"] = pin
    print(pin)
    return ret

def getNamePin(fileList, params):
    """
    fileList - list of strings, program text,
    params - dict, parameters of program
    return string like "  //номер вывода:          1 ... n"
                       "  NamePin: TNamePin = ( PinNamesList );
    if no PinNames found PinNamesList = (I1, I2, ... I_PinNum)
    e
    """
    ret = ""
    
    for s in fileList:
        pass
    if ret == "":
        ret = "  NanePin: TNamePin = ("
        if len(params["pNames"]) == 0:
            for i in range(params["pinnum"]):
                pass
    
    return ret

def genNew(fileName, fileList):
    """
    main func
    fileName - name of new file to save to
    fileList - list of strings, existing program text
    """
    print("\n" + fileName)
    params = {}
    with open(fileName, "w") as f:
        f.write("//<Head>\n")
        #get programm name
        f.write(getPName(fileName, params) + "\n")
        f.write("//Const\n")
        #get programm version
        f.write(getVer(fileList, params) + "\n")
        #get date
        f.write(getDate(params) + "\n")
        #get designer
        f.write(getDesigner(fileList, params) + "\n")
        #get DataSheet
        f.write(getTU(fileList, params) + "\n")
        f.write("//<Head>\n")
        #get Types
        f.write("//<Types>\n")
        f.write("Type\n")
        f.write(getTypes(fileList, params) + "\n")
        f.write("//<Types>\n")
        #write Debugpart (constant)
        f.write(writeDebug() + "\n")
        #write program name for tes and tme files
        f.write("//<Namestrings>\n")
        f.write("  //имя файла с ФК\n")
        f.write(getFileNames(fileList, params) + "\n")
        #write adapter
        f.write("  //используемые для проверки адаптеры\n")
        f.write(getAdapter(fileList, params) + "\n")
        #write ku
        f.write("  //используемое для проверки КУ\n")
        f.write(getKU(fileList, params) + "\n")
        #write jumpers info
        f.write("  //установка перемычек\n")
        f.write(getJumper(fileList, params) + "\n")
        #write last pin (num of boards used)
        f.write("  //необходимость подключения больше 1 пин-разъема\n")
        f.write(getPinLast(fileList, params) + "\n")
        #write adap60 mode
        f.write("  //наличие перепиновки под Адап60\n")
        f.write(getAdap60(fileList, params) + "\n")
        #write board type (S or H)
        f.write("  //тип плат на которых проверяется ИС\n")
        f.write(getBoardType(fileList, params) + "\n")
        f.write("//<Namestrings>\n")
        #write num of pins
        f.write("//<Pinpart>\n")
        f.write(getPinNum(fileList, params) + "\n")
        #write repin include
        f.write("  //загрузка файла перепиновки\n")
        ###think about it
        f.write("  {$I !Source\PinConfigAll.inc}")
        #write pin names
        f.write("//<Pins>\n")
        f.write("  //имена выводов ИС\n")
        f.write(getPinNames(fileList, params) + "\n")
        f.write("//<Pins>\n")
        #write group names
        f.write("  //массивы входных, выходных и двунаправленных выводов\n")
        f.write("//<Inoutpins>\n")
        f.write(getGroupNames(fileList, params) + "\n")
        f.write("//<Inoutpins>\n")
        #write boardLists
        f.write("  //список используемых плат\n")
        f.write(getBoardLists(fileList, params) + "\n")
        #write first pin
        f.write("  //первый и последний выводы ИС\n")
        f.write(getFirstPin(fileList, params) + "\n")
        #write last pin
        f.write(getLastPin(fileList, params) + "\n")
        f.write("//<Pinpart>\n")
        #write vectors part
        f.write("//<Vectorspart>\n")
        #write pin names array
        f.write("  //массив имен выводов\n")
        f.write("//<Namepin>\n")
        f.write(getNamePin(fileList, params) + "\n")
        
    print(params.keys())    
    print("All done")
#        
#
#fileStr1 = load_file("1505ИЕ5_ТУ.ptf")
#fileList1 = break_file(fileStr1)
#del(fileStr1)
#clean_list(fileList1)
#genNew("1505ИЕ5_ТУ_new.ptf", fileList1)
#
#fileStr2 = load_file("5514БЦ1Т1-08S_ТУ.ptf")
#fileList2 = break_file(fileStr2)
#del(fileStr2)
#clean_list(fileList2)
#genNew("5514БЦ1Т1-08S_ТУ_new.ptf", fileList2) 
#       
#fileStr3 = load_file("533ie19.ptf")
#fileList3 = break_file(fileStr3)
#del(fileStr3)
#clean_list(fileList3)
#genNew("533ИЕ19_ТУ_new.ptf", fileList3)       
#       
#fileStr4 = load_file("1537ХМ2А-192_ТУ.ptf")
#fileList4 = break_file(fileStr4)
#del(fileStr4)
#clean_list(fileList4)
#genNew("1537ХМ2А-192_ТУ_new.ptf", fileList4)




