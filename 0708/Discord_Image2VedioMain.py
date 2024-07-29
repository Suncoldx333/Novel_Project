import Discord_ViviaRequest as Request
import os
from glob import glob

from tkinter import Tk,ttk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu,messagebox
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename
import tkinter as tk

root = Tk()

windowWidth = 1000
windowHeight = 800

root.geometry(f"{windowWidth}x{windowHeight}+600+50")

button_bot = Button(root,text="START",command=lambda: start())
button_bot.pack()
button2 = Button(root,text="CONFIG",command=lambda: configPath())
button2.pack()

index = 0
folder_path = ""

def start():
    if Request.downloadTargetPath == "":
        print("SHOULD CONFIG PATH")
        return
    else:
        global index
        global folder_path
        if folder_path == "":
            folder_path = filedialog.askdirectory()
        if folder_path:
            print("选中的文件夹路径:", folder_path)

            jpg_files = glob(os.path.join(folder_path, '*.jpg'))

            if index < len(jpg_files):
                path_c = jpg_files[index]
                print(f"START WITH IMAGE : {path_c}")
                Request.beginWithImage(path_c,rootAfterCallBack,finishCalback)
            

            else:
                print('Finish')

def configPath():
    folder_path = filedialog.askdirectory()
    Request.configDownloadPath(folder_path) 

def rootAfterCallBack():
    root.after(60000,ViviaBatch)

def finishCalback(success):
    if success:
        print("SUCCESS")
    global index
    index += 1
    start()

def ViviaBatch():
    Request.doBatchRequest("")

root.mainloop()