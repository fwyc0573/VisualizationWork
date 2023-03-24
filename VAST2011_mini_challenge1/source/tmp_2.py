import tkinter
import tkinter.filedialog
from PIL import ImageTk
from torchvision import transforms as transforms
import os
import pandas as pd
import numpy as np
import cv2 as cv
import re
from matplotlib import style
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from tkinter import *
import tkinter.colorchooser
import PIL.Image
import random

# 创建一个界面窗口
win = tkinter.Tk()
win.title("picture process")
win.geometry("1920x1080")


def graphAndMap_show():
    # list_items = [1,2,3]
    # Lstbox1.delete(0, END)
    # for item in list_items:
    #     Lstbox1.insert(END, item)
    # Lstbox1.place(x=850, y=350)
    var = ["E","W","A","S"]
    for i in var:
        t.insert('end',var)
    t.place(x=1000, y=100)


# 设置保存图片的按钮
button2 = tkinter.Button(win, text="开始搜寻",command=graphAndMap_show,font = 16)
button2.place(x=100, y=100)

t = Text(win,height=1)
t.place(x=120, y=760)

#显示Keywords以及对应ID
Lstbox1 = Listbox(win,height=21,width = 95)
Lstbox1.place(x=850, y=350)

win.mainloop()

# weather = [1,0,0,2,2,3,3,3,1,0,0,0,1,3,1,0,1,0,0,1,1]
# windDire = ["E","E","SE","SE","N","N","NW","NNW","NW","NW","WNW","W","N","N","NW","NW","W","W","W","WNW","NW"]
#
# def weatherAndwind(day1,day2):#获取天气和风向
#     weatherRe = []
#     windRe = []
#     for i in range(day1,day2+1):
#         if(weather[i]==0):
#             temp =" "+str(i)+"日" + "天晴"
#             weatherRe.append(temp)
#         elif(weather[i] == 1):
#             temp =" "+str(i) + "日" + "多云"
#             weatherRe.append(temp)
#         elif(weather[i] == 2):
#             temp =" "+str(i) + "日" + "阵雨"
#             weatherRe.append(temp)
#         elif(weather[i] == 3):
#             temp =" "+str(i) + "日" + "有雨"
#             weatherRe.append(temp)

#         windRe.append(windDire[i])
#     print(weatherRe)
#     print(windRe)
#
# weatherAndwind(16,18)