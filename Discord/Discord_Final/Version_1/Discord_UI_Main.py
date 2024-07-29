import os

from tkinter import Tk,ttk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu,messagebox
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename
import tkinter as tk

import Discord_Bot_Main as Bot
import Discord_Funcs as funcs

import time
from datetime import datetime
import Const_Final as Const

import Bot_Data
from Bot_Data import DataType
from Bot_Data import DataFromBot as Data_B

import threading



root = Tk()

windowWidth = 1000
windowHeight = 800

root.geometry(f"{windowWidth}x{windowHeight}+100+100")

currentProgress = None

#-----------UI---------------HEADER
button_bot = Button(root,text="激活BOT",command=lambda: activateBot())
button_bot.pack()
button = Button(root,text="获取prompts",command=lambda: fetchPrompts())
button.pack()
button2 = Button(root,text="配置图片保存路径",command=lambda: configFilePath())
button2.pack()
button3 = Button(root,text="配置角色",command=lambda: configCharacter())
button3.pack()
progressLabel = Label(root,text="progress",bg='lightblue')
#progressLabel.pack(side='bottom')

options = ["正在获取..."]
selected_value = StringVar(root)
selected_value.set(options[0])

button4 = Button(root,text="开始生成",command=lambda: beginDraw())
button4.pack()

#-----------------------------------MAIN UI
def on_canvas_configure(event):
    bg_canvas.configure(scrollregion=bg_canvas.bbox("all"))

def on_frame_configure(event):
    bg_canvas.configure(scrollregion=bg_canvas.bbox("all"))

bg_canvas = Canvas(root,bg='lightblue')
bg_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, command=bg_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

frame = tk.Frame(bg_canvas,bg='lightyellow')
frame_id = bg_canvas.create_window((0, 0), window=frame, anchor='nw')
frame.bind("<Configure>", on_frame_configure)
bg_canvas.bind("<Configure>", on_canvas_configure)

def on_mousewheel(event):
    unit = int(-1*(event.delta/120))
    bg_canvas.yview_scroll(unit, "units")

bg_canvas.config(yscrollcommand=scrollbar.set)
bg_canvas.config(scrollregion=bg_canvas.bbox("all"))
bg_canvas.bind_all("<MouseWheel>", on_mousewheel)


#----------------GLOBAL VARS-----------
index = 0
prompts_temp = []
g_progress = 0

prompts_filepath = ""
character_filepath = ""
ImageStorePath = ""
session_id = ""

Lines = []
progrssbars = []
ImageCanvas = []
imageData = None

#-------------------FUNS-----------------------
#----------UI FUNCS----------------------

def createMainLine(prompt):
    space = Canvas(frame,width=windowWidth,height=200,bg='lightgreen')
    space.pack()

    forceCanvasSize(space,windowWidth,200)

    adddetails(prompt,space)

    global Lines
    Lines.append(space)

def adddetails(prompt,canvas):
    promptLabel = createLine(prompt,canvas)
    promptLabel.pack(side='left')

    progress = createProgressLine(canvas)
    progress.pack(side='left')

    image = createImageLine(canvas)
    image.pack(side='left')

def createLine(text,canvas):
    space = Canvas(canvas,width=450,height=200,bg='lightyellow')
    forceCanvasSize(space,450,200)

    promptLabel = Label(space,width=50,height=10,font=('Arial', 10),text=text,justify="left",wraplength=150,fg='red',relief=tk.RAISED, borderwidth=2)
    promptLabel.pack(side='left')

    return space

def createProgressLine(canvas):
    global progrssbars
    progress = Canvas(canvas,width=150,height=200,bg='lightblue')
    forceCanvasSize(progress,150,200)

    progress_bar = ttk.Progressbar(progress,mode="determinate",maximum=100,value=13)
    progress_bar.pack(pady=5)
    progrssbars.append(progress_bar)
    return progress

def createImageLine(canvas):

    global ImageCanvas
    Image = Canvas(canvas,width=400,height=200,bg='lightblue')
    forceCanvasSize(Image,400,200)
    
    ImageCanvas.append(Image)
    return Image

def forceCanvasSize(canvas,width,height):
    top = Canvas(canvas,width=width,height=1)
    top.pack(side='top')

    bottom = Canvas(canvas,width=1,height=height)
    bottom.pack(side='left')

#----------EVENT FUNCS----------------------
def activateBot():
    Const.log("激活Bot")
    Bot.on_button_click(rootAfterCallBack,sessionidFetchCallback)

def fetchPrompts():
    Const.log("FETCH PROMPTS") 
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if folder_path:
        print("选中的文件夹路径:", folder_path)
        #funcs.configPromptFilePath(folder_path)
        global prompts_filepath
        prompts_filepath = folder_path

        bool_prompt = os.path.exists(folder_path) and folder_path.endswith('.txt')
        print(f"{bool_prompt}")
        if bool_prompt:
            with open(folder_path,'r',encoding='UTF-8') as file:
                content = file.read()
                print("content = " + content)
                prompts = content.split('\n')

                for index,prompt in enumerate(prompts):
                    Const.log("LOOP PROMPTS")
                    createMainLine(prompt)

def configCharacter():
    Const.log("FETCH CHAACTER~~~") 
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    funcs.fetchCharacterFilePath(folder_path)

def configFilePath():
    Const.log("CONFIG IMAGE SAVE PATH") 
    folder_path = filedialog.askdirectory()
    if folder_path:
        print("选中的文件夹路径:", folder_path)
    funcs.configImageSavePath(folder_path)

def beginDraw():
    Const.log("BEGIN DRAW") 

    params = {
    "type" : 2,
    "application_id" : "936929561302675456",
    "guild_id" : "1255422192695509072",
    "channel_id": "1255422193249030236",
    "session_id" : "402ed12483da296b9020268bafe3b8ac",
    "data" : {
        "version" : "1237876415471554623",
        "id" : "938956540159881230",
        "name" : "imagine",
        "type" : 1,
        "options" : [{"type" : 3,
                      "name" : "prompt",
                      "value" : "The nemesis arrives, and Yu Rang swiftly acts, delivering a lethal strike that fulfills his revenge.",
                      "attachments" : []
                       }]

    }
}
    global session_id
    if session_id == "":
        Const.log("EMPTY SESSIONID")
    else:
        origin = params['session_id']
        Const.log(f"replace {origin} with new session :{session_id}")
        params['session_id'] = session_id    
        funcs.beginDraw(params,drawCallBack)

#----------CALLBACK-----------
def activateBotCallback(success,sessionId):
    if success:
        global session_id
        session_id = sessionId
        Const.log(f"BOT Login Success with sessionid : {session_id}")
        button_bot.config(text="已激活")

def sessionidFetchCallback(sessionId):
    global session_id
    session_id = sessionId
    Const.log(f"BOT Login Success with sessionid : {session_id}")
    button_bot.config(text="已激活")

def drawCallBack(progress):
    Const.log(f"PROGRESS = {str(progress)}")
        

def rootAfterCallBack():
    root.after(500,BotDoCheck)

def BotDoCheck():
    Bot.check_queue(rootAfterCallBack)


root.mainloop()