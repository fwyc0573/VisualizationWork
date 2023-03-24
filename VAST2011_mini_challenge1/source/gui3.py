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

# 设置图片保存路径
outfile = './out_pic'
graph_adress = r"H:\re\graph.png"
map_adress = r"H:\map.png"
num = 1
# keywords_wholeSymptoms = r'flu|fever|chills|aches|coughing|breathing difficulty|nausea and vomiting|vomiting|diarrhea|enlarged lymph nodes'
# keywords_wholeSymptoms = str(keywords_wholeSymptoms)
# keywords_first = r'flu|fever|chills|aches|coughing|breathing difficulty'#第一类
# keywords_second = r'nausea and vomiting|vomiting|diarrhea'#第二类

src=cv.imread('Vastopolis_Map_2.jpg')
size = src.shape
rows = size[0]
cols = size[1]
N1 = 42.3017
W1 = 93.5673

N2 = 42.1609
W2 = 93.1923
record_index = np.zeros(180465)#为每个ID创建一个用于记录的空间，1为已经被记录，0为仍未被记录,180464为最大ID序号，0不用
record_index_2 = np.zeros(180465)#记录已得第二病症的数组，1为已经被记录，0为仍未被记录,180464为最大ID序号，0作废

path = r'H:\\Microblogs.csv'
data = pd.read_csv(path)
search_day = 20


def reaserchAndDraw(startTimebox,endTimebox,k1,k2):
    # style.use('dark_background')  # 设置画布风格
    list_items = []#关键信息记录数组
    fig = plt.figure(figsize=(24, 12))  # 调整画图空间的大小
    start = datetime.datetime(2011, startTimebox[0], startTimebox[1])
    stop = datetime.datetime(2011, endTimebox[0], endTimebox[1]+1)
    delta = datetime.timedelta(1 / 4)  # 设定日期的间隔
    dates = mpl.dates.drange(start, stop, delta)  # 返回浮点型的日期序列，这个是生成时间序列

    infect_1 = [0 for i in range(len(dates))]  # 第一类初始化感染人数
    infect_2 = [0 for i in range(len(dates))]  # 第一类初始化感染人数

    for i in range(len(data['ID'])):
        try:  # hour处经过debug发现有许多带有非时间的信息
            hour = int(data['Created_at'][i].split(" ")[1].split(":")[0])
        except:
            continue
        day = int(data['Created_at'][i].split(" ")[0].split("/")[-1])
        month = int(data['Created_at'][i].split(" ")[0].split("/")[1])
        id = int(data['ID'][i])
        if (day < startTimebox[1] and month == 5):  # 在统计天数之前的；保证搜寻日期病症为当天新增病例，排除多日发送含有关键字的信息
            if (record_index[id] == 0):  # 未得过第一症状
                matchResult = re.findall(k1, str(data['text'][i]), re.IGNORECASE)  # 匹配第一类
                if (matchResult != None and matchResult != []):
                    record_index[id] = 1  # 刷新记录数组
            if (record_index_2[id] == 0):  # 未得过第二症状
                matchResult_2 = re.findall(k2, str(data['text'][i]), re.IGNORECASE)  # 匹配第一类
                if (matchResult_2 != None and matchResult_2 != []):
                    record_index_2[id] = 1  # 刷新记录数组

        elif (endTimebox[1]>day>startTimebox[1] or (endTimebox[1]==day and endTimebox[2]>=hour) or (startTimebox[1]==day and startTimebox[2]<=hour)):  # 只统计5.17号开始的数据 06,612,12,18,18,24
            if (record_index[id] == 0):  # 未得过第一症状
                matchResult = re.findall(k1, str(data['text'][i]), re.IGNORECASE)
                if (matchResult != None and matchResult != []):  # 存在1类关键信息
                    try:
                        latitude = float(data['Location'][i].split(" ")[1])  # 经度W
                        longitude = float(data['Location'][i].split(" ")[0])  # 纬度N
                        position_x = round((W1 - latitude) / 0.375 * cols)
                        position_y = round((N1 - longitude) / 0.1408 * rows)
                        print(position_x, position_y)
                        # cv.circle(src, (position_x, position_y), 2, (134, 51, 196), 1)  # 画点
                        cv.circle(src, (position_x, position_y), 2, (50, 131, 228), 1)  # 画点
                        infect_1[(day - startTimebox[1]) * 4 + hour // 6] += 1
                        #记录text
                        record_index[id] = 1  # 刷新记录数组
                    except:
                        continue
                    words_item = "ID:" + str(data['ID'][i]) + " " + data['text'][i]
                    print(words_item)
                    list_items.append(words_item)
            if (record_index_2[id] == 0):  # 未得过第二症状
                matchResult_2 = re.findall(k2, str(data['text'][i]), re.IGNORECASE)  # 未得过第一症状
                if (matchResult_2 != None and matchResult_2 != []):  # 存在2类关键信息
                    try:
                        latitude = float(data['Location'][i].split(" ")[1])  # 经度W
                        longitude = float(data['Location'][i].split(" ")[0])  # 纬度N
                        position_x = round((W1 - latitude) / 0.375 * cols)
                        position_y = round((N1 - longitude) / 0.1408 * rows)
                        print(position_x, position_y)
                        # cv.circle(src, (position_x, position_y), 2, (134, 51, 196), 1)  # 画点
                        cv.circle(src, (position_x, position_y), 2, (97, 97, 254), 1)  # 画点
                        infect_2[(day - startTimebox[1]) * 4 + hour // 6] += 1
                        # 记录text

                        record_index_2[id] = 1  # 刷新记录数组
                    except:
                        continue
                    words_item = "ID:" + str(data['ID'][i]) + " " + data['text'][i]
                    print(words_item)
                    list_items.append(words_item)

    # cv.imshow('input_image', src)
    cv.imwrite(map_adress, src)

    plt.title("The Number of  People With Symptoms  Stack Plot",fontsize=25)
    dayX = np.linspace(0, len(dates) - 1, len(dates))

    plt.xticks(dayX, fontsize=18)
    plt.yticks(infect_1, fontsize=18)
    plt.bar(dayX, infect_1, color='orange', label='First')
    plt.bar(dayX, infect_2, bottom=infect_1, color='palevioletred', label='Second')
    plt.xlabel('Time', fontsize=20)  # X轴标签
    plt.ylabel("Number", fontsize=20)  # Y轴标签
    plt.legend(loc="upper left", fontsize=20)
    # plt.show()
    plt.savefig(graph_adress)
    # 显示过滤得到的具体推特和ID
    global Lstbox1
    print("LENGTH:",len(list_items))
    Lstbox1.delete(0, END)
    for item in list_items:
        Lstbox1.insert(END, item)
    Lstbox1.place(x=850, y=350)

def graphAndMap_show():
    #处理获得图表和图片并存到硬盘
    start = inp1.get()
    end = inp2.get()
    k_1 = str(inp3.get())
    k_2 = str(inp4.get())
    startTimebox = [int(i) for i in start.split(".")]
    endTimebox = [int(i) for i in end.split(".")]

    # startTimebox = [5,18,0]
    # endTimebox = [5,20,9]
    reaserchAndDraw(startTimebox,endTimebox,k_1,k_2)


    #读取硬盘上对应的图片，进行显示
    temp = PIL.Image.open(graph_adress)
    new_im = transforms.Resize((360,800))(temp)
    render_graph = ImageTk.PhotoImage(new_im)
    temp = PIL.Image.open(map_adress)
    new_im = transforms.Resize((406,800))(temp)
    render_map = ImageTk.PhotoImage(new_im)
    #graph
    global img_g
    img_g.destroy()
    img_g = tkinter.Label(win, image=render_graph)
    img_g.image = render_graph
    img_g.place(x=10, y=-34)

    #map
    global img_m
    img_m.destroy()
    img_m = tkinter.Label(win, image=render_map)
    img_m.image = render_map
    img_m.place(x=10, y=340)

    #显示天气情况
    weatherAndwind(startTimebox[1], endTimebox[1])

def delt():#删除记录
    global Lstbox1
    if Lstbox1.curselection() != ():
        Lstbox1.delete(Lstbox1.curselection())

def weatherAndwind(day1,day2):#获取天气和风向
    weatherRe = []
    windRe = []
    for i in range(day1,day2+1):
        if(weather[i]==0):
            temp =" "+str(i)+"日" + "天晴"
            weatherRe.append(temp)
        elif(weather[i] == 1):
            temp =" "+str(i) + "日" + "多云"
            weatherRe.append(temp)
        elif(weather[i] == 2):
            temp =" "+str(i) + "日" + "阵雨"
            weatherRe.append(temp)
        elif(weather[i] == 3):
            temp =" "+str(i) + "日" + "有雨"
            weatherRe.append(temp)
        temp = " "+str(i) + "日" + windDire[i]
        windRe.append(temp)
    print(weatherRe)
    print(windRe)
    global t1
    global t2
    for i in weatherRe:
        t1.insert('end',i)
    t1.place(x=130, y=752)
    for i in windRe:
        t2.insert('end',i)
    t2.place(x=550, y=752)

#透视模式
def toushiModel():
    global num
    global sub_adress
    num+=1
    ori = cv.imread(sub_adress)
    after = cv.imread(map_adress)
    save_path = r"H:\re\Vastopolis_Map_2.jpg"
    if num%2 == 0:
        image = cv.subtract(after, ori)
        cv.imwrite(save_path, image)
        temp = PIL.Image.open(save_path)
        new_im = transforms.Resize((406, 800))(temp)
        render_map = ImageTk.PhotoImage(new_im)
        global img_m
        img_m.destroy()
        img_m = tkinter.Label(win, image=render_map)
        img_m.image = render_map
        img_m.place(x=10, y=340)
    if num % 2 != 0:
        temp = PIL.Image.open(map_adress)
        new_im = transforms.Resize((406, 800))(temp)
        render_map = ImageTk.PhotoImage(new_im)
        img_m.destroy()
        img_m = tkinter.Label(win, image=render_map)
        img_m.image = render_map
        img_m.place(x=10, y=340)

#选择被减的图象
def loadPic():
    global sub_adress
    global img_m
    select_file = tkinter.filedialog.askopenfilename(title='选择图片')
    sub_adress = select_file
    load = PIL.Image.open(sub_adress)
    load = transforms.Resize((406, 800))(load)
    render = ImageTk.PhotoImage(load)
    img_m.destroy()
    img_m = tkinter.Label(win, image=render)
    img_m.image = render
    img_m.place(x=10, y=340)


# 创建一个界面窗口
win = tkinter.Tk()
win.title("VAST 2011挑战")
win.geometry("1920x1080")

# 设置全局变量
img_g = tkinter.Label(win)
img_m = tkinter.Label(win)

# 风向和天气情况文字显示：0-晴天clear；1-多云cloudy；2-阵雨showers；3-有雨rain；
weather = [1,0,0,2,2,3,3,3,1,0,0,0,1,3,1,0,1,0,0,1,1]
windDire = ["E","E","SE","SE","N","N","NW","NNW","NW","NW","WNW","W","N","N","NW","NW","W","W","W","WNW","NW"]
label1 = tkinter.Label(win, text="天气情况：")
label1.place(x=70, y=750)
label2 = tkinter.Label(win, text="具体风向：")
label2.place(x=480, y=750)

t1 = Text(win,height=1,width=45)
t1.place(x=130, y=752)
t2 = Text(win,height=1,width=45)
t2.place(x=550, y=752)


#显示Keywords以及对应ID
Lstbox1 = Listbox(win,height=21,width = 95)
Lstbox1.place(x=850, y=350)

#开始结束时间自定义设定
lb1 = Label(win, text='开始时间:',font = 16)
lb1.place(x=850, y=50)
lb2 = Label(win, text='结束时间:',font = 16)
lb2.place(x=850, y=120)

inp1 = Entry(win)
inp1.place(x=950, y=54)
inp2 = Entry(win)
inp2.place(x=950, y=124)

#特征关键词自定义
lb3 = Label(win, text='特征1关键词:',font = 16)
lb3.place(x=1150, y=50)
lb4 = Label(win, text='特征2关键词:',font = 16)
lb4.place(x=1150, y=120)

inp3 = Entry(win)
inp3.place(x=1275, y=54)
inp4 = Entry(win)
inp4.place(x=1275, y=124)


# 设置保存图片的按钮
button1 = tkinter.Button(win, text="开始搜寻",command=graphAndMap_show,font = 16)
button1.place(x=900, y=240)


# 设置退出按钮
button0 = tkinter.Button(win, text="退出系统", command=win.quit,font = 16)
button0.place(x=1100, y=240)

# 设置透视模式
button3 = tkinter.Button(win, text="透视模式", command=toushiModel,font = 16)
button3.place(x=1300, y=240)

# 设置选择图片按键
button4 = tkinter.Button(win, text="选择图片",command=loadPic,font = 16)
button4.place(x=1000, y=740)
sub_adress = r"H:\re\Vastopolis_Map_2.jpg"

# 设置删除选中记录的按钮
button2 = tkinter.Button(win, text="删除选中记录",command=delt,font = 16)
button2.place(x=1330, y=740)

win.mainloop()

