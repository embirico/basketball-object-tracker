# Imports ---------------------------------------

import cv
import cv2
import numpy as np
from matplotlib import pyplot as plt
from collections import deque


# Constants -------------------------------------

CROWD_TOP_HEIGHT_FRACTION = .375;
CROWD_BOTTOM_HEIGHT_FRACTION = .2;
BGR_BLACK = (0,0,0)
YCBCR_BLACK = (0,128,128)
YCBCR_WHITE = (255,128,128)



# Exported code ---------------------------------

def create_court_mask(_bgr_img, dominant_colorset, binary_gray=False):
	img = cv2.cvtColor(_bgr_img, cv2.COLOR_BGR2YCR_CB)
	for row in xrange(img.shape[0]):
		for col in xrange(img.shape[1]):
			idx = (row, col)
			_, cr, cb = img[idx]
			if (cr, cb) not in dominant_colorset:
				img[idx] = YCBCR_BLACK
			elif binary_gray:
				img[idx] = YCBCR_WHITE

	return ycbcr_to_gray(img) if binary_gray else img


def get_dominant_colorset(_bgr_img, thresh=0.02, ignore_crowd=True,
	peak_num=1):
	img = cv2.cvtColor(_bgr_img, cv2.COLOR_BGR2YCR_CB)

	if ignore_crowd:
		img = img[CROWD_TOP_HEIGHT_FRACTION*img.shape[0] : -CROWD_BOTTOM_HEIGHT_FRACTION*img.shape[0]]

	hist = cv2.calcHist([img], [1,2], None, [256,256], [0,256, 0,256])

	peak1_flat_idx = np.argmax(hist)
	peak1_idx = np.unravel_index(peak1_flat_idx, hist.shape)
	peak1_val = hist[peak1_idx]
	connected_hist1, sum1, subtracted_hist = get_connected_hist(hist, peak1_idx, thresh)

	if peak_num == 1:
		return connected_hist1

	peak2_flat_idx = np.argmax(subtracted_hist)
	peak2_idx = np.unravel_index(peak2_flat_idx, subtracted_hist.shape)
	peak2_val = hist[peak2_idx]
	connected_hist2, sum2, subtracted_hist = get_connected_hist(subtracted_hist, peak2_idx, thresh)

	return connected_hist2



def get_paint_mask(image_name):
	court_colorset = get_dominant_colorset(image_name)
	court_mask = create_court_mask(image_name, court_colorset, binary_gray=True)
	court_mask = fill_holes_with_contour_filling(court_mask)

	court_masked = cv2.imread(image_name)
	for row in xrange(court_masked.shape[0]):
		for col in xrange(court_masked.shape[1]):
			if court_mask[row][col]:
				court_masked[row][col] = BGR_BLACK

	return court_masked


def fill_holes_with_contour_filling(gray, inverse=False):
  filled = gray.copy()
  if inverse:
  	filled = cv2.bitwise_not(filled)
  contour, _ = cv2.findContours(filled,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  for cnt in contour:
    cv2.drawContours(filled, [cnt], 0, 255, -1)
  if inverse:
  	filled = cv2.bitwise_not(filled)
  return filled


# Non-exported code -----------------------------

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


# Helpers ---------------------------------------

def show_image(img):
	cv2.imshow('Showing image',img)
	if cv2.waitKey(0) & 0xff == 27:
		cv2.destroyAllWindows()


def show_hist(hist_list):
	for i, hist in enumerate(hist_list):
		plt.subplot(1, len(hist_list), i+1)
		plt.imshow(hist, interpolation = 'nearest')
	plt.show()


def ycbcr_to_bgr(ycbcr_img):
	img = ycbcr_img.copy()
	return cv2.cvtColor(img, cv2.COLOR_YCR_CB2BGR)


def ycbcr_to_gray(ycbcr_img):
	img = ycbcr_img.copy()
	img = ycbcr_to_bgr(img)
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def ycbcr_to_binary(ycbcr_img):
	img = ycbcr_img.copy()
	return ycbcr_to_gray(img) > 128


def binary_to_gray(binary_img):
	img = binary_img.copy()
	return img * 255;


def gray_to_bgr(gray_img):
	img = gray_img.copy()
	return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

def show_binary(binary):
	plt.imshow(binary)
	plt.show()

if __name__ == '__main__':
	# image_root = 'images/6175'
	image_root = 'images/5993'
	image_ext = '.jpg'
	image_name = image_root + image_ext

	img = get_paint_mask(image_name)