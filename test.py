# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 11:47:00 2018

@author: edino
"""
from templ_gen_some_new import *
import os

def test_gen(fName, catalog, log):
    with open(fName + ".ptf", "r") as f:
        pText = f.read()
        fName = fName.split("/")[-1]
#        f2 = open(catalog + fName + "_old.ptf", "w")
#        f2.write(pText)            
#        f2.close()
    
    pText = pText.split("\n")
    pText = clean_text(pText)
    pText = del_comments(pText, log)
#    pText = replace_smth(pText, log, "SecondLevelOn", replace_second_level, "ConfChnlN", True)
    pText = replace_smth(pText, log, "UO(", replace_uo, "UO", True)
#    pText = replace_smth(pText, log, "ILI(", replace_ili, "ILI")
#    pText = replace_smth(pText, log, "IO(", replace_ili, "ILI")
#    pText = replace_smth(pText, log, "I0S(", replace_ios, "IOS")
#    pText = replace_smth(pText, log, "TP(", replace_tp, "TP")
#    pText = replace_smth(pText, log, "UpDown(", replace_updown, "UpDown")

directory = "P:/_python/ims/transform/test/5514"
catalog = "P:/_python/ims/transform/test/new/"
files = os.listdir(directory)
log = open(catalog + "log.txt", "w")
    #print(files)
tree = os.walk(directory)
for d in tree:
    path = d[0] + "/"
    for f in d[2]:
        fName = path + f
        f = f.split("/")[-1]
        if f[-3:] != "ptf":
            continue
        else:
            fName = fName[:-4]
            log.write(fName + "\n")
            with open(fName + ".ptf", "r") as temp:
                t = temp.read().split("\n")
            if t[0] == "//<Heаd>":
                test_gen(fName, catalog, log)
            else:
                test_gen(fName, catalog, log)
log.close()