

import logging
import os
import json
from PIL import Image, ImageTk
from tkinter.messagebox import CANCEL, YESNO, askyesnocancel, showinfo, askyesno
from tkinter import *

class generator():
    totalgens=0

    def regvars():
        global parent_dir, directory, file, path
        parent_dir = os.getenv('APPDATA')
        directory = "Money-Manager"
        file = "generators-data.json"
        path = os.path.join(parent_dir,directory)

    def get_dir():
        global parent_dir, directory, file, path, generators
        

        dir_exists = os.path.exists(path)
        if not dir_exists:
            os.mkdir(path)

        path = os.path.join(path,file)

        if not os.path.exists(path):
            with open(path, 'x') as a:
                a.write(
                    '{\n'
                    +'  "generators": [{\n'
                    +'  }]'
                    +'\n}')
                print(a.read)
                a.close()
        f= open(path, 'r') 
        rip = json.loads(f.read())
        generators = rip["generators"][0]
        f.close()
        print(str(generators) + "1")

    def getGeneratorInterval(genid):
        ri = generators["{}".format(genid)]["interval"]
        rit = generators["{}".format(genid)]["intervalType"]
        print(str(rit) + "  " + str(ri))
        if "tf" in str(rit): # mi
            return ri * 60
        elif "hj" in str(rit): # se
            return ri
        elif "lk" in str(rit): # hr
            return ri * 3600
        else:
            return False
    def getGeneratorName(genid):
        return generators["{}".format(genid)]["name"]

    def getGeneratorBalper(genid):
        return generators["{}".format(genid)]["balper"]
    def resetgens():
            
        a = open(path, "w")
        sda = str(generators).replace("'","\"")
        a.write(
            '{\n'
            +'  "generators": [{}'.format(sda)
            +']\n}')
        a.close()
        pass
    def close():
        
        a = open(path, "w")
        sda = str(generators).replace("'","\"")
        a.write(
            '{\n'
            +'  "generators": [{}'.format(sda)
            +']\n}')
        
        a.close()
        d = open(path, "r")
        print(d.read())
        pass
    def addGen(genid,nam,balper,interval,intervalType):
        a = open(path, "w")
        sda = str(generators).replace("'","\"")
        llol = str(
            '"{}"'.format(str(genid))
            +':'
            + '{'+'"name": "{}"'.format(str(nam))
            +', "balper":'
            + format(str(balper))
            +', "interval":' +str(interval)
            +', "intervalType": "{}"'.format(str(intervalType))+"}}").replace("'","\"")
        a.write(
            '{\n'
            +'  "generators": [{},{}'.format(sda[:-1],llol)
            +']\n}')
        
        a.close()
        d = open(path, "r")
        print(d.read())
        pass
    def upgradegen(i1):
        generators["{}".format(str(i))]
        print(generator.getGeneratorName(i))
        i = 1
        for x in generators:
            if i1 is generator.getGeneratorName(i):
                pass
            else: pass


