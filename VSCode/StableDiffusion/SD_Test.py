import tkinter as tk
from tkinter import ttk

def set_optionmenu(opl):
    # 获取 OptionMenu 的菜单对象
    menu = option_menu['menu']
    # 清空菜单中的选项
    menu.delete(0, 'end')
    # 添加新的选项
    opshow = "qweqe"
    for op in opl:
        menu.add_command(label=op, command=lambda x=op: v.set(x))
    # 设置默认显示的选项
    v.set(opshow)

root = tk.Tk()

# 创建一个变量，用于存储选项的值
v = tk.StringVar(root)
# 创建 OptionMenu 组件
option_menu = ttk.OptionMenu(root, v, "(空)", "Option 1", "Option 2", "Option 3")
option_menu.pack()

# 更新选项的按钮
new_options = ["123","213"]
update_button = tk.Button(root, text="Update Options", command=lambda: set_optionmenu(new_options))
update_button.pack()

root.mainloop()