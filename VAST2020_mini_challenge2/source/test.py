
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# from nets.unet import mobilenet_unet
# model = mobilenet_unet(2,416,416)
# model.summary()
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np
import random
import sys
import shutil

from keras.utils.data_utils import get_file
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from PIL import Image
import time
import keras
from keras import backend as K
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

path=r'C:\Users\FYC\Desktop\png'
newpath=r'C:\Users\FYC\Desktop\newpng'

def turnto24(path):
 fileList = []
 files = os.listdir(path)
 i=0
 for f in files:
  imgpath = path + '/' +f
  img=Image.open(imgpath).convert('RGB')
  dirpath = newpath
  file_name, file_extend = os.path.splitext(f)
  print(file_name)
  dst = os.path.join(os.path.abspath(dirpath), file_name + '.png')
  img.save(dst)



def resize(imgPath, savePath):
    m = 110
    n=0
    files = os.listdir(imgPath)
    files.sort()
    print('input :', imgPath)
    for file in files:
        fileType = os.path.splitext(file)
        if(n%12==0):
            m+=5
        new_png = Image.open(imgPath + '/' + file)  # 打开图片
        width = new_png.size[0]  # 长度
        height = new_png.size[1]  # 宽度
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                data = new_png.getpixel((i, j))  # i,j表示像素点
                # print(data[0],data[1],data[2])
                if (data[0] == 128 and data[1] == 0 and data[2] == 0):
                    # print("m=", m)
                    new_png.putpixel((i, j), (m, m, m))  # 颜色改变
        n += 1
        print(fileType[0])
        new_png.save(savePath + '/' + fileType[0] + '.png')  # 保存图片
    print('down!')
    print('****************')

def showRGB():
    new_png = Image.open(r"C:\Users\FYC\Desktop\newColpng\carabiner_1.png")  # 打开图片 115
    width = new_png.size[0]  # 长度
    height = new_png.size[1]  # 宽度
    for i in range(0, width):  # 遍历所有长度的点
        for j in range(0, height):  # 遍历所有宽度的点
            data = new_png.getpixel((i, j))  # i,j表示像素点
            if (data[0] != 0):
                print(data[0], data[1], data[2])
                break
    print('down!')


if __name__ == '__main__':
    list = [0.8, 0.1, 0.24, 1.0, 0.12, 0.2, 1.0, 1.0, 0.36, 0.1, 0.2, 0.72, 0.84, 0.24, 0.36, 0.72, 0.04, 0.1, 0.1, 0.1, 0.1,
     0.1, 0.8, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.08, 1.0, 0.84, 0.1, 0.16, 0.2, 0.1, 0.4, 0.28, 0.08, 0.36, 0.04, 0.08,
     0.24]
    print(sum(list))
    # showRGB()




    # turnto24(path)

    # # 待处理图片地址
    # dataPath = newpath
    # # 保存图片的地址
    # savePath = r'C:\Users\FYC\Desktop\newColpng'
    # resize(dataPath, savePath)
