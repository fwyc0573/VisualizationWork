from tkinter import *
import tkinter as tk
from torchvision import transforms as transforms
def run1():
     a = float(inp1.get())
     b = float(inp2.get())
     s = '%0.2f+%0.2f=%0.2f\n' % (a, b, a + b)
     txt.insert(END, s)   # 追加显示运算结果
     inp1.delete(0, END)  # 清空输入
     inp2.delete(0, END)  # 清空输入

def run2(x, y):
     a = float(x)
     b = float(y)
     s = '%0.2f+%0.2f=%0.2f\n' % (a, b, a + b)
     txt.insert(END, s)   # 追加显示运算结果
     inp1.delete(0, END)  # 清空输入
     inp2.delete(0, END)  # 清空输入

root = Tk()
root.geometry("1280x1080")
root.title('简单加法器')

#增加背景图片
photo = tk.PhotoImage(file=r"H:\re\predict_sym1.png")
# photo = transforms.Resize((200, 180))(photo)
theLabel = tk.Label(root,#内容
justify=tk.LEFT,#对齐方式
image=photo,#加入图片
compound = tk.CENTER,#关键:设置为背景图片
font=("华文行楷",20),#字体和字号
fg = "white")#前景色
theLabel.pack()



lb1 = Label(root, text='请输入两个数，按下面两个按钮之一进行加法计算')
lb1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)
inp1 = Entry(root)
inp1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)
inp2 = Entry(root)
inp2.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.1)

# 方法-直接调用 run1()
btn1 = Button(root, text='方法一', command=run1)
btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)

# 方法二利用 lambda 传参数调用run2()
btn2 = Button(root, text='方法二', command=lambda: run2(inp1.get(), inp2.get()))
btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)

# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
txt = Text(root)
txt.place(rely=0.6, relheight=0.4)





root.mainloop()
