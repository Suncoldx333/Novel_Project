import os

from tkinter import Tk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename

import time
from datetime import datetime
import StableDiffusion as SD
import SD_Const as Const
import json
import threading

import base64
import random
import asyncio
import math

root = Tk()

button = Button(root,text="获取人物形象描述",command=lambda: askgpt())
button.pack()

progressLabel = Label(root,text="progress",bg='lightblue')
progressLabel.pack(side='bottom')

options = ["正在获取..."]
selected_value = StringVar(root)
selected_value.set(options[0])
dropdown = OptionMenu(root,selected_value,*options)
dropdown.pack()

index = 0
prompts_temp = []
g_progress = 0
imagename = ""

drawFinish = False
prompts_global = []
currentPrompt = ""

SD_Threads = []

url = "https://gllh9u2mw3szyywz-80.container.x-gpu.com"

def askgpt():
    '''
    Const.log("Draw")
    file_path = "E:/novel_ai/ImageBase64s.txt"
    Image_path = "E:/novel_ai/333.png"
    with open(file_path,"r") as file:
        content = file.read()
    imageData = base64.b64decode(content)
    with open (Image_path,"wb") as f:
        f.write(imageData)
    
    global prompts_global
    folder_path = askopenfilename(filetypes=[("Text files", "*.txt")])
    if folder_path:
        print("Selected folder:", folder_path)
        with open(folder_path,"r") as file:
            content = file.read()
        prompts_global = content.split('\n')
'''
    SD.fetchModels(url,askModels_callBack)

def askModels_callBack(result):
    #Const.log(result)
    array = json.loads(result)

    global SD_Threads

    count = len(array)
    Const.log(str(count))
    
    model_options = []

    for modelDic in array:
        name = modelDic["model_name"]
        Const.log(name)
        model_hash = modelDic["hash"]
        model_dic = {"name":name,"hash":model_hash}
        model_options.append[model_dic]
        dropdown.add_command(label=name, command=lambda x=name: selected_value.set(x))
    name_0 = model_options[0]["name"]
    selected_value.set(name_0)

'''
    menu = dropdown['menu']
    menu.delete(0, 'end')
    model_0 = model_options[0]
    model_name = model_0["name"]


    
    ran = random.randint(1,count)
    randonname = array[ran]["model_name"]
    randomHash = array[ran]["hash"]




    Const.log("WILL DRAW" + randonname)
    global imagename
    imagename = str(randonname)
    prompt = "Against the vast expanse of night sky, stars twinkle, and Zhuang Xu's figure transforms into the brightest star, guiding those who follow along the path of righteousness and loyalty."
    thread = threading.Thread(target=thread_callSDImage,args=(url,prompt,randomHash,randonname,drawCall_Back))
    now = datetime.now()
    print(f"WILL DRAW AT {now}")
    thread.start()
    SD_Threads.append(thread)

    time.sleep(1)
    thread_p = threading.Thread(target=thread_callSDProgress,args=(url,progress_Callback))
    now2 = datetime.now()
    print(f"WILL GET PROGRESS AT {now2}")
    thread_p.start()
    SD_Threads.append(thread_p)

    #for thread in SD_Threads:
        #thread.join()
'''

def checkOptions():
    select = selected_value.get()
    print(f"HASH = {select}")

def thread_callSDImage(url,prompt,randomHash,randomName,callBack):
    SD.SD_ImageWithPrompt(url,prompt,randomHash,randomName,callBack)

def thread_callSDProgress(url,callBack):
    SD.checkprogress(url,callBack)

def drawCall_Back():
    Const.log("DRAW FINISH")
    global drawFinish
    drawFinish = True
    

def progress_Callback(progressDic):

    progress = progressDic["progress"]
    progress_num = float(progress) * 100
    progrss_floor = math.floor(progress_num)
    progressLabel.config(text=str(progrss_floor))
    Const.log("PREGRESS = " + str(progrss_floor))
    

    global drawFinish
    if drawFinish:
        Const.log("FINISH DRAW")
        progressLabel.config(text="100")
    elif progress_num < 100 and progress > 0:
        thread_p = threading.Thread(target=thread_callSDProgress,args=(url,progress_Callback))
        now2 = datetime.now()
        print(f"WILL GET PROGRESS AT {now2}")
        thread_p.start()
        SD_Threads.append(thread_p)
    else:
        Const.log("FALSE CONDITION")
        progressLabel.config(text="100")
    global imagename
    #Const.log(progressDic)
    

    ''''
    if progress_num < 100:
        job = progressDic["state"]["job"]
        if job == "":
            Const.log("FINISH")
        else:
            Const.log("need fetch again")
            time.sleep(3)
            SD.checkprogress(url,progress_Callback)
    else:
        image = progressDic["current_image"]
        Const.base2img(image,imagename)
    '''

root.mainloop()