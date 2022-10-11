import json

from tkinter.messagebox import CANCEL, YESNO, askyesnocancel, showinfo, askyesno
from tkinter import *

from PIL import Image, ImageTk

from time import *

from playsound import playsound

from os.path import exists
import sys, os

import generators

from apscheduler.schedulers.background import BackgroundScheduler

import os

parent_dir = os.getenv('APPDATA')
directory = "Money-Manager"
file = "data.json"
path = os.path.join(parent_dir,directory)
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


generators.generator.regvars()
generators.generator.get_dir()



dir_exists = os.path.exists(path)
if not dir_exists:
    os.mkdir(path)

path = os.path.join(path,file)

if not os.path.exists(path):
    with open(path, 'x') as a:
        a.write(
            '{\n'
            +'  "bal": 0,\n'
            +'  "upgrades": 0,\n'
            +'  "balper": 1,\n'
            +'  "prestige": 0'
            +'\n}')
        a.close()


# Reading from file
f = open(path, 'r')
data = json.loads(f.read())


soundtype=1

if soundtype==0:
    completesound = resource_path('complete.mp3')
    errorsound = resource_path('error.mp3')
    imageIcon = Image.open(resource_path('favicon.ico'))
elif soundtype==1:
    completesound = 'complete.mp3'
    errorsound = 'error.mp3'
    imageIcon = Image.open('favicon.ico')


win=Tk()
win.geometry("350x350")
win.grid()
win.config(bg="#2C2F33")
win.title("Money Manager")

win.rowconfigure(5, weight=1)
win.rowconfigure(5, weight=10)
win.columnconfigure(5, weight=1)
win.columnconfigure(5, weight=10)

lel11= 0
bal = data["bal"]
upgrades=data["upgrades"]
balper= data["balper"]
prestige=data['prestige']

# Window icon parsing
photo = ImageTk.PhotoImage(imageIcon)
win.iconphoto(False, photo)

def send_stat_msg():
    showinfo("Stats!",
     'Prestige: {}\n'.format(prestige)
    +'Level: {}\n'.format(upgrades)
    +'MPC: {}\n'.format(balper)
    +'Balance: {}\n'.format(bal)
    +'Next Upgrade Price: {}\n'.format((upgrades + 1) * 100 + 50 * getPrestige())
    +'Current Upgrade Price: {}'.format(upgrades * 100 + 50 * getPrestige())
    )
def addbal():
    global bal
    bal += balper
    reload_bal()
    reload_upgrades()
    c = Label(win, text="+ ${}".format(balper), bg="#2C2F33", fg="green")
    c.grid(column=3,row=5)
    win.after(2000, lambda: c.destroy())

def ending():
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
        ans1 = askyesno("restarting!", "Are you sure you want to restart?")
        close()
        
        pass

def getPrestige():
    global prestige
    if prestige == 0:
        return 1
    else:
        return prestige

def upgrade():
    global bal, balper, upgrades, prestige
    if bal >= upgrades * 100 + 50 * getPrestige():
        cost = upgrades * 100 + 50 * getPrestige()
        bal -= upgrades * 100 + 50 * getPrestige()
        upgrades += 1
        balper += (1 + getPrestige())
        
        
        if upgrades >= (20 + (10 * getPrestige())):
            prestigeup()
        elif (upgrades == (20 + (10 * getPrestige()))):
            lel11 = 1
            ending()
            return
        
        reload_bal()
        reload_upgrades()
        reload_upgrade_level()
        playsound(completesound)
        showinfo("Upgraded!", "You have upgraded your MPC(Money per click)\nUpgrade: {}\nCost: {}\nRemaining Bal: {}\nNext Cost: {}".format(upgrades, cost, bal, upgrades * 100 + 50 * getPrestige()) )

    else:
        s = playsound(errorsound)
        showinfo('Not Enought Money!', "Sorry, you doen't have enough money for this!\nCurrent Bal: {}\nNeeded: {}".format(bal, upgrades * 100 + 50 * getPrestige()))
        
def prestigeup():
    global bal, balper, upgrades, prestige, lel11
    prestige += 1
    bal = 0
    upgrades = 0
    balper = prestige + 1
    close()

def reload_bal():
    global bal
    balance = Label( win, text="Money: ${}".format(bal), bg="#0D1117", fg="green").grid(column=0,row=0)

def reload_upgrades():
    upgr = Label( win, text="Upgrade Price: ${}".format(upgrades * 100 + 50 * getPrestige()), bg="#0D1117", fg="white").grid(column=0,row=2)

def reload_upgrade_level():
    global upgrades
    upgrlstart = Label( win, text="Level: {}".format(upgrades), bg="#0D1117", fg="white").grid(column=0,row=3)


#scheduler = BackgroundScheduler()
#scheduler.add_job(reload_bal, 'interval', minutes=30)
#scheduler.start()


def close():
    global bal, balper, upgrades, prestige
    a = open(path, "w")
    a.write(
        '{\n'
        +'  "bal": {},\n'.format(bal)
        +'  "upgrades": {},\n'.format(upgrades)
        +'  "balper": {},\n'.format(balper)
        +'  "prestige": {}'.format(prestige)
        +'\n}')
    a.close()
    generators.generator.close()
    win.destroy()

def restart():
    ans = askyesno("Reset Warning!", "Would you like to reset your data? THIS CANNOT BE UNDONE!")
    if ans:
        global bal, balper, upgrades, prestige
        bal=0
        prestige= 0
        balper=1
        upgrades=0
        close()
    else:
        pass
reload_bal()
reload_upgrades()
reload_upgrade_level()

upgr = Button(win,text="  Upgrade  ", command=upgrade, bg="#0D1117", fg="green").grid(column=1, row=3)
win.rowconfigure(5, weight=2)
stats = Button(win,text="  Stats?  ", command=send_stat_msg, bg="#0D1117", fg="yellow").grid(column=0, row=5)

addmoney = Button(win,text="  Add Money  ", command=addbal, bg="#0D1117", fg="blue").grid(column=1, row=0)

reset = Button(win,text="  Reset  ", command=restart, bg="#0D1117", fg="red").grid(column=5, row=0)



win.protocol('WM_DELETE_WINDOW', close)
def getGenerators():
    i=1
    for x in generators.generators:
        
        print(i)
        genname=generators.generator.getGeneratorName(i)
        time=generators.generator.getGeneratorInterval(i)
        baltoadd1= generators.generator.getGeneratorBalper(i)
        if baltoadd1:
            scheduler = BackgroundScheduler()
            scheduler.add_job(id=genname, trigger=lambda: genAddBal(baltoadd1), next_run_time='interval', seconds=time)
            scheduler.start()
            print("generator error due to incorrect type formatting")
        i+=1
    

def genAddBal(baltoadd):
    global bal
    bal += baltoadd
    return

win.mainloop()