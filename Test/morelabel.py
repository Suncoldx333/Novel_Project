from tkinter import Tk, Text, Button, Canvas, Label

root = Tk()




count = 1

canvas = Canvas(root, width=400, height=200)
canvas.config(bg='lightblue')
canvas.pack()

texts = []

def add_text():

    new_label = Label(canvas, height=6, width=12)
    new_label.config(text='566')
    new_label.pack(side='left')
    texts.append(new_label)
'''
    new_text = Text(canvas, height=7, width=14)
    new_text.insert(1.0, f"New Text {len(texts) + 1}")
    new_text.pack(side="left")
    texts.append(new_text)
'''

def add_canvas():
    new_canvas = Canvas(root,width=400,height=150)
    new_canvas.config(bg='lightyellow')
    new_canvas.pack(side='right')

def add_label():
    global count
    count += 1
    new_label = Label(canvas,height=7,width=14)
    pops = "hello~" + str(count)
    new_label.config(text=pops,bg='lightblue')
    new_label.pack(side='left')

button = Button(root, text="添加文本", command=add_canvas)
button.pack()

button2 = Button(root,text='添加标签',command=add_label)
button2.pack()

root.mainloop()