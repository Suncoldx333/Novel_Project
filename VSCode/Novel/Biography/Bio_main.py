import os
from tkinter import Tk, Frame, Scrollbar, Text,filedialog,Canvas,Label
from tkinter.ttk import Button
import Bio_loadgpt as loadgpt
import BIO_cutDes as cutDes
import Bio_Midjourney as MJ

import json
import time

from PIL import Image, ImageTk
import requests
from io import BytesIO
import asyncio
import aiohttp

root = Tk()

#--------------------------
#全局属性
global_novel = ""
global_taskId = ""
#--------------------------

#--------------------------
#主控件
button = Button(root,text="读取文件",command=lambda: calculateScale())
button.pack()

frame = Frame(root,bg="lightblue")
frame.pack()

image_widget = Label(frame,width=40,height=5,bg='lightgray')
image_widget.pack(side='bottom')

progress_widget = Label(frame,width=20,height=2,bg='lightyellow')
progress_widget.pack(side='bottom')

text_widget = Text(frame,bg="lightblue")

# 创建垂直滚动条并关联到 Text 控件
scrollbar = Scrollbar(frame, command=text_widget.yview)
text_widget.config(yscrollcommand=scrollbar.set)

text_widget.pack(side='left',expand=True)
scrollbar.pack(side='right', fill='y')

#---------------------------

#---------------------------
#获取人物形象，写入txt,MJ绘制
def askgpt():
    heroface = loadgpt.makehero()
    print(heroface)
    
    with open('D:/hero/outside/伍子胥.txt','w') as f:
        f.write(heroface)
    text_widget.delete('1.0','end')
    text_widget.insert('1.0',heroface)

    button.config(text="形象")
    button.config(command=lambda: drawhero())
    

def drawhero():

    image_path = "E:/hero/outside/local_image.jpg"
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_widget.config(image=photo)
    image_widget.image = photo
    image_widget.config(width=400,height=200)

    '''
    file_path = filedialog.askopenfilename()
    print("filepath = " + file_path)
    if os.path.exists(file_path) and file_path.endswith('.txt'):
        with open(file_path,'r',encoding='UTF-8') as file:
            content = file.read()
            hero = content
    else:
        hero = ""

    trans = loadgpt.translate(hero)
    print("trans = " + trans)
    
    dic = MJ.createHero(trans)
    print(dic)

    progress = dic["progress"]
    taksId = dic["taskId"]
    global global_taskId
    global_taskId = taksId
    #progress_widget.config(text=progress)


    time.sleep(2)
    
    dic = MJ.fetch("1716272991622634")
    progress = "100%"
    imageUrl = dic['imageUrl']
    progress_widget.config(text=progress)
    if imageUrl is not None:
        #asyncio.run(download_image_async(imageUrl,"E:/hero/outside/local_image.jpg"))
        image = Image.open("E:/hero/outside/local_image.jpg")
        photo = ImageTk.PhotoImage(image)

        print("\nGETTING IMAGE SIZE")
        w,h = image.size
        print("\n IMAGE SIZE :" + str(w) + str(h))

        #zoomed = zoom_image(image,10)
        #zoomed_photo = ImageTk.PhotoImage(zoomed)

       # image_widget.config(bg='black')
        image_widget.config(image=photo)

       # w1,h1 = image_widget.size
        print(image_widget.winfo_width(),image_widget.winfo_height())
    '''
#---------------------------

def calculateScale():
    image_path = "E:/hero/outside/local_image.jpg"
    print("123")
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    w_target = image.width / 2
    h_target = image.height / 2

    print("w,h = " + str(w_target) + str(h_target))

    canvas = Canvas(frame, width = w_target, height = h_target )
    canvas.config(bg='lightyellow')
    canvas.pack(side='bottom')

    canvas.create_image(0, 0, anchor="nw", image=photo)

def resize_image_proportionally(image_path, max_width, max_height):
    image = Image.open(image_path)
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    ratio = min(width_ratio, height_ratio)
    new_width = int(image.width * ratio)
    new_height = int(image.height * ratio)
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    resized_image.save("resized_proportional_image.jpg")

def resize_image(image_path, new_width, new_height):
    image = Image.open(image_path)
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    resized_image.save("resized_image.jpg")

def show_image(url):
    print("imageUrl = ",url)
    response = requests.get(url)

    data_stream = BytesIO(response.content)
    pil_image = Image.open(data_stream)
    w,h = pil_image.size
    tk_image = ImageTk.PhotoImage(pil_image)

    #image_widget.config(image=tk_image,bg='black')
    #image_widget.config(padx=5,pady=5)

async def async_load_image(url, label):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            image = Image.open(BytesIO(data))
            photo = ImageTk.PhotoImage(image)

           # zoomed = zoom_image(image,3)
           # zoomed_photo = ImageTk.PhotoImage(zoomed)

            label.image = photo

def display_image(url):
    print("imageUrl = ",url)
    asyncio.run(async_load_image(url, image_widget))

def zoom_image(image, factor):
    width, height = image.size
    new_width = int(width * factor)
    new_height = int(height * factor)
    zoomed_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return zoomed_image

async def download_image_async(image_url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            image_data = await response.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')
            image.save(save_path)

def askforscree():
    screes = loadgpt.askscreens()
    print("-----\n" + screes + "\n-----")


#---------------------------
#提取
def makegrids(arraystr):
    print("str = " + arraystr)

    cnhead = "画面描述："
    cnend = "。"
    enhead = "英文描述："
    enend = "."

    #arraystr = "镜一：陈伶愕然地看着\n\n脚下的"
    
    lines = arraystr.split('画面描述')
    for items in lines:
        print(items)
        ##print("array = " + str(len(array)))
''' 
    cns = extract_strings(arraystr,cnhead,cnend)
    ens = extract_strings(arraystr,enhead,enend)

    print("cn = " + cns)
    print("en = " + ens)


    array = json.loads(str)
    print("len = " + str(len(array)))

    for item in array :
        print("item = " + item)
        cn = item["画面描述"]
        en = item["英文描述"]
        print("cn = " + cn + "\nen = " + en)
'''
def extract_strings(text,head,end):
    result = []
    start_index = 0
    while True:
        start = text.find(head, start_index)
        if start == -1:
            break
        end = text.find(end, start + 1)
        if end!= -1:
            result.append(text[start:end + 1])
        start_index = start + 1
    return result

#---------------------------








#---------------------------
#读取文件

def select_file():

    print("读取文件")

    array = cutDes.test()
    for dic in array:
        key_s = 'screen'
        key_e = 'EN'
        key_c = 'CN'

        screen = dic[key_s]
        EN = dic[key_e]
        CN = dic[key_c]

        text_widget.pack_forget()
        create(screen,EN,CN)



    '''
    global global_novel
    file_path = filedialog.askopenfilename()
    print("filepath = " + file_path)
    if os.path.exists(file_path) and file_path.endswith('.txt'):
        with open(file_path,'r',encoding='UTF-8') as file:
            content = file.read()
            global_novel = content
    else:
        global_novel = ""
    text_widget.delete('1.0','end')
    text_widget.insert('1.0',global_novel)

    button.config(text="分镜")
    button.config(command=lambda: buttonclick())
    '''
#---------------------------

def create(screen,CN,EN):
    print()
    canvas = Canvas(frame,height=20)
    canvas.pack(side='bottom')

    label1 = Label(canvas, text="aadad", wraplength=5, justify="left")
    #label1.config(width=200,height=100)
    label1.config(bg='lightgray')
    label1.place(x=5, y=5)

    label2 = Label(canvas, text=CN, wraplength=5, justify="left")
    label2.config(width=200,height=100)
    label2.config(bg='lightblue')
    label2.place(x=100, y=5)
    
    label3 = Label(canvas, text=EN, wraplength=5, justify="left")
    label3.config(width=200,height=100)
    label3.config(bg='lightyellow')
    label3.place(x=200, y=5)



#---------------------------
#gpt描述分镜
def buttonclick ():
    print("分镜")
    
    novel = text_widget.get('1.0','end')
    
    makegrids(novel)

    '''
    novel = text_widget.get('1.0','end')
    screens = loadgpt.makescreen(novel)
    text_widget.delete('1.0','end')
    text_widget.insert('1.0',screens)
    
    print(screens)
    with open('D:/novel/gpt_answer.txt','w') as f:
        f.write(screens)
    '''
#---------------------------


def makedes ():
    print("描述")
    des = loadgpt.makemore("请为每个分镜创建简洁的画面描述")

    #button.config(text="翻译")
    #button.config(command=lambda: delivertrans())

    descri = loadgpt.makemore(des)
    text_widget.delete('1.0','end')
    text_widget.insert('1.0',descri)

    short = cutDes.find_bracketed_strings(descri)
    #more = cutDes.find_bracketed_strings(short)
    print(short)

'''
def translate ():
    print("翻译")
    button.state(['disabled'])
    translatestr = loadgpt.makemore("请将每个画面描述翻译为英文")

    descri = loadgpt.makemore(translatestr)
    text_widget.delete('1.0','end')
    text_widget.insert('1.0',descri)
    print(descri)

    print("will cut")
    #获得截取后的英文组成的json，转回数组
    cutjson = cutDes.find(descri)
    text_widget.delete('1.0','end')
    text_widget.insert('1.0',cutjson)
'''

def delivertrans (des):
    print("提取英文")
    #获得截取后的英文组成的json，转回数组
    cutarray = cutDes.find_bracketed_strings(des)
    count = len(cutarray)

    sss = ""
    if str(count):
        array = json.loads(cutarray[0])
        print("----count = " + str(len(array)))

        for asd in array:
            sss = sss + asd


    text_widget.delete('1.0','end')
    text_widget.insert('1.0',sss)


root.mainloop()