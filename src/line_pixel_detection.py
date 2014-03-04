# First, use Liu "Playfield detection" to get a GMM of court color
# Then, mask non-court
# Then, detect line pixels
# Then, get lines
# Then, find features from line interections
# Then compute optimal H

import cv
import cv2
import numpy as np
from matplotlib import pyplot as plt

from collections import deque

def getColorPeaks(imageName):
	img = cv2.imread(imageName)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)

	hist = cv2.calcHist([img], [1,2], None, [256,256], [0,256, 0,256])

	peak1_flat_idx = np.argmax(hist)
	peak1_idx = np.unravel_index(peak1_flat_idx, hist.shape)
	peak1_val = hist[peak1_idx]
	connected_hist1, sum1, subtracted_hist = get_connected_hist(hist, peak1_idx)

	peak2_flat_idx = np.argmax(subtracted_hist)
	peak2_idx = np.unravel_index(peak2_flat_idx, subtracted_hist.shape)
	peak2_val = subtracted_hist[peak2_idx]
	connected_hist2, sum2, _ = get_connected_hist(subtracted_hist, peak2_idx)

	print "{} counts similar to {}".format(sum1, peak1_idx)
	print "{} counts similar to {}".format(sum2, peak2_idx)

	show_hist([hist, subtracted_hist, _])


# BTW etc is the total count and the 'subtracted new histogram'
def get_connected_hist(hist, peak_idx, thresh=.05):
	connected_hist = np.zeros(hist.shape)
	sum_val = 0
	subtracted_hist = np.copy(hist)

	min_passing_val = thresh * hist[peak_idx]

	connected_hist[peak_idx] = 1
	sum_val	+= hist[peak_idx]
	subtracted_hist[peak_idx] = 0
	queue = deque([peak_idx])
	while queue:
		x, y = queue.popleft()
		toAdd = []
		if x > 1:
			toAdd.append((x-1, y))
		if x < hist.shape[0] - 1:
			toAdd.append((x+1, y))
		if y > 1:
			toAdd.append((x, y-1))
		if y < hist.shape[1] - 1:
			toAdd.append((x, y+1))

		for idx in toAdd:
			if not connected_hist[idx] and hist[idx] >= min_passing_val:
				connected_hist[idx] = 1
				sum_val += hist[idx]
				subtracted_hist[idx] = 0
				queue.append(idx)

	return connected_hist, sum_val, subtracted_hist



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


def show_image(img):
	cv2.imshow('Showing image',img)
	if cv2.waitKey(0) & 0xff == 27:
		cv2.destroyAllWindows()


def show_hist(hist_list):
	for i, hist in enumerate(hist_list):
		plt.subplot(1, len(hist_list), i+1)
		plt.imshow(hist, interpolation = 'nearest')
	plt.show()


if __name__ == '__main__':
	imageName = 'images/5993.jpg'
	getColorPeaks(imageName)