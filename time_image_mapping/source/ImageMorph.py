import numpy as np
import cv2
import sys
import Delaunay

#从pts读取特征点
def readPoints(path,img):
    points = []
    width = img.shape[1]-1
    height = img.shape[0]-1
    add_ParmPoints = [(0,0),(0,height),(int(width/2),0),(int(width/4),0),(int(width*3/4),0),
                      (0,int(height/2)),(0,int(height/4)),(0,int(height*3/4)),(width,int(height/2)),(width,int(height/4)),(width,int(height*3/4)),
                      (int(width/2), height),(int(width/4),height),(int(width*3/4),height)
                      ,(width,0),(width,height)]
    lineNum = 1
    with open(path) as file:
        for line in file:
            if(lineNum >3 and lineNum<72):
                x, y = line.split(" ")
                x, y = float(x), float(y)
                points.append((int(x), int(y)))
            lineNum+=1
    points.extend(add_ParmPoints)
    return points

#从pts读取特征点
def readPoints_txt(path,img):
    points = []
    width = img.shape[1]-1
    height = img.shape[0]-1
    add_ParmPoints = [(0,0),(0,height),(int(width/2),0),(int(width/4),0),(int(width*3/4),0),
                      (0,int(height/2)),(0,int(height/4)),(0,int(height*3/4)),(width,int(height/2)),(width,int(height/4)),(width,int(height*3/4)),
                      (int(width/2), height),(int(width/4),height),(int(width*3/4),height)
                      ,(width,0),(width,height)]
    with open(path) as file:
        for line in file:
            x, y = line.split(" ")
            points.append((int(x), int(y)))
    points.extend(add_ParmPoints)
    return points


# 仿射变换
def applyAffineTransform(src, srcTri, dstTri, size):
    # 计算仿射变换的矩阵
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))
    #进行仿射变换
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    return dst

def morphTriangle(img1, img2, img, t1, t2, t, alpha):
    #得到包裹三角形的矩形
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))
    # 得到各矩形的左上角偏移量
    t1Rect = []
    t2Rect = []
    tRect = []
    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]), (t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
    #建立蒙版，对三角形进行填充
    mask = np.zeros((r[3], r[2], 3), dtype=np.float32)  # 先行再列
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0));
    # 找到而对应区域
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]  # img1中对应矩形区域
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]  # img2中对应矩形区域
    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)
    # 像素填充
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2
    #只保留三角区域的变换
    img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] * (1 - mask) + imgRect * mask

if __name__ == '__main__':
    for i in range(13):
        alpha = 0
        j = i+1
        if(i<10):
            i = "0"+str(i)
        if(j<10):
            j = "0"+str(j)
        print("i,j->",i,j)
        filename1 = "boys/" + "080A" + str(i) +".JPG"
        filename2 = "boys/" + "080A" + str(j) +".JPG"

        # ptsname1 = "boys_pts/" + "080a" + str(i) +".pts"
        # ptsname2 = "boys_pts/" + "080a" + str(j) + ".pts"
        ptsname1 = "boys_txt/" + "080a" + str(i) +".txt"
        ptsname2 = "boys_txt/" + "080a" + str(j) + ".txt"

        img1 = np.float32(cv2.imread(filename1))
        img2 = np.float32(cv2.imread(filename2))
        # w = img1.shape[0]
        h = max(img1.shape[0],img2.shape[0])
        w = max(img1.shape[1],img2.shape[1])

        points1 = readPoints_txt(ptsname1, img1)
        points2 = readPoints_txt(ptsname2, img2)
        points = []
        for i in range(21):
            if alpha<1.0:
                alpha += 0.05
            # Compute weighted average point coordinates
            for i in range(0, len(points1)):
                x = (1 - alpha) * points1[i][0] + alpha * points2[i][0]
                y = (1 - alpha) * points1[i][1] + alpha * points2[i][1]
                points.append((x, y))

            imgMorph = np.zeros((h,w,3), dtype=img1.dtype)
            # 读取三角形
            TriangleList_t1 = np.array(Delaunay.getTriList(img1, points1), dtype=np.int32)
            tri_Matrix = []
            for i in range(len(TriangleList_t1)):
                temp = []
                t1 = [tuple(TriangleList_t1[i][0:2]), tuple(TriangleList_t1[i][2:4]), tuple(TriangleList_t1[i][4:6])]
                for i in range(3):
                    if (t1[i] in points1):
                        temp.append(points1.index(t1[i]))
                tri_Matrix.append(temp)

            for each in tri_Matrix:
                x = each[0]
                y = each[1]
                z = each[2]
                t1 = [points1[x], points1[y], points1[z]]
                t2 = [points2[x], points2[y], points2[z]]
                t = [points[x], points[y], points[z]]
                morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha)

            cv2.imshow("Boy Morphed Face", np.uint8(imgMorph))
            cv2.waitKey(40)

