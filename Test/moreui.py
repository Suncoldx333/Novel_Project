from tkinter import Tk, Button, Toplevel,Label,Canvas,Text

root = Tk()

canvas = Canvas(root, width=200, height=100)  # 设置固定的 scrollregion
canvas.config(bg='lightblue')
canvas.pack()

label = Label(canvas, text="这是一个很宽的标签", width=50)
label.config(bg='lightblue')
label.pack()

'''
root = Tk()

array_canvas = []

def add_canvas():
    new_canvas = Canvas(root,width=400,height=150)
    new_canvas.config(bg='lightyellow')
    new_canvas.pack(side='top')
    array_canvas.append(new_canvas)

def add_texts():

    target_canvas = array_canvas[1]
    new_text = Text(target_canvas,width=7,height=3.5)
    new_text.insert(1.0,'wowowo')
    new_text.config(state='disabled')
    new_text.pack(side='right')

button = Button(root, text="添加画布", command=add_canvas)
button.pack()

button2 = Button(root, text="添加文本", command=add_texts)
button2.pack()

canvas = Canvas(root, width=400, height=200)
canvas.config(bg='lightblue')
canvas.pack()

'''

root.mainloop()

