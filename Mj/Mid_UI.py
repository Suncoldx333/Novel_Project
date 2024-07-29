import os

from tkinter import Tk,ttk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu,messagebox
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename
import tkinter as tk

import Midjourney as MJ
import Midjourney_CustomId as MJ_CustomId
import Mid_loadgpt as gpt
import time
from datetime import datetime

import Mid_Const as Const
import threading
from PIL import Image, ImageTk

root = Tk()

windowWidth = 1000
windowHeight = 800

root.geometry(f"{windowWidth}x{windowHeight}+100+100")

currentProgress = None

#-----------UI---------------HEADER
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
#dropdown = OptionMenu(root,selected_value,*options)
#dropdown.pack()

button4 = Button(root,text="开始生成",command=lambda: beginDraw())
button4.pack()

#-----------------------------------MAIN
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
                    createMainLine(prompt)
                button.config(text='已配置')
                    

def testFrame():
    print("add label")
    Label = tk.Label(frame,text='1233',fg='red')
    Label.pack()

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
#--------------------------------

def fetchCharacter():
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    global character_filepath
    character_filepath = folder_path
    #label_Character.config(text=character_filepath,fg="darkgreen")

def configImageSavePath():
    global ImageStorePath
    folder_path = filedialog.askdirectory()
    if folder_path:
        print("选中的文件夹路径:", folder_path)
        ImageStorePath = folder_path
        #label_ImagePath.config(text=ImageStorePath,fg='darkgreen')

def beginDraw():
    
    global prompts_filepath
    global character_filepath
    global ImageStorePath
    if prompts_filepath == "" or character_filepath == "" or ImageStorePath == "":
        #Const.log("FILEPATH DID NOT CONFIG")

        messagebox.showinfo("错误提示","FILEPATH DID NOT CONFIG")

        return
    Const.log(f"GET PROMPTS AT {prompts_filepath} AND CHARACTER AT {character_filepath} AND IMAGE WILL STORE IN {ImageStorePath}")

    bool_prompt = os.path.exists(prompts_filepath) and prompts_filepath.endswith('.txt')
    bool_character = os.path.exists(character_filepath) and character_filepath.endswith('.txt')

    if bool_prompt and bool_character:
        with open(prompts_filepath,'r',encoding='UTF-8') as file:
            content = file.read()
            print("content = " + content)
            prompts = content.split('\n')

            with open(character_filepath,'r',encoding='UTF-8') as c_file:
                c_content = c_file.read()
                print("\n" + c_content + "\n")
                for prompt in prompts:
                    print("prompt = " + prompt + "\n")

                #taskId = MJ.imagineWithPrompt(prompt,c_content)
                #print("TASKID---" + taskId) 

            
        fetch(prompts,c_content)

    else:
        hero = ""


def configFilePath():
    global ImageStorePath
    folder_path = filedialog.askdirectory()
    if folder_path:
        print("选中的文件夹路径:", folder_path)
        ImageStorePath = folder_path
        button2.config(text='已配置')

def configCharacter():
    global character_filepath
    folder_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    character_filepath = folder_path
    if character_filepath:
        button3.config(text='已配置')

#--------------------
def callback_taskId(code,taskId):
    Const.customPrint("\n CALLBACK_TASKID")
    if code == 1:
        Const.customPrint(taskId)

        Const.customPrint("WILL FETCH")

        thread = threading.Thread(target=thread_fetchProgress,args=(taskId,callback_progress))
        thread.start()
    else:
        Const.log("fail code")

def callback_progress(progress,taskId,customId,url):
    Const.customPrint("\n CALLBACK_PROGRESS")

    global index
    global progrssbars

    cut = extract_digits(progress)
    progressLabel.config(text=str(cut))
    Const.customPrint(str(cut))

    viewIndex = index - 1
    current = progrssbars[viewIndex]
    current['value'] = int(cut)

    if int(cut) < 100 :
        time.sleep(5)
        Const.customPrint("FETCH AGAIN")
        MJ.fetch(taskId,callback_progress)
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
    
    global prompts_temp
    global index

    if len(prompts_temp) < len(prompts):
        pro = prompts[index]

        Const.customPrint(pro)

        global ImageStorePath
        storePath = ImageStorePath + "/" + str(index)
        if os.path.exists(storePath):
            Const.log("PATH EXIST")
        else:
            Const.configFilePath(storePath)

        prompts_temp.append(pro)
        index += 1

        print("HAS DRAW = " + str(len(prompts_temp)) + "\n")
        print("CURRECT + " + str(datetime.now()) + "\n")
        #MJ.imagineWithPrompt(pro,character,callback_taskId)
        thread = threading.Thread(target=thread_imagineWithPrompt,args=(pro,character,callback_taskId))
        now = datetime.now()
        print(f"WILL DRAW AT {now}")
        thread.start()

    else:
        print("FINISH AND RESET")
        prompts_temp = []
        index = 0

def thread_imagineWithPrompt(pro,character,callback):
    MJ.imagineWithPrompt(pro,character,callback)

def thread_fetchProgress(taskId,callback):
    MJ.fetch(taskId,callback)

def thread_action(taskId,customId,callback):
    MJ.action(taskId,customId,callback)

def thread_customId(taskId,callback):
    MJ_CustomId.fetch(taskId,callback)

def thread_customFetch(taskId,callback):
    MJ_CustomId.fetch(taskId,callback)

def drawPicWithPrompt(prompt,character):
    taskId = MJ.imagineWithPrompt(prompt,character)
    Const.customPrint(taskId)

def fetchProgress (taskId):

    print("FETCH PROGRESS" + "\n")
    global g_progress
    g_progress = MJ.fetch(taskId)
    lastIndex = len(g_progress) - 1
    cutProgress = g_progress[0 : lastIndex]
    progressLabel.config(text=cutProgress)



def test():
    now = datetime.now()
    print("now = " + str(now))

    gpt.ask_test()

    now = datetime.now()
    print("now = " + str(now))




root.mainloop()