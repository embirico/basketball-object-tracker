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

	cv2.imshow('bitch',newImg)
	if cv2.waitKey(0) & 0xff == 27:
		cv2.destroyAllWindows()


if __name__ == '__main__':
	imageName = 'images/5993.jpg'
	convertToYCrCb(imageName)