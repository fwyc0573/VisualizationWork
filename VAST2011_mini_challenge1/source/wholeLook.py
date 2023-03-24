#总体上先进行疫情爆发的时间点的确定以便后续缩小探究范围
import re
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import csv
import pandas as pd
import numpy as np
from matplotlib import style


fig = plt.figure(figsize=(24, 12))  # 调整画图空间的大小
style.use('dark_background')  # 设置画布风格
path = r'H:\\Microblogs.csv'

# 患病关键词
keywords_wholeSymptoms = r'flu|fever|chills|aches|coughing|breathing difficulty|nausea and vomiting|vomiting|diarrhea|enlarged lymph nodes'

start = datetime.datetime(2011, 4, 30)
stop = datetime.datetime(2011, 5, 21)
delta = datetime.timedelta(1/4)  # 设定日期的间隔
dates = mpl.dates.drange(start, stop, delta)  # 返回浮点型的日期序列，这个是生成时间序列
infectPeople = [0 for i in range(len(dates))]#初始化感染人数


record_index = np.zeros(180465)#为每个ID创建一个用于记录的空间，1为已经被记录，0为仍未被记录,180464为最大ID序号，0不用
data = pd.read_csv(path)

for i in range(len(data['ID'])):
    id = int(data['ID'][i])
    if(record_index[id] == 0):
        try:
          matchResult = re.findall(keywords_wholeSymptoms, str(data['text'][i]), re.IGNORECASE)
        except:
            continue
        if ( matchResult != None and matchResult !=[]):  # 存在关键信息
            month = int(data['Created_at'][i].split(" ")[0].split("/")[1])
            day = int(data['Created_at'][i].split(" ")[0].split("/")[-1])
            try:  # hour处经过debug发现有许多带有非时间的信息
                hour = int(data['Created_at'][i].split(" ")[1].split(":")[0])
                print(month, day,hour)
            except:
                continue
            record_index[id] = 1  # 刷新记录数组
            if (day != 30):  # 即是5月份
                infectPeople[day * 4 + hour // 6] += 1
                # print(day*4+hour//6)
            else:  # 是4月30号
                infectPeople[hour // 6] += 1
            print(data['ID'][i],":",data['text'][i])
plt.title("The Number of  People With Symptoms  Stack Plot")
dayX = np.linspace(1, 84, 84)
plt.bar(dayX, infectPeople, linestyle='-', color = 'steelblue')  # 作图
plt.xlabel('Time', fontsize=13)  # X轴标签
plt.ylabel("Number", fontsize=13)  # Y轴标签
plt.legend(loc="upper left", fontsize=10)
plt.show()