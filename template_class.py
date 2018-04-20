# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:45:30 2018

@author: edino
"""

import str_work as sw

class Template(object):
    """
    represents all parameters of a program
    """
    
    def __init__(self, name):
        """
        str, programm name
        """
        self.name = name
        
    def get_name(self):
        return self.name
    
    def set_catalog(self, catalog):
        """
        str, programm catalog
        """
        self.catalog = catalog        
        
    def get_catalog(self):
        """
        string, programm catalog
        """
        return self.catalog
    
    def set_eng_name(self, name):
        """
        str, english programm name
        """
        self.eng_name = name        
        
    def get_eng_name(self):
        """
        string, english programm name
        """
        return self.eng_name
    
    def set_ver(self, ver):
        """
        str, programm version
        """
        self.ver = ver
        
    def get_ver(self):
        """
        str, programm version
        """
        return self.ver
    
    def set_date(self, date):
        """
        str, programm release date
        """
        self.date = date
        
    def get_date(self):
        """
        str, programm release date
        """
        return self.date
    
    def set_designer(self, des):
        """
        str, designer name
        """
        self.designer = des
    
    def get_designer(self):
        """
        str, designer name
        """
        return self.designer
    
    def set_tu(self, tu):
        """
        str, tu
        """
        self.tu = tu
        
    def get_tu(self):
        """
        str, tu
        """
        return self.tu
    
    def set_numpins(self, n):
        """
        str, number of pins
        """
        self.numpins = n
        
    def get_numpins(self):
        """
        str, number of pins
        """
        return self.numpins
    
    def set_fnames(self, fnames):
        """
        list of str, fk filenames
        """
        self.fnames = fnames[:]
        
    def get_fnames(self):
        """
        list of str, fk filenames
        """
        return self.fnames[:]
    
    def set_adap(self, adap):
        """
        str, allowed adapters
        """
        self.adap = adap
        
    def get_adap(self):
        """
        str, allowed adapters
        """
        return self.adap
    
    def set_ku(self, ku):
        """
        str, allowed ku-s
        """
        self.ku = ku
        
    def get_ku(self):
        """
        str, allowed ku-s
        """
        return self.ku
    
    def set_jump(self, jump):
        """
        str, positions of jumpers
        """
        self.jump = jump
        
    def get_jump(self):
        """
        str, positions of jumpers
        """
        return self.jump
    
    def set_lboard(self, board):
        """
        str, last board
        """
        self.lboard = board
        
    def get_lboard(self):
        """
        str, last board
        """
        return self.lboard
    
    def set_adap60(self, a60):
        """
        str, adap60 repin availability
        """
        self.a60 = a60
        
    def get_adap60(self):
        """
        str, adap60 repin availability
        """
        return self.a60
    
    def set_repin(self, repin):
        """
        str, need of repin
        """
        self.repin = repin
    
    def get_repin(self):
        """
        str, need of repin
        """
        return self.repin
    
    def set_pinsets(self, pins):
        """
        list of str, pin names as arrays
        """
        self.pinsets = pins[:]
        
    def get_pinsets(self):
        """
        list of str, pin names as arrays
        """
        return self.pinsets[:]
    
    def set_pingroups(self, groups):
        """
        list of str, pin groups
        """
        self.groups = groups[:]
        
    def get_pingroups(self):
        """
        list of str, pin groups
        """
        return self.groups[:]
    
    def set_blists(self, blists):
        """
        list of str, board lists
        """
        self.blists = blists[:]
        
    def get_blists(self):
        """
        list of str, board lists
        """
        return self.blists[:]
    
    def set_pinnames(self, names):
        """
        str, names of pins
        """
        self.pnames = names
        
    def get_pinnames(self):
        """
        str, names of pins
        """
        return self.pnames
    
    def set_vectors(self, vecs):
        """
        list of str, test vectors
        """
        self.vecs = vecs[:]
        
    def get_vectors(self):
        """
        list of str, test vectors
        """
        return self.vecs[:]
    
    def set_umeastime(self, time):
        """
        str, time before u measurement
        """
        self.utime = time
        
    def get_umeastime(self):
        """
        str, time before u measurement
        """
        return self.utime
    
    def set_imeastime(self, time):
        """
        str, time before i measurement
        """
        self.itime = time
        
    def get_imeastime(self):
        """
        str, time before i measurement
        """
        return self.itime
    
    def set_tin(self, tin):
        """
        list of str, time delay for times measurement
        """
        self.tin = tin[:]
        
    def get_tin(self):
        """
        list of str, time delay for times measurement
        """
        return self.tin[:]
    
    def set_ilim(self, lim):
        """
        str, current lim for power source
        """
        self.lim = lim
        
    def get_ilim(self):
        """
        str, current lim for power source
        """
        return self.lim
    
    def set_procedures(self, procs):
        """
        list of lists of str
        """
        self.procs = procs[:]
        
    def get_procedures(self):
        """
        list of lists of str
        """
        return self.procs[:]
    
    def set_vee(self, vee):
        """
        str, vee on/off
        """
        self.vee = vee
        
    def get_vee(self):
        """
        str, vee on/off
        """
        return self.vee
    
    def set_svpn2(self, svpn2):
        """
        str, active svpn number
        """
        self.svpn2 = svpn2
        
    def get_svpn2(self):
        """
        str, active svpn number
        """
        return self.svpn2
    
    def set_pwr(self, pwr):
        """
        str, power source
        """
        self.pwr = pwr
        
    def get_pwr(self):
        """
        str, power source
        """
        return self.pwr
    
    def set_gnd(self, gnd):
        """
        str, ground source
        """
        self.gnd = gnd
        
    def get_gnd(self):
        """
        str, ground source
        """
        return self.gnd
    
    def set_dcmpwr(self, pwr):
        """
        str, dcm to power source
        """
        self.dcmpwr = pwr
        
    def get_dcmpwr(self):
        """
        str, dcm to power source
        """
        return self.dcmpwr
    
    def set_dcmgnd(self, gnd):
        """
        str, dcm to ground source
        """
        self.dcmgnd = gnd
        
    def get_dcmgnd(self):
        """
        str, dcm to ground source
        """
        return self.dcmgnd
    
    def set_fk_load_i(self, fk):
        """
        list of str, fk files to load (init part)
        """
        self.fkli = fk[:]
        
    def get_fk_load_i(self):
        """
        list of str, fk files to load (init part)
        """
        return self.fkli[:]
    
    def set_tme_load_i(self, tme):
        """
        list of str, tme files to load (init part)
        """
        self.tli = tme[:]
        
    def get_tme_load_i(self):
        """
        list of str, tme files to load (init part)
        """
        return self.tli[:]
    
    def set_fk_act_i(self, fk):
        """
        list of str, fk files to activate (init part)
        """
        self.fkai = fk[:]
        
    def get_fk_act_i(self):
        """
        list of str, fk files to activate (init part)
        """
        return self.fkai[:]
    
    def set_fk_load_m(self, fk):
        """
        list of str, fk files to load (main part)
        """
        self.fklm = fk[:]
        
    def get_fk_load_m(self):
        """
        list of str, fk files to load (main part)
        """
        return self.fklm[:]
    
    def set_tme_load_m(self, tme):
        """
        list of str, tme files to load (main part)
        """
        self.tlm = tme[:]
        
    def get_tme_load_m(self):
        """
        list of str, tme files to load (main part)
        """
        return self.tlm[:]
    
    def set_fk_act_m(self, fk):
        """
        list of str, fk files to activate (main part)
        """
        self.fkam = fk[:]
        
    def get_fk_act_m(self):
        """
        list of str, fk files to activate (main part)
        """
        return self.fkam[:]

    def set_all_pins(self, ap):
        """
        str, all pins and other sets
        """
        self.allpins = ap

    def get_all_pins(self):
        """
        str, all pins and other sets
        """
        return self.allpins
    
    def set_unc_i(self, unc):
        """
        str, unconnect (init part)
        """
        self.unci = unc
        
    def get_unc_i(self):
        """
        str, unconnect (init part)
        """
        return self.unci
    
    def set_unc_m(self, unc):
        """
        str, unconnect (main part)
        """
        self.uncm = unc
        
    def get_unc_m(self):
        """
        str, unconnect (main part)
        """
        return self.uncm
    
    def set_unc_f(self, unc):
        """
        str, unconnect (fin part)
        """
        self.uncf = unc
        
    def get_unc_f(self):
        """
        str, unconnect (fin part)
        """
        return self.uncf
    
    def set_transp(self, tr):
        """
        str, transparant text
        """
        self.trans = tr
        
    def get_transp(self):
        """
        str, transparant text
        """
        return self.trans
    
    def set_contact(self, cont):
        """
        str, contact function
        """
        self.contact = cont
        
    def get_contact(self):
        """
        str, contact function
        """
        return self.contact
    
    def set_pwr_act(self, pwr):
        """
        list of str, contact function
        """
        self.pwr_act = pwr[:]
        
    def get_pwr_act(self):
        """
        list of str, contact function
        """
        return self.pwr_act[:]

    def set_tests(self, tests):
        """
        list of str, main part of program, all tests
        """
        self.tests = tests[:]

    def get_tests(self):
        """
        list of str, main part of program, all tests
        """
        return self.tests[:]
    
    def set_icc_off(self, icc):
        """
        str, icc_off at fin
        """
        self.icc = icc
        
    def get_icc_off(self):
        """
        str, icc_off at fin
        """
        return self.icc
    
    
    def gen_prog(self):
        text = []
        s = ""
        #strconst
        s = "//<strconst>"
        text.append(s)
        s = "Program " + self.get_eng_name() + ";"
        text.append(s)
        s = "Const"
        text.append(s)
        s = "  Ver       : PChar = 'Версия ПП: " + self.get_ver() + "';"
        text.append(s)
        s = "  Data      : PChar = 'Дата отладки: " + self.get_date() + "';"
        text.append(s)
        s = "  Raz       : PChar = '" + self.get_designer() + "';"
        text.append(s)
        s = "  TU        : PChar = '" + self.get_tu() + "';"
        text.append(s)
        s = "  Adap      : PChar   = '" + self.get_adap() + "';"
        text.append(s)
        s = "  KU        : PChar   = '" + self.get_ku() + "';"
        text.append(s)
        s = "  Jumper    : PChar   = '" + self.get_jump() + "';"
        text.append(s)
        s = "  LastBoard : PChar   = '" + self.get_lboard() + "';"
        text.append(s)
        s = "//<strconst>"
        text.append(s)
        
        #filenames
        s = "//<filenames>"
        text.append(s)
        s = self.get_fnames()
        for i in s:
            if i == "":
                continue
            i = i.split("€")
            i = "  " + i[0] + " : string = '" + i[1] + "';"
            text.append(i)
        s = "//<filenames>"
        text.append(s)
        
        #realconst
        s = "//<realconst>"
        text.append(s)
        s = "  NumOfPin   = " + self.get_numpins() + ";"
        text.append(s)
        s = "  ILimPwr    = " + self.get_ilim() + ";"
        text.append(s)
        s = "  TimeMeasU  = " + self.get_umeastime() + ";"
        text.append(s)
        s = "  TimeMeasI  = " + self.get_imeastime() + ";"
        text.append(s)
        s = "  ActiveSVPN : integer = " + self.get_svpn2() + ";"
        text.append(s)
        s = "//<realconst>"
        text.append(s)
        
        #tins
        s = "//<tins>"
        text.append(s)
        s = self.get_tin()
        for i in s:
            i = i.split("€")
            i = "  " + i[0] + " = " + i[1] + ";"
            text.append(i)
        s = "//<tins>"
        text.append(s)
        
        #boolconst
        s = "//<boolconst>"
        text.append(s)
        s = "  VEEON   : boolean = " + self.get_vee() + ";"
        text.append(s)
        s = "  Adap60  : boolean = " + self.get_adap60() + ";"
        text.append(s)
        s = "  NoRepin : boolean = " + self.get_repin() + ";"
        text.append(s)
        s = "//<boolconst>"
        text.append(s)
        
        #types
        s = "//<types>"
        text.append(s)
        s = "Type"
        text.append(s)
        s = "  TNamePin = Array[1..NumOfPin] of string;"
        text.append(s)
        s = "  TVectors = Array[1..NumOfPin] of integer;"
        text.append(s)
        s = "//<types>"
        text.append(s)
        
        #debugpart
        s = "//<debugpart>"
        text.append(s)
        s = "Const"
        text.append(s)
        s = "(*)"
        text.append(s)
        s = "DEBUG : boolean = true;"
        text.append(s)
        s = "(*)"
        text.append(s)
        s = "DEBUG : boolean = false;"
        text.append(s)
        s = "(**)"
        text.append(s)
        s = "//<debugpart>"
        text.append(s)
        
        #pinconfig
        s = "//<pinconfig>"
        text.append(s)
        s = "  {$I !Source\PinConfigAll.inc}"
        text.append(s)
        s = "//<pinconfig>"
        text.append(s)
        
        #pins
        s = "//<pins>"
        text.append(s)
        s = self.get_pinsets()
        for i in s:
            i = i.split("€")
            i = "  " + i[0] + " " * (13 - len(i[0])) + " : TLargeSet = [" + i[1] + "];"
            text.append(i)
        s = "//<pins>"
        text.append(s)
        
        #ping
        s = "//<ping>"
        text.append(s)
        s = self.get_pingroups()
        for i in s:
            i = i.split("€")
            temp = []
            i[1] = i[1].split(",")
            for k in range(len(i[1]) // 10):
                temp += [i[1][10 * k: 10 * (k + 1)]]
            temp += [i[1][(len(i[1]) // 10) * 10:]]
            i[1] = ""
            for l in range(len(temp)):
                if l != 0:
                    i[1] += "\n" + " " * 30
                for k in temp[l]:
                    i[1] += " " + k + ","
            i[1] = i[1][:-1] 
            del(temp)
            i = "  " + i[0] + " " * (13 - len(i[0])) + ": TLargeSet = [" + i[1] + " ];"
            text.append(i)
        s = "//<ping>"
        text.append(s)
        
        #boards
        s = "//<boards>"
        text.append(s)
        s = self.get_blists()
        for i in s:
            i = i.split("€")
            i = "  " + i[0] + " " * (13 - len(i[0])) + ": TLargeSet = [ " + i[1] + " ];"
            text.append(i)
        s = "//<boards>"
        text.append(s)
        
        #pinnames
        s = "//<pinnames>"
        text.append(s)
        s = self.get_pinnames().split(",")
        temp = []
        for k in range(len(s) // 20):
            temp += [s[20 * k : 20 * (k + 1)]]
        temp += [s[(len(s) // 20) * 20:]]
        s = "  NamePin       : TNamePin  = ("
        for l in range(len(temp)):
            if l != 0:
                s += "\n" + " " * 30
            for k in temp[l]:
                s += " " + k + ","
        del(temp)
        s = s[:-1] + ");"
        text.append(s)
        s = "//<pinnames>"
        text.append(s)
        
        #vectors
        s = "//<vectors>"
        text.append(s)
        s = self.get_vectors()
        for i in s:
            if i == "":
                continue
            i = i.split("€")
            temp = []
            i[1] = i[1].split(",")
            for k in range(len(i[1]) // 16):
                temp += [i[1][16 * k: 16 * (k + 1)]]
            temp += [i[1][(len(i[1]) // 16) * 16:]]
            i[1] = ""
            for l in range(len(temp)):
                if l != 0:
                    i[1] += "\n" + " " * 30
                for k in temp[l]:
                    i[1] += " " + k + ","
            i[1] = i[1][:-1] 
            del(temp)
            i = "  " + i[0] + " " * (13 - len(i[0])) + ": TVectors  = (" + i[1] + " );"
            text.append(i)
        s = "//<vectors>"
        text.append(s)
        
        #source
        s = "//<source>"
        text.append(s)
        s = "  {$I !Source\Testes_dll.inc}"
        text.append(s)
        s = "//<source>"
        text.append(s)
        
        #addproc
        s = "//<addproc>"
        text.append(s)
        s = self.get_procedures()
        for i in s:
            if i.replace(" ", "")[:2] != "//":
                text.append(i)
        s = "//<addproc>"
        text.append(s)
        
        #initpart
        s = "//<initpart>"
        text.append(s)
        s = "INITIALIZATION"
        text.append(s)
        s = "  PinChangeDll();"
        text.append(s)
        s = "  if DeviceNotReady = false then"
        text.append(s)
        s = "    begin"
        text.append(s)
        
        #allpins
        s = "//<allpins>"
        text.append(s)
        s = " " * 6 + "AllPins  := " + self.get_all_pins() + ";"
        text.append(s)
        s = "//<allpins>"
        text.append(s)
        
        #unconnecti
        s = "//<unconnecti>"
        text.append(s)
        s = " " * 6 + "UnConnectAlll(" + self.get_unc_i() + ");"
        text.append(s)
        s = "//<unconnecti>"
        text.append(s)
        
        #loadfilesi
        s = "//<loadfilesi>"
        text.append(s)
        s = self.get_fk_load_i()
        if s[0] != "":
            for i in s:
                i = i.split(",")
                i = " " * 6 + "LoadFKFile(" + i[0] + ", " + i[1] + ");"
                i += "\n" + " " * 6 + "DelayMS(TimeUSB);"
                text.append(i)
        s = self.get_tme_load_i()
        if s[0] != "":
            for i in s:
                i = i.split(",")
                i = " " * 6 + "Time_to_FKRec(" + i[0] + ", " + i[1] + ");"
                i += "\n" + " " * 6 + "DelayMS(TimeUSB);"
                text.append(i)
        s = self.get_fk_act_i()
        if s[0] != "":
            for i in s:
                i = i.split(",")
                i = " " * 6 + "ActivateFileFK(" + i[0] + ", " + i[1] + ");"
                i += "\n" + " " * 6 + "DelayMS(TimeUSB);"
                text.append(i)
        s = "//<loadfilesi>"
        text.append(s)
        
        s = " " * 6 + "Initialise(FileName, Ver, Data, Raz, GetTesterNumber, IMSNumber);"
        text.append(s)
        s = " " * 4 + "end;"
        text.append(s)
        
        #transp
        s = "//<transpi>"
        text.append(s)
        s = "  Transparant ('" + self.get_transp() + "');"
        text.append(s)
        s = "//<transpi>"
        text.append(s)
        
        s = "//<initpart>"
        text.append(s)
        
        #mainpart
        s = "//<mainpart>"
        text.append(s)
        s = "MEASBEGIN"
        text.append(s)
        #transp
        s = "//<transpm>"
        text.append(s)
        s = "  Transparant ('" + self.get_transp() + "');"
        text.append(s)
        s = "//<transpm>"
        text.append(s)
        
        s = "  StartMeasTime;"
        text.append(s)
        s = "  if DeviceNotReady then GoTo ProgrammBrake;"
        text.append(s)
        s = "  TestNumber := 0;"
        text.append(s)
        s = "  Header(FileName, IMSNumber, DEBUG);"
        text.append(s)
        s = "  ActivateSVPN(ActiveSVPN);"
        text.append(s)
        s = "  DelayMS(TimeUSB);"
        text.append(s)
        s = "  ConnPins := InPins;"
        text.append(s)
        
        #addconst
        s = "//<addconst>"
        text.append(s)
        s = " " * 2 + "PWR := " + self.get_pwr() + ";"
        text.append(s)
        s = " " * 2 + "GND := " + self.get_gnd() + ";"
        text.append(s)
        s = " " * 2 + "ComDCMPWr := " + self.get_dcmpwr() + ";"
        text.append(s)
        s = " " * 2 + "ComDCMGND := " + self.get_dcmgnd() + ";"
        text.append(s)
        s = "//<addconst>"
        text.append(s)
        
        #unconnectm
        s = "//<unconnectm>"
        text.append(s)
        s = " " * 2 + "UnConnectAlll(" + self.get_unc_m() + ");"
        text.append(s)
        s = "//<unconnectm>"
        text.append(s)
        
        #loadfilesi
        s = "//<loadfilesm>"
        text.append(s)
        s = self.get_fk_load_m()
        if s[0] != "":
            for i in s:
                i = i.split(",")
                i = " " * 2 + "LoadFKFile(" + i[0] + ", " + i[1] + ");"
                i += "\n" + " " * 2 + "DelayMS(TimeUSB);"
                text.append(i)
        s = self.get_tme_load_m()
        if s[0] != "":
            for i in s:
                i = i.split(",")
                i = " " * 2 + "Time_to_FKRec(" + i[0] + ", " + i[1] + ");"
                i += "\n" + " " * 2 + "DelayMS(TimeUSB);"
            text.append(i)
        s = self.get_fk_act_m()
        if s[0] != "":
            for i in s:
                i = i.split(",")
                i = " " * 2 + "ActivateFileFK(" + i[0] + ", " + i[1] + ");"
                i += "\n" + " " * 2 + "DelayMS(TimeUSB);"
                text.append(i)
        s = "//<loadfilesm>"
        text.append(s)
        
        #contact
        s = "//<contact>"
        text.append(s)
        s = "  if VEEON = true then"
        text.append(s)
        s = "    SetPower(GND, Ugnd_0, IlimPwr, Source_On);"
        text.append(s)
        s = "  else"
        text.append(s)
        s = "    SetPower(GND, Ugnd_0, IlimPwr, Source_Off);"
        text.append(s)
        if self.get_contact() != "":
            s = "  contact(" + self.get_contact() + ");"
            text.append(s)
        s = "//<contact>"
        text.append(s)
        
        #pwrson
        s = "//<pwrson>"
        text.append(s)
        s = self.get_pwr_act()
        for i in s:
            i = "  SetPower(" + i + ");"
            text.append(i)
        s = "  DelayMS(TimeUSB);"
        text.append(s)
        s = "//<pwrson>"
        text.append(s)
        
        #funcspart
        s = "//<funcspart>"
        text.append(s)
        s = self.get_tests()
        for i in s:
            text.append(i)
        s = "//<funcspart>"
        text.append(s)
        
        s = "  ProgrammBrake:"
        text.append(s)
        s = "//<mainpart>"
        text.append(s)
        
        #finalpart
        s = "//<finalpart>"
        text.append(s)
        s = "FINALIZATION"
        text.append(s)
        
        #iccoff
        s = "//<iccoff>"
        text.append(s)
        if self.get_icc_off() != "":
            s = "  " + self.get_icc_off() + ";"
            text.append(s)
        s = "//<iccoff>"
        text.append(s)
        
        #unconnectf
        s = "//<unconnectf>"
        text.append(s)
        s = " " * 2 + "UnConnectAlll(" + self.get_unc_f() + ");"
        text.append(s)
        s = "//<unconnectf>"
        text.append(s)
        
        s = "  MeasTime := MeasTimeMks;"
        text.append(s)
        s = "  RaportPrint(MeasTime/1000000);"
        text.append(s)
        s = "END."
        text.append(s)
        s = "//<finalpart>"
        text.append(s)
        
        with open(self.get_catalog() + self.get_name() + "_new.ptf", "w") as f:
            for s in text:
                f.write(s + "\n")
#                print(s)
        
def set_var(templ, func, var):
    for i in range(len(func)):
        func[i](templ, var[i])
        
def init_templ(fName, log, catalog = ""):
    name = fName.split("/")[-1]
    if catalog == "":
        catalog = fName[:-len(name)]
    name = name[:name.find("_templ")]
    templ = Template(name)
    with open(fName + ".ptf", "r") as f:
        pText = f.read().split("\n")
    
    
    templ.set_ver("2.0")
    templ.set_catalog(catalog)
    templ.set_svpn2("1")
    #str const
    currPart = sw.get_text_part(pText, "//<strconst>", log)
    
    #default values
    if currPart[1] == "":
        import datetime
        currPart[1] = datetime.date.today().strftime("%d.%m.%y")
    if currPart[2] == "":
        currPart[2] = "Virtual programmer"
    if currPart[3] == "" and templ.name[:4] == "5514":
        currPart[3] = "АЕЯР.431260.179 ТУ коррекция 13"
        
    func = [Template.set_eng_name, Template.set_date, Template.set_designer, Template.set_tu, Template.set_adap, Template.set_ku, Template.set_jump, Template.set_lboard]
    set_var(templ, func, currPart)
    
    #filenames
    currPart = sw.get_text_part(pText, "//<filenames>", log)
    templ.set_fnames(currPart)
    
    #real const
    currPart = sw.get_text_part(pText, "//<realvars>", log)
    
    #default values
    if currPart[1] == "":
        currPart[1] = "0.1"
    if currPart[2] == "":
        currPart[2] = "20"
    if currPart[3] == "":
        currPart[3] = "50"
    
    func = [Template.set_numpins, Template.set_ilim, Template.set_umeastime, Template.set_imeastime]
    set_var(templ, func, currPart)
    
    #tins
    currPart = sw.get_text_part(pText, "//<tins>", log)
    if currPart == "":
        currPart = "Tin€10.0"
    templ.set_tin(currPart)
    
    #bool constants
    currPart = sw.get_text_part(pText, "//<boolconst>", log)
    if currPart[1] == "":
        currPart[1] = "False"
    func = [Template.set_vee, Template.set_adap60, Template.set_repin]
    set_var(templ, func, currPart)
    
    #additional constants
    currPart = sw.get_text_part(pText, "//<addconst>", log)
    
    #default values
    if currPart[0] == "":
        currPart[0] = "pVCC"
    if currPart[1] == "":
        currPart[1] = "pVEE"
    if currPart[2] == "":
        currPart[2] = "DCM_To_VCC"
    if currPart[3] == "":
        currPart[3] = "DCM_To_VCC"
        
    func = [Template.set_pwr, Template.set_gnd, Template.set_dcmpwr, Template.set_dcmgnd]
    set_var(templ, func, currPart)

    #pin sets
    currPart = sw.get_text_part(pText, "//<pins>", log)
    templ.set_pinsets(currPart)
    
    #pin_groups
    currPart = sw.get_text_part(pText, "//<ping>", log)
    templ.set_pingroups(currPart)
    
    #board lists
    currPart = sw.get_text_part(pText, "//<boards>", log)
    templ.set_blists(currPart)
    
    #pin names list
    currPart = sw.get_text_part(pText, "//<pinnames>", log)
    templ.set_pinnames(currPart[0])
    
    #vectors
    currPart = sw.get_text_part(pText, "//<vectors>", log)
    templ.set_vectors(currPart)
    
    #additional procedures
    currPart = sw.get_text_part(pText, "//<addproc>", log)
    templ.set_procedures(currPart)
    
    #fk load and activate (init part)
    currPart = sw.get_text_part(pText, "//<loadfki>", log)
    templ.set_fk_load_i(currPart)
    currPart = sw.get_text_part(pText, "//<loadtmei>", log)
    templ.set_tme_load_i(currPart)
    currPart = sw.get_text_part(pText, "//<activatefki>", log)
    templ.set_fk_act_i(currPart)
    
    #all pins init
    currPart = sw.get_text_part(pText, "//<allpins>", log)
    if currPart[0] == "":
        currPart[0] = "InPins + OutPins"
    templ.set_all_pins(currPart[0])
    
    #unconnect (init part)
    currPart = sw.get_text_part(pText, "//<unconnecti>", log)
    if currPart[0] == "":
        currPart[0] = "0, 0"
    templ.set_unc_i(currPart[0])
    
    #transparant
    currPart = sw.get_text_part(pText, "//<transp>", log)
    if currPart[0] == "":
        currPart[0] = templ.get_name() + " " + templ.get_ku()
    templ.set_transp(currPart[0])
    
    #unconnect (main part)
    currPart = sw.get_text_part(pText, "//<unconnectm>", log)
    if currPart[0] == "":
        currPart[0] = "0, 0"
    templ.set_unc_m(currPart[0])
    
    #fk load and activate (main part)
    currPart = sw.get_text_part(pText, "//<loadfkm>", log)
    templ.set_fk_load_m(currPart)
    currPart = sw.get_text_part(pText, "//<loadtmem>", log)
    templ.set_tme_load_m(currPart)
    currPart = sw.get_text_part(pText, "//<activatefkm>", log)
    templ.set_fk_act_m(currPart)
    
    #contact
    currPart = sw.get_text_part(pText, "//<contact>", log)
    templ.set_contact(currPart[0])
    
    #pwr sources activation
    currPart = sw.get_text_part(pText, "//<pwrson>", log)
    temp = []
    for s in currPart:
        if(s.split(",")[0].lower() == "gnd"):
            continue
        temp.append(s)
    currPart = temp
    del(temp)
    templ.set_pwr_act(currPart)
    
    #main part with functions
    currPart = sw.get_text_part(pText, "//<funcspart>", log)
    templ.set_tests(currPart)
    
    #icc_off at fin
    currPart = sw.get_text_part(pText, "//<iccoff>", log)
    if currPart[0] == "":
        currPart[0] = "ICC_off"
    templ.set_icc_off(currPart[0])
    
    #unconnect (fin part)
    currPart = sw.get_text_part(pText, "//<unconnectf>", log)
    if currPart[0] == "":
        currPart[0] = "0, 0"
    templ.set_unc_f(currPart[0])
    
    return templ
#
log = open("log.txt", "w")
 templ = init_templ("D:/_python/ims/transform/1564ИД7_ТУ_templ", log)
templ.gen_prog()
log.close()