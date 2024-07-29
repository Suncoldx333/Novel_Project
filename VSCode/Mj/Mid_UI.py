import os

from tkinter import Tk, Frame, Scrollbar, Text,filedialog,Canvas,Label
from tkinter.ttk import Button

import Midjourney as MJ
import Midjourney_CustomId as MJ_CustomId
import Mid_loadgpt as gpt
import time
from datetime import datetime

import Mid_Const as Const


root = Tk()

button = Button(root,text="读取文件",command=lambda: calculateScale())
button.pack()

progressLabel = Label(root,text="progress",bg='lightblue')
progressLabel.pack(side='bottom')

index = 0
prompts_temp = []
g_progress = 0

def calculateScale():
    
    file_path = "E:/hero/3/prompts.txt"
    character = "E:/hero/3/character.txt"

    bool_prompt = os.path.exists(file_path) and file_path.endswith('.txt')
    bool_character = os.path.exists(character) and file_path.endswith('.txt')

    if bool_prompt and bool_character:
        with open(file_path,'r',encoding='UTF-8') as file:
            content = file.read()
            print("content = " + content)
            prompts = content.split('\n')

            with open(character,'r',encoding='UTF-8') as c_file:
                c_content = c_file.read()
                print("\n" + c_content + "\n")
                for prompt in prompts:
                    print("prompt = " + prompt + "\n")

                #taskId = MJ.imagineWithPrompt(prompt,c_content)
                #print("TASKID---" + taskId) 

            
        fetch(prompts,c_content)

    else:
        hero = ""

#--------------------
def callback_taskId(code,taskId):
    Const.customPrint("\n CALLBACK_TASKID")
    if code == 1:
        Const.customPrint(taskId)

        Const.customPrint("WILL FETCH")
        MJ.fetch(taskId,callback_progress)
    else:
        Const.log("fail code")

def callback_progress(progress,taskId,customId,url):
    Const.customPrint("\n CALLBACK_PROGRESS")

    cut = extract_digits(progress)
    progressLabel.config(text=str(cut))
    Const.customPrint(str(cut))

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
            MJ.action(taskId,customId,callback_action)


def callback_action(code,taskId,customId):
    Const.customPrint(str(code))
    Const.customPrint(taskId)

    if code == 1:
        MJ_CustomId.fetch(taskId,callback_customIdProgress)
    else:
        time.sleep(10)
        Const.customPrint("SLEEP FOR 10 SEC")
        MJ.action(taskId,customId,callback_action)

def extract_digits(string):
    return ''.join(e for e in string if e.isdigit())

#---------------------------------------

#---------------------------------------

def callback_customIdProgress(progress,taskId,url,status):
    Const.customPrint("\n CALLBACK_CUSTOMID_PROGRESS")
    Const.customPrint(status)
    
    if status == "NOT_START":
        MJ_CustomId.fetch(taskId,callback_customIdProgress)
    else:
        cut = extract_digits(progress)
        progressLabel.config(text=str(cut))
        Const.customPrint(str(cut))

        if int(cut) < 100 :
            time.sleep(5)
            Const.customPrint("FETCH AGAIN")
            MJ_CustomId.fetch(taskId,callback_customIdProgress)
        else:
            #绘画完成
            Const.customPrint(url)

            global prompts_temp
            index = len(prompts_temp)
            file_name = "hero" + str(index) + ".jpg"
            Const.log(file_name)

            file_path = "E:/hero/outside/" + file_name + ".jpg"
            Const.download_image(url,file_path,file_name,callback_download)


def callback_download(filename):
    Const.log(filename + "------SUCCESS")

    global prompts_temp
    global index

    calculateScale()


#---------------------------------------

def fetch(prompts,character):
    
    global prompts_temp
    global index

    if len(prompts_temp) < len(prompts):
        pro = prompts[index]

        Const.customPrint(pro)

        prompts_temp.append(pro)
        index += 1

        print("HAS DRAW = " + str(len(prompts_temp)) + "\n")
        print("CURRECT + " + str(datetime.now()) + "\n")
        MJ.imagineWithPrompt(pro,character,callback_taskId)


    else:
        print("FINISH AND RESET")
        prompts_temp = []
        index = 0





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