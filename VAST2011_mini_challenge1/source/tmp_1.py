import numpy as np
import cv2
# record_index = np.zeros(5)
# record_index[0] = 1
# print(record_index)
# str = "2020/4/30  0:00:00"
# print(str.split("  ")[0].split("/")[1])
# print(str.split("  ")[0].split("/")[-1])
# print(str.split("  ")[1].split(":")[0])
# a = [1,2,3,4]
# print(sum(a[0:4]))

image_1 = r"H:\re\5.18_12to24.jpg"
image_2 = r"H:\re\5.18_0to12.jpg"
image_3 = r"H:\Vastopolis_Map_2.jpg"#原图
src1 = cv2.imread(image_1)
src2 = cv2.imread(image_2)
src3 = cv2.imread(image_3)
image = cv2.subtract(src3, src2)
cv2.namedWindow('input_image_1', cv2.WINDOW_AUTOSIZE)
cv2.imshow("input_image_1",image)
cv2.imwrite(r"H:\jian.jpg", image)
cv2.waitKey(0)


# cv2.imshow("input_image_2",image_2)
# image_2 = cv2.subtract(src2, src3)
# cv2.namedWindow('input_image_2', cv2.WINDOW_AUTOSIZE)
# cv2.imwrite(r"H:\5.2012to24_SUB.jpg", image_2)
