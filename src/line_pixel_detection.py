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

def get_dominant_colorset(image_name, thresh=0.4, peak_num=0):
	img = cv2.cvtColor(cv2.imread(image_name), cv2.COLOR_BGR2YCR_CB)

	hist = cv2.calcHist([img], [1,2], None, [256,256], [0,256, 0,256])

	peak1_flat_idx = np.argmax(hist)
	peak1_idx = np.unravel_index(peak1_flat_idx, hist.shape)
	peak1_val = hist[peak1_idx]
	connected_hist1, sum1, subtracted_hist = get_connected_hist(hist, peak1_idx, thresh)

	peak2_flat_idx = np.argmax(subtracted_hist)
	peak2_idx = np.unravel_index(peak2_flat_idx, subtracted_hist.shape)
	peak2_val = hist[peak2_idx]
	connected_hist2, sum2, subtracted_hist = get_connected_hist(subtracted_hist, peak2_idx, thresh)

	return [connected_hist1, connected_hist2][peak_num]


def get_connected_hist(hist, peak_idx, thresh):
	connected_hist = set()
	sum_val = 0
	subtracted_hist = np.copy(hist)

	min_passing_val = thresh * hist[peak_idx]

	connected_hist.add(peak_idx)
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
			if idx not in connected_hist and hist[idx] >= min_passing_val:
				connected_hist.add(idx)
				sum_val += hist[idx]
				subtracted_hist[idx] = 0
				queue.append(idx)

	return connected_hist, sum_val, subtracted_hist


def show_image(img):
	cv2.imshow('Showing image',img)
	if cv2.waitKey(0) & 0xff == 27:
		cv2.destroyAllWindows()


def show_hist(hist_list):
	for i, hist in enumerate(hist_list):
		plt.subplot(1, len(hist_list), i+1)
		plt.imshow(hist, interpolation = 'nearest')
	plt.show()


def create_court_mask(image_name, dominant_colorset):
	img = cv2.cvtColor(cv2.imread(image_name), cv2.COLOR_BGR2YCR_CB)
	for row in xrange(img.shape[0]):
		for col in xrange(img.shape[1]):
			idx = (row, col)
			_, cr, cb = img[idx]
			if (cr, cb) not in dominant_colorset:
				img[idx] = (0,128,128)

	return img


if __name__ == '__main__':
	image_root = 'images/6175'
	image_ext = '.jpg'
	image_name = image_root + image_ext
	for thresh in np.linspace(0.01, 0.05, 5):
		dominant_colorset = get_dominant_colorset(image_name, thresh, 1)
		img = create_court_mask(image_name, dominant_colorset)
		cv2.imwrite(image_root + '_masked_' + str(thresh) + image_ext,
			cv2.cvtColor(img, cv2.COLOR_YCR_CB2BGR))