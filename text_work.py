# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 16:19:20 2018

@author: User
"""

import str_work as sw

def del_comments(pText, log = 0):
    ret = []
    ret = sw.get_text_part(pText, "(****", log, "****)")
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

def get_procedure(pText, i):
    import string
    if pText[i].find("(") != -1:
        ch = "("
    else:
        ch = ";"
    name = sw.get_quote(pText[i], "", 0, ch, 0).lower()
    name = name.replace("procedure", "")
    name = name.replace("function", "")
    name = name.replace(" ", "")
    name = name.replace("\t", "")
    
    s = pText[i].replace(" ", "").replace("\t","").lower()
    while s[:5] != "begin":
        i += 1
        s = pText[i].replace(" ", "").replace("\t","").lower()
    
    n = 1
    
    while n != 0:
        i += 1
        s = pText[i].replace(" ", "").replace("\t","").lower()
        if s.find("begin") != -1:
            if s.find("begin") == 0 or not s[s.find("begin") - 1] in string.ascii_lowercase:
                n += 1
                print(n)
        if s.find("end") != -1:
            if s.find("end") == 0 or not s[s.find("end") - 1] in string.ascii_lowercase:
                n -= 1
                print(n)
            
    
    return i, name