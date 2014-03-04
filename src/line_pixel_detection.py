# First, use Liu "Playfield detection" to get a GMM of court color
# Then, mask non-court
# Then, detect line pixels
# Then, get lines
# Then, find features from line interections
# Then compute optimal H

import cv2
import numpy as np




def convertToYCrCb(imageName):
	img = cv2.imread(imageName)
	newImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# newImg = cv2.cvtColor(img,cv2.COLOR_RGB2YCR_CB)
	# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	cv2.imshow('bitch',newImg)
	if cv2.waitKey(0) & 0xff == 27:
		cv2.destroyAllWindows()


if __name__ == '__main__':
	imageName = 'images/5993.jpg'
	convertToYCrCb(imageName)