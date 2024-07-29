import os

from tkinter import Tk,ttk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename

import time
from datetime import datetime
import StableDiffusion as SD
import SD_Const as Const
import json
import threading
import tkinter as tk

import base64
import random
import asyncio
import math

root = Tk()

windowWidth = 1000
windowHeight = 800

root.geometry(f"{windowWidth}x{windowHeight}+100+100")
#-----------UI---------------
button = Button(root,text="获取prompts",command=lambda: fetchPrompts())
button.pack()
button2 = Button(root,text="配置图片保存路径",command=lambda: configFilePath())
button2.pack()

progressLabel = Label(root,text="progress",bg='lightblue')
progressLabel.pack(side='bottom')

options = ["正在获取..."]
selected_value = StringVar(root)
selected_value.set(options[0])
dropdown = OptionMenu(root,selected_value,*options)
dropdown.pack()
#-----------------------------------

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

#-----------VARS---------------
index = 0
prompts_temp = []
model_options = []
g_progress = 0
imagename = ""

drawFinish = False
prompts_global = []
currentPrompt = ""

SD_Threads = []
ImageStorePath = ""

Lines = []
progrssbars = []
ImageCanvas = []
imageData = None

#-----------------------------------
url = "https://8jty8bw5ejldhgou-80.container.x-gpu.com"
urlConfigDone = True

def fetchModels():
    if urlConfigDone:
        askgpt()
    else:
        Const.log("URL NOT CONFIG")

def fetchPrompts():
    
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if folder_path:
        print("选中的文件夹路径:", folder_path)
        bool_prompt = os.path.exists(folder_path) and folder_path.endswith('.txt')
        print(f"{bool_prompt}")
        if bool_prompt:
            with open(folder_path,'r',encoding='UTF-8') as file:
                content = file.read()
                print("content = " + content)
                prompts = content.split('\n')
                drawPicsWithPrompts(prompts)

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

    promptLabel = Label(space,width=50,height=10,font=('Arial', 10),text=text,justify="left",wraplength=150,fg='red',relief=Tk.RAISED, borderwidth=2)
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


def drawPicsWithPrompts(prompts):
    global prompts_temp
    global index
    global prompts_global
    prompts_global = prompts

    name = selected_value.get()
    hash = ""
    for model in model_options:
        innername = model["name"]
        if innername == name:
            hash = model["hash"]
            break

    Const.log(f"DID CHOOSE MODEL : {name} and {hash}")

    if len(prompts_temp) < len(prompts):
        pro = prompts[index]

        Const.customPrint(pro)

        global ImageStorePath
        storePath = ImageStorePath + "/" + str(index)
        Const.configFilePath(storePath)

        prompts_temp.append(pro)
        index += 1

        print("HAS DRAW = " + str(len(prompts_temp)) + "\n")
        print("CURRECT + " + str(datetime.now()) + "\n")

        thread = threading.Thread(target=thread_callSDImage,args=(url,pro,hash,name,drawCall_Back))
        now = datetime.now()
        print(f"WILL DRAW AT {now}")
        thread.start()

    else:
        print("FINISH AND RESET")
        prompts_temp = []
        index = 0

def configFilePath():
    global ImageStorePath
    folder_path = filedialog.askdirectory()
    if folder_path:
        print("选中的文件夹路径:", folder_path)
        ImageStorePath = folder_path
        #Const.configFilePath(folder_path)

def createHeaderCanvas():
    header = Canvas(bg_canvas,width=400,height=50,bg='lightyellow')
    header.pack()

    cv1 = Canvas(header,width=400,height=3,bg='lightyellow')
    cv1.pack(side='top')
    cv2 = Canvas(header,width=3,height=50,bg='lightyellow')
    cv2.pack(side='right')
   
    rect1 = header.create_rectangle(3, 9, 100, 50,width=3, outline='black')
    rect2 = header.create_rectangle(100, 9, 200, 50,width=3, outline='black')
    rect3 = header.create_rectangle(200, 9, 394, 50,width=3, outline='black')
    
def askgpt():
    Const.log("WILL FETCH MODELS")
    thread = threading.Thread(target=fetchModelsInUI,args=(url,askModels_callBack))
    thread.start()

def fetchModelsInUI(url,callbacck):
    SD.fetchModels(url,callbacck)

def askModels_callBack(result):
    #Const.log(result)
    array = json.loads(result)

    global SD_Threads

    count = len(array)
    Const.log(str(count))
    
    global model_options
    model_options = []

    for modelDic in array:
        name = modelDic["model_name"]
        Const.log(name)
        model_hash = modelDic["hash"]
        model_dic = {"name":name,"hash":model_hash}
        print(f"{model_dic}")
        model_options.append(model_dic)

        menu = dropdown['menu']
        menu.add_command(label=name, command=lambda x=name: selected_value.set(x))

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
    global prompts_global
    drawPicsWithPrompts(prompts_global)

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
#root.after(3000,fetchModels)
root.mainloop()
