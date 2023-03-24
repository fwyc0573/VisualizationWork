import numpy as np
import cv2
import sys

# 读入图像并转化为浮点型
img1 = cv2.imread("hillary_clinton.jpg")

# 输出图像被设置为白色
img2 = 255 * np.ones(img1.shape, dtype=img1.dtype)

# 定义输入输出三角形
tri1 = np.float32([[[360, 200], [60, 250], [450, 400]]])
tri2 = np.float32([[[400, 200], [160, 270], [400, 400]]])

# 计算每个三角形的边框
r1 = cv2.boundingRect(tri1)
r2 = cv2.boundingRect(tri2)
print(r1)
print(r2)

# Offset points by left top corner of the 
# respective rectangles

# tri1Cropped = []
# tri2Cropped = []
#
# for i in range(0, 3):
#     tri1Cropped.append(((tri1[0][i][0] - r1[0]), (tri1[0][i][1] - r1[1])))
#     tri2Cropped.append(((tri2[0][i][0] - r2[0]), (tri2[0][i][1] - r2[1])))
#
# # Apply warpImage to small rectangular patches
# img1Cropped = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]