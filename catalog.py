# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 11:27:56 2018

@author: edino
"""

import os
import text_work as tw

#import templ_gen
#import templ_gen_some_new
#import template_class

def catalog_gen_templs():
    directory = "C:/_python/ims/transform/test/5514"
    catalog = "C:/_python/ims/transform/test/new/"
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
                    templ_gen.templ_gen(fName, catalog, log)
                else:
                    templ_gen_some_new.templ_gen(fName, catalog, log)
    log.close()
    
def catalog_gen_progs():
    directory = "C:/_python/ims/transform/test/new"
    catalog = "C:/_python/ims/transform/test/gen_progs/"
    files = os.listdir(directory)
    log = open(catalog + "log.txt", "w")
    tree = os.walk(directory)
    for d in tree:
        path = d[0] + "/"
        for f in d[2]:
            if f.find("_templ") == -1:
                continue
            fName = path + f
            f = f.split("/")[-1]
            if f[-3:] != "ptf":
                continue
            else:
                fName = fName[:-4]
                log.write(fName + "\n")
                templ = template_class.init_templ(fName, log, catalog)
                templ.gen_prog()
#    
#catalog_gen_templs()
#catalog_gen_progs()
 
               
def get_ptf_stat(fName, dic):
    with open(fName, "r") as f:
        text = f.read().split("\n")
    
    text = tw.clean_text(text)
    text = tw.del_comments(text)
    for i in range(len(text)):
        s = text[i].lower()
        if s.find("procedure") != -1 or s.find("function") != -1:
            s = s[:s.find("(")].replace(" ", "")
            s = s.lower().replace("procedure", "")
            s = s.replace("function", "")
            dic[s] = dic.get(s, 0) + 1

                
def catalog_test_files():
    directory = "D:/_python/ims/transform/test/5514"
    catalog = "D:/_python/ims/transform/test/new/"
    files = os.listdir(directory)
    log = open(catalog + "log.txt", "w")
    #print(files)
    tree = os.walk(directory)
    ext = {}
    incs = {}
    statDic = {}
    for d in tree:
        path = d[0] + "/"
        for f in d[2]:
            fName = path + f
            f = f.split("/")[-1]
            if f[-3:] == "ptf" or f[-3:] == "inc":
                get_ptf_stat(fName, statDic)
            if f[-3:] == "inc":
                incs[f] = incs.get(f, 0) + 1
            f = f[-1::-1]
            f = f[:f.index(".")][-1::-1].lower()
            ext[f] = ext.get(f, 0) + 1
    log.write("File extensions: " + str(len(ext.keys())) + "\n")
    for i in ext.keys():
        log.write(i + ": " + str(ext[i]) + "\n")
    log.write("\nInclude files: " + str(len(incs.keys())) + "\n")
    for i in sorted(incs.keys()):
        log.write(i + ": " + str(incs[i]) + "\n")
    log.write("\nUsed functions and procedures: " + str(len(statDic.keys())) + "\n")
    for i in sorted(statDic.keys()):
        log.write(i + ": " + str(statDic[i]) + "\n")
    log.close()
    
catalog_test_files()