import os

from tkinter import Tk,ttk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu,messagebox
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename
import tkinter as tk

import Test_Const as Const
import BotTest as Bot

root = Tk()

windowWidth = 1000
windowHeight = 800

root.geometry(f"{windowWidth}x{windowHeight}+100+100")

button_bot = Button(root,text="激活BOT",command=lambda: activateBot())
button_bot.pack()

button_bot2 = Button(root,text="测试主线程",command=lambda: testMainProcess())
button_bot2.pack()

def activateBot():
    Const.log("ACTIVATE")
    Bot.Login(BotLoginCallback)

def testMainProcess():
    Const.log("123")

def BotLoginCallback(sessionid):
    Const.log(f"SESSION_ID = {sessionid}")
    

root.mainloop()

