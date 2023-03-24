from nets.unet import mobilenet_unet
from PIL import Image
import numpy as np
import random
import copy
import os
import cv2
from imgChange import letterbox_image,get_random_data,rand

# import tensorflow.compat.v1 as tf
# from keras import backend as K
# tf.disable_v2_behavior()
# config = tf.ConfigProto()
# config.gpu_options.allow_growth=True
# sess = tf.Session(config=config)
# K.set_session(sess)



random.seed(0)
class_colors = [[0,0,0],[0,255,0]]
NCLASSES = 2
HEIGHT = 416
WIDTH = 416

#无滑动窗口计数
def CheckRight():
    model = mobilenet_unet(n_classes=NCLASSES, input_height=HEIGHT, input_width=WIDTH)
    with open(r"C:\Users\FYC\Desktop\allKinds.txt","r") as f:#读取对应txt文件
        lines = f.readlines()
    proList = []
    for model_line in range(len(lines)):
        print("此时检测的是：", lines[model_line].strip())
        Classname = lines[model_line].strip()
        modelPath = "logs/" + lines[model_line].strip() + ".h5"
        print(modelPath)
        model.load_weights(modelPath)  # 权重导入
        list = os.listdir(r"C:\Users\FYC\Desktop\Answer2\Answer2/" + Classname)
        sum = len(list) - 1
        rightNum = 0
        for filePic in list:
            if (filePic != "Thumbs.db"):
                # 从文件中读取图像
                img = Image.open(r"C:\Users\FYC\Desktop\Answer2\Answer2/" + Classname + "/" + filePic)
                old_img = copy.deepcopy(img)
                orininal_h = np.array(img).shape[0]
                orininal_w = np.array(img).shape[1]
                if (orininal_w != WIDTH or orininal_h != HEIGHT):
                    # 进行边界填充，防止形变失真
                    img, _, _ = letterbox_image(img, (WIDTH, HEIGHT), "jpg")
                img = img.resize((WIDTH, HEIGHT))
                img = np.array(img)
                img = img / 255
                img = img.reshape(-1, HEIGHT, WIDTH, 3)
                pr = model.predict(img)[0]  # 进行预测

                count = 0  # 物体像素点数量
                temp_sum = 0.0  # 物体像素点置信度总和
                for i in range(pr.shape[0]):
                    if pr[i][1] > pr[i][0]:
                        temp_sum += pr[i][1]
                        count += 1
                if (count > 15):  # 发现obj，进行计数
                    rightNum+=1
        if(rightNum!=0):
            proList.append(float(rightNum / sum))
        else:
            proList.append(0)
        print("完成该文件图片的遍历")  # 完成全文件图片的遍历
    print("proList:",proList)


#进行不同模型条件下的图象批量分类统计
def CountGO():
    model = mobilenet_unet(n_classes=NCLASSES, input_height=HEIGHT, input_width=WIDTH)
    with open(r"C:\Users\FYC\Desktop\allKinds.txt","r") as f:#读取对应txt文件
        lines = f.readlines()
    with open(r".\record2.txt", "a+") as t:  # 进行信息记录
        for model_line in range(len(lines)):
            print("此时检测的是：", lines[model_line].strip())

            modelPath = "logs/" + lines[model_line].strip() + ".h5"
            print(modelPath)
            model.load_weights(modelPath)  # 权重导入
            for root, dirs, files in os.walk(r"G:\dataVis\TrainingImages/"):#     G:\dataVis\MC2-Image-Data/
                fenge = files[0].strip("_")
                if (lines[model_line].strip() == fenge[0]):
                    break
                for i in range(len(files)):
                    if (files[i][-3:] == 'jpg'):
                        # print("root:",root)
                        # print("files:", files)
                        file_path = root + '/' + files[i]  # 图片path
                        personID = files[i].split("_")[0]  # 对应嫌疑人ID
                        print(file_path)
                        # 从文件中读取图像
                        img = Image.open(file_path)
                        # 记录长宽
                        old_img = copy.deepcopy(img)
                        orininal_h = np.array(img).shape[0]
                        orininal_w = np.array(img).shape[1]
                        if (orininal_w != WIDTH or orininal_h != HEIGHT):
                            # 进行边界填充，防止形变失真
                            img, _, _ = letterbox_image(img, (WIDTH, HEIGHT), "jpg")
                        img = img.resize((WIDTH, HEIGHT))
                        img = np.array(img)
                        img = img / 255
                        img = img.reshape(-1, HEIGHT, WIDTH, 3)
                        pr = model.predict(img)[0]  # 进行预测

                        count = 0  # 物体像素点数量
                        temp_sum = 0.0  # 物体像素点置信度总和
                        for i in range(pr.shape[0]):
                            if pr[i][1] > pr[i][0]:
                                temp_sum += pr[i][1]
                                count += 1
                        if(count!=0):
                            confidence = temp_sum / count  # 计算平均像素置信度
                        else:
                            confidence = 0
                        print("总数：", count)
                        # print("置信度：", confidence)
                        # print("占比：w", float(count / pr.shape[0]))
                        if (count > 50):  # 发现obj，进行计数
                            print("写入文本，",personID + ";" + lines[model_line].strip()+";" +str(confidence) + "\n")
                            t.write(personID + ";" + lines[model_line].strip()+";" +str(confidence) + "\n")
                            t.flush()
        print("完成全文件图片的遍历")#完成全文件图片的遍历
    t.close()
    f.close()


def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize[1]):
        for x in range(0, image.shape[1], stepSize[0]):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


# 返回滑动窗结果集合，本示例暂时未用到
def get_slice(image, stepSize, windowSize):
    slice_sets = []
    for (x, y, window) in sliding_window(image, stepSize, windowSize):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != windowSize[1] or window.shape[1] != windowSize[0]:
            continue
        slice = image[y:y + windowSize[1], x:x + windowSize[0]]
        slice_sets.append(slice)
    return slice_sets

#滑动窗口计数
def slideCheck():
    with open(r"C:\Users\FYC\Desktop\allKinds.txt","r") as f:#读取对应txt文件
        lines = f.readlines()
    proList = []
    for model_line in range(len(lines)):
        print("此时检测的是：", lines[model_line].strip())
        Classname = lines[model_line].strip()
        list = os.listdir(r"C:\Users\FYC\Desktop\Answer2\Answer2/" + Classname)
        sum = len(list) - 1
        rightNum = 0
        for filePic in list:
            if (filePic != "Thumbs.db"):
                image = cv2.imread(r"C:\Users\FYC\Desktop\Answer2\Answer2/" + Classname + "/" + filePic)
                # 自定义滑动窗口的大小
                w = image.shape[1]
                h = image.shape[0]
                #图片分为3×3，共九个子区域
                (winW, winH) = (int(w / 3), int(h / 3))
                stepSize = (int(w / 3), int(h / 3))
                cnt = 0
                for (x, y, window) in sliding_window(image, stepSize=stepSize, windowSize=(winW, winH)):
                    # if the window does not meet our desired window size, ignore it
                    if window.shape[0] != winH or window.shape[1] != winW:
                        continue
                    # since we do not have a classifier, we'll just draw the window
                    clone = image.copy()
                    cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
                    cv2.imshow("Window", clone)
                    cv2.waitKey(1000)

                    slice = image[y:y + winH, x:x + winW]
                    count_pix = 0
                    for i in range(winH):
                        for j in range(winW):
                            if (slice[i, j][0] != 0 or slice[i, j][1] != 0 or slice[i, j][2] != 0):
                                # print("发现像素点")
                                count_pix += 1
                    if (count_pix > 30):
                        rightNum += 1
                        print("计数加1")

                    cv2.namedWindow('sliding_slice', 0)
                    cv2.imshow('sliding_slice', slice)
                    cv2.waitKey(1000)
                    cnt = cnt + 1
        if(rightNum!=0):
            proList.append(float(rightNum / sum))
        else:
            proList.append(0)
        print("完成该文件图片的遍历")  # 完成全文件图片的遍历
    print("proList:",proList)


def listTest():
    # CheckRight()#无滑动窗口计数
    # CountGO()#Person关系寻找
    #slideCheck()#滑动窗口计数

    model = mobilenet_unet(n_classes=NCLASSES, input_height=HEIGHT, input_width=WIDTH)
    model.load_weights("logs/turtle.h5")

    imgs = os.listdir(r"C:\Users\FYC\Desktop\Answer2\Answer2\turtle")#   ./img
    for jpg in imgs:
        # 从文件中读取图像
        if(jpg !="Thumbs.db"):
            img = Image.open(r"C:\Users\FYC\Desktop\Answer2\Answer2\turtle/" + jpg)  # "./img/"

            old_img = copy.deepcopy(img)
            orininal_h = np.array(img).shape[0]
            orininal_w = np.array(img).shape[1]

            # 进行边界填充，防止形变失真
            img, _, _ = letterbox_image(img, (WIDTH, HEIGHT), "jpg")

            img = img.resize((WIDTH, HEIGHT))
            img = np.array(img)
            img = img / 255
            img = img.reshape(-1, HEIGHT, WIDTH, 3)
            pr = model.predict(img)[0]
            # print(pr.size)
            # print(pr.shape[0])#图象的像素个数
            # print(pr.shape[1])
            count = 0
            temp_sum = 0.0
            for i in range(pr.shape[0]):
                if pr[i][1] > pr[i][0]:
                    temp_sum += pr[i][1]
                    count += 1
            # confidence = temp_sum/count#计算平均像素置信度
            print("总数：", count)
            # print("置信度：",confidence)
            print("占比：w", float(count / pr.shape[0]))
            pr = pr.reshape((int(HEIGHT / 2), int(WIDTH / 2), NCLASSES)).argmax(axis=-1)
            seg_img = np.zeros((int(HEIGHT / 2), int(WIDTH / 2), 3))
            colors = class_colors

            for c in range(NCLASSES):
                seg_img[:, :, 0] += ((pr[:, :] == c) * (colors[c][0])).astype('uint8')
                seg_img[:, :, 1] += ((pr[:, :] == c) * (colors[c][1])).astype('uint8')
                seg_img[:, :, 2] += ((pr[:, :] == c) * (colors[c][2])).astype('uint8')

            seg_img = Image.fromarray(np.uint8(seg_img)).resize((orininal_w, orininal_h))
            image = Image.blend(old_img, seg_img, 0.7)
            image.save("./7/" + jpg)



if __name__ == '__main__':

    model = mobilenet_unet(n_classes=NCLASSES, input_height=HEIGHT, input_width=WIDTH)
    model.load_weights("logs/CANCER.h5")
    img = Image.open(r"C:\Users\FYC\Desktop\TNSCUI2020_train\TNSCUI2020_train\24IMAGE\4604.PNG")  # "./img/"
    old_img = copy.deepcopy(img)
    orininal_h = np.array(img).shape[0]
    orininal_w = np.array(img).shape[1]

    # 进行边界填充，防止形变失真
    img, _, _ = letterbox_image(img, (WIDTH, HEIGHT), "png")

    img = img.resize((WIDTH, HEIGHT))
    img = np.array(img)
    img = img / 255
    img = img.reshape(-1, HEIGHT, WIDTH, 3)
    pr = model.predict(img)[0]
    count = 0
    temp_sum = 0.0
    print(pr)
    for i in range(pr.shape[0]):
        if pr[i][1] > pr[i][0]:
            temp_sum += pr[i][1]
            count += 1
    # confidence = temp_sum/count#计算平均像素置信度
    print("总数：", count)
    # print("置信度：",confidence)
    print("占比：w", float(count / pr.shape[0]))
    pr = pr.reshape((int(HEIGHT / 2), int(WIDTH / 2), NCLASSES)).argmax(axis=-1)
    seg_img = np.zeros((int(HEIGHT / 2), int(WIDTH / 2), 3))
    colors = class_colors

    for c in range(NCLASSES):
        seg_img[:, :, 0] += ((pr[:, :] == c) * (colors[c][0])).astype('uint8')
        seg_img[:, :, 1] += ((pr[:, :] == c) * (colors[c][1])).astype('uint8')
        seg_img[:, :, 2] += ((pr[:, :] == c) * (colors[c][2])).astype('uint8')

    seg_img = Image.fromarray(np.uint8(seg_img)).resize((orininal_w, orininal_h))
    image = Image.blend(old_img, seg_img, 0.3)
    image.save(r"C:\Users\FYC\Desktop\TNSCUI2020_train/4604.PNG")



