
import numpy as np
import cv2
import sys
import Delaunay

# Read points from text file
def readPoints(path) :
    points = []
    with open(path) as file :
        for line in file :
            x, y = line.split(" ")
            x,y = float(x), float(y)
            points.append((int(x), int(y)))
    return points

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )
    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha) :
    # Find bounding rectangle for each triangle
    # r1 = cv2.boundingRect(np.float32([t1]))
    # r2 = cv2.boundingRect(np.float32([t2]))
    # r = cv2.boundingRect(np.float32([t]))
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))


    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []

    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))
    # print(tRect)
    # print(t1Rect)
    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)#先行再列
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0));
    # cv2.imshow("Morphed Face", np.uint8(mask))
    # cv2.waitKey(0)
    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]#img1中对应矩形区域
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]#img2中对应矩形区域
    # print(img1Rect)
    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2
    # cv2.imshow("Morphed Face", np.uint8(imgRect))
    # cv2.waitKey(0)
    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask
    # cv2.imshow("Morphed Face", np.uint8(img))
    # cv2.waitKey(0)


if __name__ == '__main__' :
    # filename1 = '080A06.JPG'
    # filename2 = '080A13.JPG'
    filename2 = '080A13.JPG'
    filename1 = '080A06.JPG'
    alpha = 0.5

    # Read images
    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)
    # Convert Mat to float data type
    img1 = np.float32(img1)
    img2 = np.float32(img2)

    # Read array of corresponding points
    points2 = readPoints('2.txt')
    points1 = readPoints('1.txt')
    points = []

    # Compute weighted average point coordinates
    for i in range(0, len(points1)):
        x = (1 - alpha ) * points1[i][0] + alpha * points2[i][0]
        y = (1 - alpha ) * points1[i][1] + alpha * points2[i][1]
        points.append((x,y))

    # Allocate space for final output
    imgMorph = np.zeros(img1.shape, dtype = img1.dtype)

    # Read triangles
    TriangleList_t1 = np.array(Delaunay.getTriList(img1, points1), dtype=np.int32)


    # print(TriangleList_t1)
    # TriangleList_t2 = Delaunay.getTriList(img1, points2)
    # TriangleList_t = Delaunay.getTriList(img1,points)
    tri_Matrix = []
    for i in range(len(TriangleList_t1)):
        # t1 =[tuple(np.array(TriangleList_t1[i][0:2], dtype=np.int32)),
        #      tuple(np.array(TriangleList_t1[i][2:4], dtype=np.int32)),
        #      tuple(np.array(TriangleList_t1[i][4:6], dtype=np.int32))]
        # t2 = [tuple(np.array(TriangleList_t2[i][0:2], dtype=np.int32)),
        #       tuple(np.array(TriangleList_t2[i][2:4], dtype=np.int32)),
        #       tuple(np.array(TriangleList_t2[i][4:6], dtype=np.int32))]
        # t = [tuple(np.array(TriangleList_t[i][0:2], dtype=np.int32)),
        #       tuple(np.array(TriangleList_t[i][2:4], dtype=np.int32)),
        #       tuple(np.array(TriangleList_t[i][4:6], dtype=np.int32))]
        temp = []
        t1 = [tuple(TriangleList_t1[i][0:2]), tuple(TriangleList_t1[i][2:4]), tuple(TriangleList_t1[i][4:6])]
        for i in range(3):
            if(t1[i] in points1):
                temp.append(points1.index(t1[i]))
                print(points1.index(t1[i]))
        tri_Matrix.append(temp)
    print(tri_Matrix)

    for each in tri_Matrix:
        x = each[0]
        y = each[1]
        z = each[2]
        t1 = [points1[x], points1[y], points1[z]]
        t2 = [points2[x], points2[y], points2[z]]
        t = [points[x], points[y], points[z]]
        morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha)


    # with open("tri.txt") as file :
    #     for line in file :
    #         x,y,z = line.split()
    #         x = int(x)
    #         y = int(y)
    #         z = int(z)
    #
    #         t1 = [points1[x], points1[y], points1[z]]
    #         t2 = [points2[x], points2[y], points2[z]]
    #         t = [ points[x], points[y], points[z] ]
    #         print(t1)
    #
    #         # Morph one triangle at a time.
    #         morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha)
    #
    # # Display Result
    cv2.imshow("Morphed Face", np.uint8(imgMorph))
    cv2.waitKey(0)
