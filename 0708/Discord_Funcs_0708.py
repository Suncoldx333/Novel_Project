import os

from tkinter import Tk,ttk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu,messagebox
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename
import tkinter as tk


import time
from datetime import datetime

import Const_Final_0708 as Const

import threading
from PIL import Image, ImageTk
from Bot_Data_0708 import CustomIdObject

import Discord_Bot_Main_0708 as Bot
import Dsicord_Network_Main_0708 as Network

import Discord_DownloadImages as Downloader

#----------------GLOBAL VARS-----------
index = 0
prompts_temp = []
g_progress = 0

prompts_filepath = ""
character_filepath = ""
ImageStorePath = ""

Lines = []
progrssbars = []
ImageCanvas = []
imageData = None
drawCallback = None
imagesDwonloadCallback = None
drawWithCusomCallback = None

#-------------------FUNS-----------------------
def ActivateBot(callback):
    Bot.loginBot(callback)
    #print("NO LONGER USE")

def fetchPrompts():

    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if folder_path:
        print("选中的文件夹路径:", folder_path)
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
                    #createMainLine(prompt)
                #button.config(text='已配置')


def fetchCharacter():
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    global character_filepath
    character_filepath = folder_path
#-------------CONFIG-------------------
def fetchCharacterFilePath(path):
    Const.log(f"Character url in {path}")
    global character_filepath
    character_filepath = path

def configImageSavePath(path):
    Const.log(f"Image save in {path}")
    global ImageStorePath
    ImageStorePath = path

def configPromptFilePath(path):
    Const.log(f"PROMPT in {path}")
    global prompts_filepath
    prompts_filepath = path

def beginDraw(params,callback,c_callback,d_callback):

    if len(params) == 0:
        return
    Network.configParam(params)

    global drawCallback
    drawCallback = callback
    
    global imagesDwonloadCallback
    imagesDwonloadCallback = d_callback

    global prompts_filepath
    global character_filepath
    global ImageStorePath
    if prompts_filepath == "" or character_filepath == "" or ImageStorePath == "":
        #print(f"PROMPTS = {prompts_filepath},CHARACTER = {character_filepath},SAVEPATH = {ImageStorePath}")
        #Const.log("FILEPATH DID NOT CONFIG")

        messagebox.showinfo("错误提示","FILEPATH DID NOT CONFIG")

        return
    Const.log(f"GET PROMPTS AT {prompts_filepath} AND CHARACTER AT {character_filepath} AND IMAGE WILL STORE IN {ImageStorePath}")

    bool_prompt = os.path.exists(prompts_filepath) and prompts_filepath.endswith('.txt')
    bool_character = os.path.exists(character_filepath) and character_filepath.endswith('.txt')

    if bool_prompt and bool_character:
        with open(prompts_filepath,'r',encoding='UTF-8') as file:
            content = file.read()
            #print("content = " + content)
            prompts = content.split('\n')

            with open(character_filepath,'r',encoding='UTF-8') as c_file:
                c_content = c_file.read()
                #print("\n" + c_content + "\n")
                for prompt in prompts:
                    print("prompt = " + prompt + "\n")

        Bot.configProgressCallback(callback) 
        Bot.configDrawingState(True,False)
        Bot.configFetchCustomIdCallback(c_callback)
        fetch(prompts,c_content)

    else:
        hero = ""

def drawSingleInFuncs(custom,sessionid,callback):
    global drawWithCusomCallback
    drawWithCusomCallback = callback

    Bot.configDrawingState(False,True)
    Bot.configFetchCustomImageUrlCallback(callback)

    thread = threading.Thread(target=thread_imagineWithCustomId,args=(custom,sessionid,drawCustomCallback))
    now = datetime.now()
    print(f"SINGLE WILL DRAW AT {now}")
    thread.start()
    

def thread_imagineWithCustomId(custom,sessionId,callback):
    if isinstance(custom,CustomIdObject):
        print(f"WILL DRAW CUSTOM IN SESSION : {sessionId}")
        Network.drawSingleWithCustomId(custom,sessionId,callback)

def drawCustomCallback(code):
    print(f"FINISH DRAW CUSTOM WITH CODE :{str(code)}")
    

def configFilePath():
    global ImageStorePath
    folder_path = filedialog.askdirectory()
    if folder_path:
        print("选中的文件夹路径:", folder_path)
        ImageStorePath = folder_path
        

def configCharacter():
    global character_filepath
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    character_filepath = folder_path
    if character_filepath:
        Const.log("123")

#--------------------
def callback_taskId(code):
    Const.customPrint("\n CALLBACK_TASKID")
    Const.log(f"CODE = {str(code)}")
    global drawCallback
    if drawCallback:
        drawCallback(code,0)

def callback_progress(progress,taskId,customId,url):
    Const.customPrint("\n CALLBACK_PROGRESS")

    global index
    global progrssbars

    cut = extract_digits(progress)
    #progressLabel.config(text=str(cut))
    Const.customPrint(str(cut))

    viewIndex = index - 1
    current = progrssbars[viewIndex]
    current['value'] = int(cut)

    if int(cut) < 100 :
        time.sleep(5)
        Const.customPrint("FETCH AGAIN")
        #MJ.fetch(taskId,callback_progress)
    else:
        #绘画完成
        Const.customPrint("绘画完成！")
        Const.customPrint(url)
        if customId == "":
            Const.customPrint("ERROR CUSTOMID")
        else :
            Const.log("FINISH")
            #获取单图
            time.sleep(2)
            Const.customPrint(customId)
            thread = threading.Thread(target=thread_action,args=(taskId,customId,callback_action))
            thread.start()


def callback_action(code,taskId,customId):
    Const.customPrint(str(code))
    Const.customPrint(taskId)

    if code == 1:

        thread = threading.Thread(target=thread_customId,args=(taskId,callback_customIdProgress))
        thread.start()
    else:
        time.sleep(10)
        Const.customPrint("SLEEP FOR 10 SEC")
        #MJ.action(taskId,customId,callback_action)
        thread = threading.Thread(target=thread_action,args=(taskId,customId,callback_action))
        thread.start()


def extract_digits(string):
    return ''.join(e for e in string if e.isdigit())

#---------------------------------------

#---------------------------------------

def callback_customIdProgress(progress,taskId,url,status):
    Const.customPrint("\n CALLBACK_CUSTOMID_PROGRESS")
    Const.customPrint(status)
    
    if status == "NOT_START":
        Const.log(status)
        #thread = threading.Thread(target=thread_customFetch,args=(taskId,callback_customIdProgress))
        #thread.start()
    else:
        cut = extract_digits(progress)
        global index
        viewIndex = index -1
        current = progrssbars[viewIndex]
        current['value'] = int(cut)

        #progressLabel.config(text=str(cut))
        Const.customPrint(str(cut))

        if int(cut) < 100 :
            time.sleep(5)
            Const.customPrint("FETCH AGAIN")
            #MJ_CustomId.fetch(taskId,callback_customIdProgress)
            thread = threading.Thread(target=thread_customFetch,args=(taskId,callback_customIdProgress))
            thread.start()
        else:
            #绘画完成
            Const.customPrint(url)

            global prompts_temp
            index = len(prompts_temp) - 1
            file_name = "hero" + str(index) + ".jpg"
            Const.log(file_name)
            global ImageStorePath

            file_path = ImageStorePath + "/" + str(index) + "/" + file_name
            Const.download_image(url,file_path,file_name,callback_download)


def callback_download(succuess,filename):
    
    if str(succuess) == "True":
        Const.log(filename + "------SUCCESS")

        canvas_width = 400
        canvas_height = 225

        global ImageStorePath
        global prompts_temp
        index = len(prompts_temp) - 1
        img_path = ImageStorePath + "/" + str(index) + "/" + filename
        
        photo = load_and_resize_image(img_path, canvas_width, canvas_height)
        global imageData
        photo = imageData
        # 将图片添加到Canvas
        global ImageCanvas
        imagePage = ImageCanvas[0]
        imagePage.create_image(0, 0, anchor=tk.NW, image=photo)

    else:
        Const.log("FAIL")

    #global prompts_temp
    #global index

    #fetchPrompts()


def load_and_resize_image(path, width, height):
    # 加载图片并调整其大小
    global imageData

    image = Image.open(path)
    resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
    imageData = ImageTk.PhotoImage(resized_image)
    return ImageTk.PhotoImage(resized_image)

#---------------------------------------

def fetch(prompts,character):
    Const.log("FETCH")

    global prompts_temp
    global index

    if len(prompts_temp) < len(prompts):
        pro = prompts[index]

        Const.customPrint(pro)

        global ImageStorePath
        storePath = ImageStorePath + "/" + str(index)

        if os.path.exists(storePath):
            Const.log("PATH EXIST")
            Const.configFilePath(storePath)
        else:
            Const.configFilePath(storePath)

        prompts_temp.append(pro)
        index += 1

        print("HAS DRAW = " + str(len(prompts_temp)) + "\n")
        print("CURRECT + " + str(datetime.now()) + "\n")
        
        thread = threading.Thread(target=thread_imagineWithPrompt,args=(pro,character,callback_taskId))
        now = datetime.now()
        print(f"WILL DRAW AT {now}")
        thread.start()


    else:
        print("FINISH AND RESET SHOULD LOAD IMAGES")
        prompts_temp = []
        index = 0
        global imagesDwonloadCallback

        #global ImageStorePath
        path = ImageStorePath + '/Downloads'

        if imagesDwonloadCallback:
            print("图片绘制完成,开始下载之downloads文件夹内")
            Downloader.OutterDownload(ImageStorePath,path,imagesDwonloadCallback)

def thread_imagineWithPrompt(pro,character,callback):
    Const.log("THREAD IMAGE WITH PROMPTS")
    Network.drawWithPrompt(pro,character,callback)

def thread_fetchProgress(taskId,callback):
    Const.log("THREAD FETCH PROGRESSS")
    #MJ.fetch(taskId,callback)

def thread_action(taskId,customId,callback):
    Const.log("THREAD ACTION")
    #MJ.action(taskId,customId,callback)

def thread_customId(taskId,callback):
    Const.log("THREAD CUSTOMID")
    #MJ_CustomId.fetch(taskId,callback)

def thread_customFetch(taskId,callback):
    Const.log("THREAD CUSTOMF FETCJ")
    #MJ_CustomId.fetch(taskId,callback)

def drawPicWithPrompt(prompt,character):
    Const.log("THREAD DRAW")
    #taskId = MJ.imagineWithPrompt(prompt,character)
    #Const.customPrint(taskId)

def fetchProgress (taskId):

    print("FETCH PROGRESS" + "\n")
    



def test():
    now = datetime.now()
    print("now = " + str(now))

    now = datetime.now()
    print("now = " + str(now))