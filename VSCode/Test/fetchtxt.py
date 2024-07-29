from tkinter import Tk, Label, Entry, Button, filedialog
import os

def select_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, 'end')
    entry.insert(0, file_path)

def read_file():
    file_path = entry.get()
    if os.path.exists(file_path) and file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            content = file.read()
            label.config(text=content)
    else:
        label.config(text="文件不存在或不是 TXT 文件")

root = Tk()

Label(root, text="选择文件ewe:").pack()
entry = Entry(root)
entry.pack()

select_button = Button(root, text="选择文件", command=select_file)
select_button.pack()

read_button = Button(root, text="读取", command=read_file)
read_button.pack()

label = Label(root, wraplength=300)
label.pack()

root.mainloop()