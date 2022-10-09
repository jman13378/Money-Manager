import json

from tkinter.messagebox import CANCEL, YESNO, askyesnocancel, showinfo, askyesno
from tkinter import *

from PIL import Image, ImageTk

from time import *

from playsound import playsound

from os.path import exists
import sys, os

from pathlib import Path

import os
parent_dir = os.getenv('APPDATA')
directory = "Money-Manager"
file = "data.json"
path = os.path.join(parent_dir,directory)
print(path)
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


dir_exists = os.path.exists(path)
if not dir_exists:
    os.mkdir(path)

path = os.path.join(path,file)
print(os.path.exists(path))

if not os.path.exists(path):
    with open(path, 'x') as a:
        a.write(
            '{\n'
            +'  "bal": 0,\n'
            +'  "upgradeprice": 100,\n'
            +'  "upgrades": 0,\n'
            +'  "balper": 1,\n'
            +'  "nextupprice": 50,\n'
            +'  "prestige": 0'
            +'\n}')
        a.close()


# Reading from file
f = open(path, 'r')
data = json.loads(f.read())



win=Tk()
win.geometry("350x350")
win.grid()
win.config(bg="#2C2F33")
win.title("Money Manager")

imageIcon = Image.open(resource_path('favicon.ico'))

bal = data["bal"]
upgradeprice=data["upgradeprice"]
upgrades=data["upgrades"]
balper= data["balper"]
nextupprice=data["nextupprice"]
prestige=data['prestige']

# Window icon parsing
photo = ImageTk.PhotoImage(imageIcon)
win.iconphoto(False, photo)


def addbal():
    global bal
    bal += balper
    reload_bal()
    reload_upgrades()
    print(bal)

def ending():
    global bal, upgradeprice, balper, upgrades, nextupprice
    ans = askyesnocancel("Ending!", "You have Reached the end of the game"
    + "\nClick YES to Prestige"
    + "\nClick NO to exit(will save your data)"
    + "\nClick CANCEL to restart"
    )
    if ans:
        showinfo("Prestiging!","Prestiging to: {}!".format(prestige+1))
        prestigeup()
        pass
    elif not ans:
        showinfo("Exiting!","Exiting!")
        close()
        pass
    elif ans == CANCEL:
        ans1 = askyesno("restarting!", "ARE YOU SURE YOU WANT TO RESTART")
        close()
        pass



def upgrade():
    global bal, upgradeprice, balper, upgrades, nextupprice,prestige
    if bal >= upgradeprice:
        upgrades += 1
        bal -= upgradeprice
        balper += 1 + prestige
        cost = upgradeprice
        upgradeprice += nextupprice
        if upgrades == 3:
            nextupprice = 100*prestige
        elif upgrades == 6:
            nextupprice = 150*prestige
        elif upgrades == 9:
            nextupprice = 200*prestige
        elif upgrades == 13:
            nextupprice = 300*prestige
        elif upgrades == 15:
            nextupprice = 450*prestige
        elif upgrades == 18:
            nextupprice = 600*prestige
        elif (upgrades == (20 + (10 * prestige))):
            ending()

        reload_bal()
        reload_upgrades()
        reload_upgrade_level()
        playsound(resource_path('complete.mp3'))
        showinfo("Upgraded!", "You have upgraded your MPS(Money per second)\nUpgrade: {}\nCost: {}\nRemaining Bal: {}\nNext Cost: {}".format(upgrades, cost, bal, upgradeprice) )

    else:
        playsound(resource_path('error.mp3'))
        showinfo('Not Enought Money!', "Sorry, you doen't have enough money for this!\nCurrent Bal: {}\nNeeded: {}".format(bal, upgradeprice))
        
def prestigeup():
    prestige += 1
    bal=0
    upgradeprice=150
    upgrades=0
    balper= 1+prestige
    nextupprice=50

def reload_bal():
    global bal
    balance = Label( win, text="Money: ${}".format(bal), bg="#0D1117", fg="white").grid(column=1,row=0)

def reload_upgrades():
    global upgradeprice
    upgr = Label( win, text="Upgrade Price: ${}".format(upgradeprice), bg="#0D1117", fg="white").grid(column=1,row=1)


def reload_upgrade_level():
    global upgrades
    upgrlstart = Label( win, text="Level: {}".format(upgrades), bg="#0D1117", fg="white").grid(column=2,row=1)


#scheduler = BackgroundScheduler()
#scheduler.add_job(reload_bal, 'interval', minutes=30)
#scheduler.start()


def close():
    global bal, upgradeprice, balper, upgrades, nextupprice,prestige
    a = open(path, "w")
    a.write(
        '{\n'
        +'  "bal": {},\n'.format(bal)
        +'  "upgradeprice": {},\n'.format(upgradeprice)
        +'  "upgrades": {},\n'.format(upgrades)
        +'  "balper": {},\n'.format(balper)
        +'  "nextupprice": {},\n'.format(nextupprice)
        +'  "prestige": {}'.format(prestige)
        +'\n}')
    a.close()
    win.destroy()

def restart():
    ans = askyesno("Reset Warning!", "WOULD YOU LIKE TO RESET ALL OF YOUR DATA!")
    if ans:
        global bal, upgradeprice, balper, upgrades, nextupprice, prestige
        bal=0
        prestige= 0
        upgradeprice=100
        balper=1
        upgrades=0
        nextupprice=50
        close()
    else:
        pass
reload_bal()
reload_upgrades()
reload_upgrade_level()
upgr = Button(win,text="Upgrade", command=upgrade, bg="#0D1117", fg="white").grid(column=3, row=1)

addmoney = Button(win,text="Add Money", command=addbal, bg="#0D1117", fg="white").grid(column=2, row=0)

reset = Button(win,text="Reset", command=restart, bg="#0D1117", fg="white").grid(column=5, row=0)



win.protocol('WM_DELETE_WINDOW', close)

win.mainloop()

