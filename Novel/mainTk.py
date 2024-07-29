import os
from tkinter import Tk, Frame, Scrollbar, Text,filedialog,Canvas,Label
from tkinter.ttk import Button
import loadgpt as loadgpt
import cutDes as cutDes

import json

root = Tk()

#--------------------------
#全局属性
global_novel = ""

#--------------------------

#--------------------------
#主控件
button = Button(root,text="读取文件",command=lambda: select_file())
button.pack()

frame = Frame(root,bg="lightblue")
frame.pack()

text_widget = Text(frame,bg="lightblue")

# 创建垂直滚动条并关联到 Text 控件
scrollbar = Scrollbar(frame, command=text_widget.yview)
text_widget.config(yscrollcommand=scrollbar.set)

text_widget.pack(side='left',expand=True)
scrollbar.pack(side='right', fill='y')

#---------------------------



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