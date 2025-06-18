import cv2
import numpy as np


#Convert image to edge bitmap
img = cv2.imread('assets/koala.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
inverted = cv2.bitwise_not(edges)

cv2.imwrite('assets/hinata_edges.bmp', inverted)
cv2.imshow('Image',inverted)
cv2.waitKey(0)
cv2.destroyAllWindows()
