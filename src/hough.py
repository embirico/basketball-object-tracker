# Imports ---------------------------------------

import cv
import cv2
import numpy as np
from matplotlib import pyplot as plt

import colors # local reference


def find_top_boundary(court_mask):
	# top_line_set = set()
	# for col in xrange(img.shape[1]):
	# 	for row in xrange(img.shape[0]):
	# 		if court_mask[row][col] != (0,128,128):
	# 			top_line_set.append((row,col))
	# 			break

	# # RANSAC (projection threshold ~0.5 of horizontal baseline)
	# best_top_line = find_top_line(top_line_set)
	top_line_only = np.copy(court_mask)
	for col in xrange(court_mask.shape[1]):
		top_found = False
		for row in xrange(court_mask.shape[0]):
			if top_found:
				top_line_only[row][col] = (0,128,128)
			else:
				if not np.array_equal(top_line_only[row][col], np.array([0,128,128])):
					top_found = True

	# Hough transform to find top boundary (doesn't work that well)
	best_top_line = hough_find_top_line(top_line_only)
	# RANSAC (projection threshold ~0.5 of horizontal baseline)
	# best_top_line = ransac_find_top_line(top_line_only)


if __name__ == '__main__':
	# image_root = 'images/6175'
	image_root = 'images/5993'
	image_ext = '.jpg'
	image_name = image_root + image_ext
	court_mask = colors.create_court_mask(image_name, binary=True)
	court_mask = colors.ycbcr_to_binary(court_mask)
	plt.imshow(court_mask)
	plt.show()
	# edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)