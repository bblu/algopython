import cv2 as cv
img =cv.imread('/home/bblu/repo/opencv/samples/data/butterfly.jpg')
cv.namedWindow("fly")
cv.imshow("fly",img)
cv.waitKey(0)
cv.destroyAllWindows()
