#统计了5.16、5.17、5.18、5.19、5.20 四天时间的感染人数数据，通过Logistic模型进行预测

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import style

def logistic_increase_function(t,P0,r,K):#Logistic函数
    # t:time   t0:initial time    P0:initial_value    K:capacity  r:increase_rate
    # r = 0.3
    exp_value = np.exp(r * (t))
    return (K * exp_value * P0) / (K + (exp_value - 1) * P0)


def predictAndCur(x,y,futrueArray):
    popt, pcov = curve_fit(logistic_increase_function, x_ori, y_ori)  # 进行拟合
    p0 = popt[0]  # popt里面是拟合系数
    r = popt[1]
    K = popt[2]

    print("p0,r,K", popt)
    # y_predict=logistic_increase_function(x_ori, p0, r, K)#将系数带入,拟合
    y_predict = logistic_increase_function(futrueArray, p0, r, K)  # 将系数带入
    style.use('dark_background')  # 设置画布风格
    plt.scatter(x, y, s=10, c="yellow", alpha=1, marker=(9, 3, 30), label='原始数据')
    plot2 = plt.plot(futrueArray, y_predict, c='teal', linewidth=3, label='拟合曲线')
    plt.xlabel('天数', fontsize=10)
    plt.ylabel('感染人数', fontsize=10)

    plt.legend(loc=4)
    plt.title('Logistic模型预测*Second_Symptoms*感染人数', fontsize=13)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文格式
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()


if __name__ == "__main__":
    x_ori = np.arange(1, 6, 1)  # 对应5天
    y_ori = np.array([183, 369, 5384, 11508, 16361])  # 对应5天的感染人数

    x_ori_2 = np.arange(1, 3, 1)  # 对应2天
    y_ori_2 = np.array([929,4109])  # 对应2天的感染人数
    future = np.linspace(0, 20, 21)  # 预测1个月的情况
    future = np.array(future)
    predictAndCur(x_ori_2,y_ori_2,future)




