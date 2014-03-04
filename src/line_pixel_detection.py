# First, use Liu "Playfield detection" to get a GMM of court color
# Then, mask non-court
# Then, detect line pixels
# Then, get lines
# Then, find features from line interections
# Then compute optimal H

import cv2
import numpy as np
from matplotlib import pyplot as plt

def convertToYCrCb(imageName):
	img = cv2.imread(imageName)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)

	hist = cv2.calcHist([img], [1,2], None, [256,256], [0,256, 0,256]);
	plt.imshow(hist, interpolation = 'nearest')
	plt.show()

	# cv2.imshow('bitch',img)
	# if cv2.waitKey(0) & 0xff == 27:
	# 	cv2.destroyAllWindows()

def oneDimHists(imageName):
	img = cv2.imread(imageName)
	newImg = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
	# newImg = cv2.cvtColor(img,cv2.COLOR_RGB2YCR_CB)
	# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	h = np.zeros((300,256,3))
	bins = np.arange(256).reshape(256,1)
	color = [ (255,0,0),(0,255,0),(0,0,255) ]

	y, cr, cb = newImg[:,:,0].copy(), newImg[:,:,1].copy(), newImg[:,:,2].copy()
	for item,col in enumerate(color):
	    hist_item = cv2.calcHist([newImg],[item],None,[256],[0,255])
	    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
	    hist=np.int32(np.around(hist_item))
	    pts = np.column_stack((bins,hist))
	    cv2.polylines(h,[pts],False,col)

	h=np.flipud(h)

	cv2.imshow('colorhist',h)
	cv2.waitKey(0)
	# cv2.imshow('bitch',newImg)
	# if cv2.waitKey(0) & 0xff == 27:
	# 	cv2.destroyAllWindows()



if __name__ == '__main__':
	imageName = 'images/5993.jpg'
	convertToYCrCb(imageName)