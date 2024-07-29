import os

from tkinter import Tk,ttk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu,messagebox
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename
import tkinter as tk

import Discord_Bot_Main_0708 as Bot
import Discord_Funcs_0708 as funcs

import time
from datetime import datetime
import Const_Final_0708 as Const

import Bot_Data_0708
from Bot_Data_0708 import DataType
from Bot_Data_0708 import DataFromBot as Data_B
from Bot_Data_0708 import CustomIdObject
from Bot_Data_0708 import ImageUrlObject

import threading
import json
import random
from PIL import Image, ImageTk

import Discord_Email as Email
import Discord_ViviaRequest_0727 as Vivia
from glob import glob

import Discord_VedioCombine as Combine
from datetime import datetime

root = Tk()

windowWidth = 1000
windowHeight = 800

root.geometry(f"{windowWidth}x{windowHeight}+600+50")

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
button5 = Button(root,text="生成视频",command=lambda: combine2Video())
button5.pack()
button6 = Button(root,text="测试token",command=lambda: testviviaLink())
button6.pack()
text = tk.Entry(root,width=80)
text.pack()
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
    #print(str(unit))
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

Image2Video_index = 0
Image2Video_ifolder_path = ""

Lines = []
progrssbars = []
ImageCanvas = []
imageData = None
imageDataDic = {}
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
    #testImageReplace()
    #return
    Bot.on_button_click(rootAfterCallBack,sessionidFetchCallback)

def fetchPrompts():
    Const.log("FETCH PROMPTS") 
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if folder_path:
        print("选中的文件夹路径:", folder_path)
        funcs.configPromptFilePath(folder_path)
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
                    prompt_index = '1.  ' + prompt
                    createMainLine(prompt_index)

def configCharacter():
    Const.log("FETCH CHAACTER~~~") 
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    funcs.fetchCharacterFilePath(folder_path)

def configFilePath():
    Const.log("CONFIG IMAGE SAVE PATH") 
    folder_path = filedialog.askdirectory()

    global ImageStorePath

    if folder_path:
        print("选中的文件夹路径:", folder_path)
        ImageStorePath = folder_path
        path = ImageStorePath + '/Videos'
        Vivia.configDownloadPath(path)

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
        funcs.beginDraw(params,drawCallBack,fetchCustomIDCallback,imagesDownloadCallback)
        Bot.check_queue(rootAfterCallBack)
#----------Image2Video---------------------
def testviviaLink():
    cookie = text.get()
    Vivia.cookie_g = cookie

    if Vivia.cookie_g == "":
        print("CONFIG COOKIE FIRST")
        return
    Vivia.doEventRequest(viviaCallBack)


def viviaCallBack(code):
    print(f"VIVIA CALLBACK with code : {code}")
    if code == 200:
        button4.config(state=tk.NORMAL)
    else:
        button4.config(text='TOKEN FAIL')
        button4.config(state=tk.DISABLED)
    

def combine2Video():
    global ImageStorePath
    videopath = ImageStorePath + '/Videos'
    root.after(3000,lambda:rootAfterCombine(videopath))

def createVideos():

    cookie = text.get()
    Vivia.cookie_g = cookie

    print("CREATE VIDEOS")
    if Vivia.downloadTargetPath == "":
        print("CONFIG DOWNLOAD TARGETPATH FIRST")
        return
    elif Vivia.cookie_g == "":
        print("CONFIG COOKIE FIRST")
        return
    else:
        global Image2Video_index
        global ImageStorePath
        if ImageStorePath:
            path = ImageStorePath + '/Downloads'
            print(f"PATH = {path},index = {Image2Video_index}")
            jpg_files = glob(os.path.join(path, '*.jpg'))
            print(f"JPGS = {str(len(jpg_files))}")
            
            if Image2Video_index < len(jpg_files):
                path_c = jpg_files[Image2Video_index]
                print(f"START WITH IMAGE : {path_c}")
                Vivia.beginWithImage(path_c,rootAfterCallBack_v,finishCalback)
            else:
                print('Finish')
                videopath = ImageStorePath + '/Videos'
                root.after(3000,lambda:rootAfterCombine(videopath))
                

def rootAfterCombine(path):
    Combine.createVediofromImages(path,combineCallback)
    

def ViviaBatch():
    Vivia.doBatchesRequest()

def finishCalback(success):
    if success:
        print("SUCCESS")

        combine2Video()

    global Image2Video_index
    #Image2Video_index += 1
    #createVideos()

def rootAfterCallBack_v():
    print("ROOT AFTER CALL BACK")
    root.after(10000,ViviaBatch)

def combineCallback(folderpath):
    print(f"FOLDER PATH = {folderpath}")
    name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #short = str(int(name))
    Email.senfEmail(name,folderpath)

#----------CALLBACK-----------
def sessionidFetchCallback(sessionId):
    global session_id
    session_id = sessionId
    Const.log(f"BOT Login Success with sessionid : {session_id}")
    button_bot.config(text="已激活")

def drawCallBack(progress):
    #Const.log(f"PROGRESS = {str(progress)}")

    global index
    global progrssbars
    progressbar = progrssbars[index]
    if isinstance(progressbar,ttk.Progressbar):
        progressbar['value'] = progress

    Bot.check_queue(rootAfterCallBack)

def imagesDownloadCallback(Success,filepath):
    if Success:
        Const.log(f"IMAGES DOWNLOAD FINISH into {filepath}")
        createVideos()

def fetchCustomIDCallback(data):
    print("FETCH CUSTOMID CALL BACK")
    messid = data.messageId
    guildId = data.guildId
    channelId = data.channelId
    customIds = data.customIds

    customId_array = json.loads(customIds)
    choosen = ""
    for customid in customId_array:
        if isinstance(customid,list):
            if len(customid) == 5:
                index = random.randint(0,3)
                choosen = customid[index]
                print(f"CHOOSEN CUSTOMID = {choosen}")
                break
    if choosen == "":
        print("DID NOT FETCH CUSTOM ID")
    else:
        global session_id
        print(f"WILL DRAW WITH CUSTOM ID : {choosen},SESSION ID :{session_id}")
        funcs.drawSingleInFuncs(data,session_id,drawCustomIdCallback)
        Bot.check_queue(rootAfterCallBack)

def drawCustomIdCallback(data):
    print("DRAW CUSTOM CALLBACK IN UI_MAIN")
    if isinstance(data,ImageUrlObject):
        url = data.url
        global ImageStorePath

        print(f"DID DRAW IMAGE : {data.url}")
        name = datetime.now().timestamp()
        Const.writeImageUrl(url,ImageStorePath,"zhuanzhu_01",ImageDownloadCallback2)

def ImageDownloadCallback2(Success,name,path):
    if Success:

        print(f"DWONLOAD SUCCESS IN :{name}")

        '''
        canvas_width = 400
        canvas_height = 225

        photo = load_and_resize_image(path, canvas_width, canvas_height)
        global imageData
        global imageDataDic
        photo = imageDataDic[str(index)]
        # 将图片添加到Canvas
        global ImageCanvas
        imagePage = ImageCanvas[index]
        imagePage.create_image(0, 0, anchor=tk.NW, image=photo)
        
        index += 1
        Const.log(f"INDEX = {index}")

        unit = 3
        bg_canvas.yview_scroll(unit, "units")
        
        if index%3 == 0:
            print(f"INDEX = {str(index)},WILL REACTIVATE BOT")
            activateBot()
        '''
        beginDraw()

    else:
        print("FAIL")

def load_and_resize_image(path, width, height):
    # 加载图片并调整其大小
    global imageData

    global index
    global imageDataDic

    image = Image.open(path)
    resized_image = image.resize((width, height), Image.Resampling.LANCZOS)

    imageDataDic[str(index)] = ImageTk.PhotoImage(resized_image)

    imageData = ImageTk.PhotoImage(resized_image)
    return ImageTk.PhotoImage(resized_image)


def rootAfterCallBack():
    root.after(500,BotDoCheck)

def BotDoCheck():
    Bot.check_queue(rootAfterCallBack)

def testImageReplace():

    global index

    folder_path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])

    canvas_width = 400
    canvas_height = 225

    photo = load_and_resize_image(folder_path, canvas_width, canvas_height)
    global imageData
    global imageDataDic
    photo = imageDataDic[str(index)]

    # 将图片添加到Canvas
    global ImageCanvas
    imagePage = ImageCanvas[index]
    imagePage.create_image(0, 0, anchor=tk.NW, image=photo)

    if index%3 == 0:
        print(f"INDEX = {str(index)},WILL REACTIVATE BOT")
        activateBot()

    index+=1

root.mainloop()