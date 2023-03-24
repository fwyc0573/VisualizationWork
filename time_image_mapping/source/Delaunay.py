import cv2
import numpy as np
import random

def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True

def draw_point(img, p, color):
    cv2.circle(img, p, 2, color, 1, cv2.LINE_AA, 0)

def draw_delaunay(img, triangleList, delaunay_color):
    size = img.shape
    r = (0, 0, size[1], size[0])
    for t in triangleList:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])
        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)

# Draw voronoi diagram
def draw_voronoi(img, subdiv):
    (facets, centers) = subdiv.getVoronoiFacetList([])
    for i in range(0, len(facets)):
        ifacet_arr = []
        for f in facets[i]:
            ifacet_arr.append(f)
        ifacet = np.array(ifacet_arr, np.int)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        cv2.fillConvexPoly(img, ifacet, color, cv2.LINE_AA, 0);
        ifacets = np.array([ifacet])
        cv2.polylines(img, ifacets, True, (0, 0, 0), 1, cv2.LINE_AA, 0)
        cv2.circle(img, (centers[i][0], centers[i][1]), 3, (0, 0, 0), 2, cv2.LINE_AA, 0)

def getTriList(img1,points3):
    size = img1.shape
    rect = (0, 0, size[1], size[0])
    subdiv = cv2.Subdiv2D(rect)
    for p in points3:
        subdiv.insert(p)
    delaunay_color = (0.5, 0.5, 0.5)
    triangleList = subdiv.getTriangleList()
    # r = (0, 0, size[1], size[0])
    # for t in triangleList:
    #     pt1 = (t[0], t[1])
    #     pt2 = (t[2], t[3])
    #     pt3 = (t[4], t[5])
    #     if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
    #         cv2.line(img1, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
    #         cv2.line(img1, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
    #         cv2.line(img1, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
    # cv2.imshow("1", img1)
    # cv2.waitKey(0)
    return subdiv.getTriangleList()


if __name__ == '__main__':
    win_delaunay = "Boy Morphed Face"
    animate = True
    delaunay_color = (0.5, 0.5, 0.5)
    points_color = (0, 0, 255)
    img = cv2.imread("080A06.JPG")
    img_orig = img.copy();

    size = img.shape
    rect = (0, 0, size[1], size[0])
    subdiv = cv2.Subdiv2D(rect)
    points = []
    points2 = []
    points3 = []
    #图1特征点
    with open("1.txt") as file:
        for line in file:
            x, y = line.split(" ")
            x,y = float(x), float(y)
            points.append((int(x), int(y)))
    # 将特征点加入subdiv进行Delaunay三角剖分
    for p in points:
        subdiv.insert(p)
        triangleList = subdiv.getTriangleList();
        if animate:#动态显示
            img_copy = img_orig.copy()
            # Draw delaunay triangles
            draw_delaunay(img_copy, triangleList, (255.0, 255.0, 255.0));
            cv2.imshow(win_delaunay, img_copy)
            cv2.waitKey(100)

    print(triangleList)
    draw_delaunay(img, triangleList, (255, 255, 255));
    #绘出原来特征点的位置
    for p in points:
        draw_point(img, p, (0, 0, 255))

    cv2.imshow(win_delaunay, img)
    cv2.waitKey(0)