#将时间片切片，统计5.17、5.18、5.19、5.20 四天时间的感染人数在地图上的分布

import cv2 as cv
import re
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import csv
import pandas as pd
import numpy as np


keywords_wholeSymptoms = r'flu|fever|chills|aches|coughing|breathing difficulty|nausea and vomiting|vomiting|diarrhea|enlarged lymph nodes'
keywords_wholeSymptoms = str(keywords_wholeSymptoms)

keywords_first = r'flu|fever|chills|aches|coughing|breathing difficulty'#第一类
keywords_second = r'nausea and vomiting|vomiting|diarrhea'#第二类

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
for i in range(len(data['ID'])):
    try:  # hour处经过debug发现有许多带有非时间的信息
        hour = int(data['Created_at'][i].split(" ")[1].split(":")[0])
    except:
        continue
    day = int(data['Created_at'][i].split(" ")[0].split("/")[-1])
    month = int(data['Created_at'][i].split(" ")[0].split("/")[1])
    id = int(data['ID'][i])
    if (day < search_day and month == 5):#在统计天数之前的；保证搜寻日期病症为当天新增病例，排除多日发送含有关键字的信息
        if(record_index[id] == 0):#未得过第一症状
            matchResult = re.findall(keywords_first, str(data['text'][i]), re.IGNORECASE)  # 匹配第一类
            if (matchResult != None and matchResult != []):
                record_index[id] = 1  # 刷新记录数组
        if(record_index_2[id] == 0):#未得过第二症状
            matchResult_2 = re.findall(keywords_second, str(data['text'][i]), re.IGNORECASE)  # 匹配第一类
            if (matchResult_2 != None and matchResult_2 != []):
                record_index_2[id] = 1  # 刷新记录数组

    elif(day==search_day and month == 5 and (12<=hour<24)):#只统计5.17号开始的数据 06,612,12,18,18,24
        if(record_index[id] == 0):#未得过第一症状
            matchResult = re.findall(keywords_first, str(data['text'][i]), re.IGNORECASE)
            if (matchResult != None and matchResult != []):  # 存在1类关键信息
               try:
                latitude = float(data['Location'][i].split(" ")[1])  # 经度W
                longitude = float(data['Location'][i].split(" ")[0])  # 纬度N
                position_x = round((W1 - latitude) / 0.375 * cols)
                position_y = round((N1 - longitude) / 0.1408 * rows)
                print(position_x, position_y)
                # cv.circle(src, (position_x, position_y), 2, (134, 51, 196), 1)  # 画点
                cv.circle(src, (position_x, position_y), 2, (50, 131, 228), 1)  # 画点
                record_index[id] = 1  # 刷新记录数组
               except:
                   continue
        if (record_index_2[id] == 0):  # 未得过第二症状
            matchResult_2 = re.findall(keywords_second, str(data['text'][i]), re.IGNORECASE)  #未得过第一症状
            if (matchResult_2 != None and matchResult_2 != []):  # 存在2类关键信息
                try:
                    latitude = float(data['Location'][i].split(" ")[1])  # 经度W
                    longitude = float(data['Location'][i].split(" ")[0])  # 纬度N
                    position_x = round((W1 - latitude) / 0.375 * cols)
                    position_y = round((N1 - longitude) / 0.1408 * rows)
                    print(position_x, position_y)
                    # cv.circle(src, (position_x, position_y), 2, (134, 51, 196), 1)  # 画点
                    cv.circle(src, (position_x, position_y), 2, (97, 97, 254), 1)  # 画点
                    record_index_2[id] = 1  # 刷新记录数组
                except:
                    continue
# cv.namedWindow('input_image', cv.WINDOW_AUTOSIZE)
# cv.imshow('input_image', src)
cv.imwrite(r"H:\5.20_12to24.jpg", src)
cv.waitKey(0)
cv.destroyAllWindows()