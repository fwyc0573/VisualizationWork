#总体上先进行疫情爆发的时间点的确定以便后续缩小探究范围
import re
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import csv
import pandas as pd
import numpy as np
from matplotlib import style

# mystring = 'some string We '
keywords_wholeSymptoms = r'flu|fever|chills|aches|coughing|breathing difficulty|nausea and vomiting|vomiting|diarrhea|enlarged lymph nodes'
keywords_first = r'flu|fever|chills|aches|coughing|breathing difficulty'#第一类
keywords_second = r'nausea and vomiting|vomiting|diarrhea'#第二类

style.use('dark_background')  # 设置画布风格
fig = plt.figure(figsize=(24, 12))  # 调整画图空间的大小

start = datetime.datetime(2011, 5, 16)
stop = datetime.datetime(2011, 5, 21)
delta = datetime.timedelta(1/4)  # 设定日期的间隔
dates = mpl.dates.drange(start, stop, delta)  # 返回浮点型的日期序列，这个是生成时间序列
# infectPeople = [0 for i in range(len(dates))]#初始化感染人数
infect_1 = [0 for i in range(len(dates))]#第一类初始化感染人数
infect_2 = [0 for i in range(len(dates))]#第一类初始化感染人数

path = r'H:\\Microblogs.csv'
record_index = np.zeros(180465)#记录已得第一病症的数组，1为已经被记录，0为仍未被记录,180464为最大ID序号，0作废
record_index_2 = np.zeros(180465)#记录已得第二病症的数组，1为已经被记录，0为仍未被记录,180464为最大ID序号，0作废
data = pd.read_csv(path)

for i in range(len(data['ID'])):
    day = int(data['Created_at'][i].split(" ")[0].split("/")[-1])
    month = int(data['Created_at'][i].split(" ")[0].split("/")[1])
    id = int(data['ID'][i])
    if(day>=16 and month == 5):#时间满足要求
      if(record_index[id] == 0):#未得过第一病症
        matchResult = re.findall(keywords_first, str(data['text'][i]), re.IGNORECASE)
        if ( matchResult != None and matchResult !=[]):  # 存在1类关键信息
            try:  # hour处经过debug发现有许多带有非时间的信息
                hour = int(data['Created_at'][i].split(" ")[1].split(":")[0])
            except:
                continue
            record_index[id] = 1  # 刷新记录数组
            infect_1[(day-16) * 4 + hour // 6] += 1
      if(record_index_2[id] == 0):#未得过第二病症
        matchResult_2 = re.findall(keywords_second, str(data['text'][i]), re.IGNORECASE)
        if (matchResult_2 != None and matchResult_2 != []):  # # 存在2类关键信息
             try:
                 hour = int(data['Created_at'][i].split(" ")[1].split(":")[0])
             except:
                 continue
                 record_index_2[id] = 1  # 刷新记录数组
             try:
               infect_2[(day-16) * 4 + hour // 6] += 1
             except:
                 break


plt.title("The Number of  People With Symptoms  Stack Plot")
dayX = np.linspace(0, len(dates)-1, len(dates))
# plt.plot(dayX, infectPeople, linestyle='-', c='rosybrown')  #总体作图
plt.bar(dayX, infect_1, color='gray', label='Air')
plt.bar(dayX, infect_2, bottom=infect_1, color='blue', label='Water')

plt.xlabel('Time', fontsize=13)  # X轴标签
plt.ylabel("Number", fontsize=13)  # Y轴标签
plt.legend(loc="upper left", fontsize=10)
plt.show()

print("5.16:",sum([i for i in infect_1 ][0:4]))
print("5.17:",sum([i for i in infect_1 ][4:8]))
print("5.18:",sum([i for i in infect_1 ][8:12]))
print("5.19:",sum([i for i in infect_1 ][12:16]))
print("5.20:",sum([i for i in infect_1 ][16:20]))
print("-------------------------------------------------")
print("5.16:",([i for i in infect_2 ][0:4]))
print("5.17:",([i for i in infect_2 ][4:8]))
print("5.18:",([i for i in infect_2 ][8:12]))
print("5.19:",([i for i in infect_2 ][12:16]))
print("5.20:",([i for i in infect_2 ][16:20]))