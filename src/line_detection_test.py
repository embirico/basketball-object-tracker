import cv2
from cv2.cv import *
import numpy as np

show = False

imgName = '5993'

for i in range(0,10):
	img = cv2.imread(imgName + '.jpg')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,20 * i,255,apertureSize = 3)

	lines = cv2.HoughLines(edges,1,np.pi/180,380)
	for rho,theta in lines[0]:
	    a = np.cos(theta)
	    b = np.sin(theta)
	    x0 = a*rho
	    y0 = b*rho
	    x1 = int(x0 + 1000*(-b))
	    y1 = int(y0 + 1000*(a))
	    x2 = int(x0 - 1000*(-b))
	    y2 = int(y0 - 1000*(a))

	    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

	cv2.imwrite(imgName + '_low_' + str(i*20) + '.jpg',img)

if show:
	imgNew = LoadImage(imgName + '_Processed.jpg')
	NamedWindow('window')
	ShowImage('window',imgNew)
	WaitKey(0)

