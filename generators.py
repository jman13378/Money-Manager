
import os
import json
from PIL import Image, ImageTk
from tkinter.messagebox import CANCEL, YESNO, askyesnocancel, showinfo, askyesno
from tkinter import *

class generator():
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

        pth = os.path.join(path,file)
        print(os.path.exists(pth))

        if not os.path.exists(pth):
            with open(path, 'x') as a:
                a.write(
                    '{\n'
                    +'  "generators": [{\n'
                    +'      "1": [{\n'
                    +'          "name": "starter",\n'
                    +'          "balper": 50,\n'
                    +'          "interval": "1mi"\n'
                    +'      }]\n'
                    +'  }]'
                    +'\n}')
                print(a.read)
                a.close()
        f= open(pth, 'r') 
        rip = json.loads(f.read())
        generators = rip["generators"]
        f.close()
        print(generators)

    def getGeneratorInterval():
        global path
        if not os.path.exists(path):
            import mlibs
            mlibs.close()
        pass
    def getGeneratorName():
        pass
    def getGeneratorBalper():
        return
    def getGenerators():

        pass
    def close():
        
        pth = os.path.join(path,file)
        a = open(pth, "w")
        a.write(
            '{\n'
            +'  "generators": {\n'+'{}'.format(generators)
            +'}\n}')
        a.close()
        pass