from tkinter import *
from PIL import Image, ImageTk
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
# root = Tk()
# cv = Canvas(root, bg='white', width=500, height=650)
# rt = cv.create_rectangle(10, 10, 110, 110, outline='red', stipple='gray12', fill='green')
# img = PhotoImage(file=r'H:\re\detail_above516.png')
# img = img.resize((20, 100), Image.ANTIALIAS)
# cv.create_image((20 * 1, 200 * 1), image=img)
# cv.pack()
# root.mainloop()

# startTimebox = [5, 20, 0]
# endTimebox = [5, 20, 12]
#
# start = datetime.datetime(2011, startTimebox[0], startTimebox[1])
# stop = datetime.datetime(2011, endTimebox[0], endTimebox[1])
# delta = datetime.timedelta(1)  # 设定日期的间隔
# dates = mpl.dates.drange(start, stop, delta)  # 返回浮点型的日期序列，这个是生成时间序列
# print(dates)
# x = [1,2,3,4]
# y = [100,300,200,42]
# plt.bar(x, y,  color='#c07ec2', label='Water')
#
# plt.xlabel('Time', fontsize=13)  # X轴标签
# plt.ylabel("Number", fontsize=13)  # Y轴标签
# plt.legend(loc="upper left", fontsize=10)
# plt.show()
k_1 = "5.20.3"
startTimebox = [int(i) for i in k_1.split(".")]
print(startTimebox)
