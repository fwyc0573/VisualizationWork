from PIL import Image,ImageFilter,ImageEnhance
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import os
import random
NCLASSES = 2
HEIGHT = 416
WIDTH = 416

def letterbox_image(image, size, type):
    iw, ih = image.size
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    image = image.resize((nw,nh), Image.BICUBIC)
    if(type=="jpg"):
        new_image = Image.new('RGB', size, (0,0,0))
    elif(type=="png"):
        new_image = Image.new('RGB', size, (0,0,0))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    return new_image,nw,nh

def rand(a=0, b=1):
    return np.random.rand()*(b-a) + a
    
def get_random_data(image, label, input_shape, jitter=.2, hue=.2, sat=1.1, val=1.1):
    h, w = input_shape
    # resize image
    rand_jit1 = rand(1-jitter,1+jitter)
    rand_jit2 = rand(1-jitter,1+jitter)
    new_ar = w/h * rand_jit1/rand_jit2
    scale = rand(.8, 1.2)
    if new_ar < 1:
        nh = int(scale*h)
        nw = int(nh*new_ar)
    else:
        nw = int(scale*w)
        nh = int(nw/new_ar)
    image = image.resize((nw,nh), Image.BICUBIC)
    label = label.resize((nw,nh), Image.BICUBIC)
    # place image
    dx = int(rand(0, w-nw))
    dy = int(rand(0, h-nh))
    new_image = Image.new('RGB', (w,h), (0,0,0))
    new_label = Image.new('RGB', (w,h), (0,0,0))
    new_image.paste(image, (dx, dy))
    new_label.paste(label, (dx, dy))
    image = new_image
    label = new_label

    # flip image or not
    flip_lr = rand()<.3
    if flip_lr:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        label = label.transpose(Image.FLIP_LEFT_RIGHT)
    flip_updown = rand()<.3
    if flip_updown:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        label = label.transpose(Image.FLIP_TOP_BOTTOM)

    #rotate
    rotate = rand()<.2
    if rotate:
        angle = np.random.randint(0, 360)
        image = image.rotate(angle)
        label = label.rotate(angle)
        print("angle:", angle)

    #blur
    blur = rand()<.3
    if blur:
        image.filter(ImageFilter.BLUR)

    # brightness
    brightness = rand() < .99
    if brightness:
        image_brightness = ImageEnhance.Brightness(image)#获取亮度调整周期
        bri = random.uniform(0.5,1.5)
        image = image_brightness.enhance(bri)

    # distort image
    hue = rand(-hue, hue)
    sat = rand(1, sat) if rand()<.1 else 1/rand(1, sat)
    val = rand(1, val) if rand()<.1 else 1/rand(1, val)

    x = rgb_to_hsv(np.array(image)/255.)
    x[..., 0] += hue
    x[..., 0][x[..., 0]>1] -= 1
    x[..., 0][x[..., 0]<0] += 1
    x[..., 1] *= sat
    x[..., 2] *= val
    x[x>1] = 1
    x[x<0] = 0
    image_data = hsv_to_rgb(x)
    return image_data,label


def Generate_get_random_data(image, input_shape, jitter=.05, hue=.05, sat=1.1, val=1.1):
    h, w = input_shape

    rand_jit1 = rand(1-jitter,1+jitter)
    rand_jit2 = rand(1-jitter,1+jitter)
    new_ar = w/h * rand_jit1/rand_jit2
    scale = rand(.95, 1.1)
    if new_ar < 1:
        nh = int(scale*h)
        nw = int(nh*new_ar)
    else:
        nw = int(scale*w)
        nh = int(nw/new_ar)
    image = image.resize((nw,nh), Image.BICUBIC)

    dx = int(rand(0, w-nw))
    dy = int(rand(0, h-nh))
    new_image = Image.new('RGB', (w,h), (0,0,0))
    new_image.paste(image, (dx, dy))
    image = new_image

    flip_lr = rand()<.3
    if flip_lr:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    flip_updown = rand()<.3
    if flip_updown:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return image


def GenerateIMG(Classname):
    #随机选择图象进行增强
    list = os.listdir(r"C:\Users\FYC\Desktop\Answer2\Answer2/"+Classname)
    num = len(list)
    print("该类已有图象的数量为：",num)
    i = 0
    for filePic in list:
        if(filePic!="Thumbs.db"):
            # 从文件中读取图像
            jpg = Image.open(r"C:\Users\FYC\Desktop\Answer2\Answer2/" + Classname + "/" + filePic)

            jpg = Generate_get_random_data(jpg, [WIDTH, HEIGHT])
            newJpgName = r"C:\Users\FYC\Desktop\Answer2\Answer2/" + Classname + r"/" + '_' + str(i) + ".jpg"

            print("写入文件路径:", newJpgName)
            Image.fromarray(np.uint8(jpg * 255)).save(newJpgName, quality=95)
            i += 1




def strongIMG(filepath,Classname):
    #随机选择10张图象进行增强
    list = os.listdir(r".\dataset2/"+Classname)
    num = len(list)
    print("该类已有图象的数量为：",num)
    with open(filepath,"r") as f:#读取对应txt文件
        lines = f.readlines()
    with open(filepath, "a") as f:  # 读取对应txt文件
        # lines = f.readlines()
        # 打乱行
        np.random.seed(10101)
        np.random.shuffle(lines)
        np.random.seed(None)
        i = 0
        while i < 10:
            index = num + i + 1
            name = lines[i].split(';')[0]
            # 从文件中读取图像
            print(i)
            # jpg = Image.open(r".\dataset2\jpg" + '/' + name)
            jpg = Image.open(r".\dataset2/" + Classname + '/' + name)

            name = (lines[i].split(';')[1]).replace("\n", "")
            # 从文件中读取图像
            # png = Image.open(r".\dataset2\png" + '/' + name)
            png = Image.open(r".\dataset2/" + Classname + 'PNG/' + name)

            jpg, png = get_random_data(jpg, png, [WIDTH, HEIGHT])
            # newJpgName = r".\dataset2\jpg" + r"/" + name.split('_')[0] + '_' + str(index) + ".jpg"
            # newPngName = r".\dataset2\png" + r"/" + name.split('_')[0] + '_' + str(index) + ".png"

            newJpgName = r".\dataset2/" + Classname + r"/" + name.split('_')[0] + '_' + str(index) + ".jpg"
            newPngName = r".\dataset2/" + Classname + 'PNG/'+r"/" + name.split('_')[0] + '_' + str(index) + ".png"

            # 将jpg,png加入到对应文件夹中
            print("写入文件路径:", newJpgName)
            Image.fromarray(np.uint8(jpg * 255)).save(newJpgName, quality=95)
            Image.fromarray(np.uint8(png)).save(newPngName, quality=95)

            # 尾部追加到对应的txt文件
            f.write( name.split('_')[0] + '_' + str(index) + ".jpg" + ";" + name.split('_')[0] + '_' + str(index) + ".png" + "\n")
            i += 1


if __name__ == '__main__':
    strongNum = 8#增强的迭代次数，每代生成10张
    with open(r"C:\Users\FYC\Desktop\allKinds.txt","r") as f:#读取对应txt文件
        lines = f.readlines()
    # for index in range(len(lines)):
    #     for i in range(strongNum):
    #         txtName = r".\dataset2/" + lines[index].strip() + ".txt"
    #         strongIMG(txtName,lines[index].strip())


    #通过简单的变换处理来生成更多的测试图象评估模型
    for index in range(len(lines)):
        for i in range(3):
            GenerateIMG(lines[index].strip())

    # jpg = Image.open(r"G:\dataVis\MC2-Image-Data\TrainingImages\birdCall\birdCall\birdCall_3.jpg")
    # png = Image.open(r"G:\dataVis\MC2-Image-Data\TrainingImages\birdCall\out\3\label.png")

    # 数据预处理
    # jpg,_,_ = letterbox_image(jpg,[512,512],"jpg")
    # png,_,_ = letterbox_image(png,[512,512],"png")
    # jpg.show()
    # png.show()

    # 数据增强
    # jpg, png = get_random_data(jpg, png, [512, 512])
    # Image.fromarray(np.uint8(jpg * 255)).show()
    # Image.fromarray(np.uint8(png)).show()
    f.close()