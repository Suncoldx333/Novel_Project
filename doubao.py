from tkinter import Tk,Label

root = Tk()

root.geometry("400x300")
root.geometry("+200+100")

root.title("my code")

label = Label(root,text = "simple")
label.pack()

root.mainloop()