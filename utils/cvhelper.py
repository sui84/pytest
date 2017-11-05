#coding=utf-8
import cv2.cv as cv



image = cv.LoadImage(r'd:\temp\test2.jpg')

new = cv.CreateImage(cv.GetSize(image), image.depth, 1)
for i in range(image.height):
    for j in range(image.width):
        new[i,j] = max(image[i,j][0], image[i,j][1], image[i,j][2])

cv.Threshold(new, new, 10, 255, cv.CV_THRESH_BINARY_INV)
cv.ShowImage('a_window', new)
cv.WaitKey(0)
