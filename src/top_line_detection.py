import cv
import cv2
import numpy as np

import line_pixel_detection as lpd
import colors

def hough_find_top_line(top_line_only):
	# Finding the best threshold for Hough
	for i in range(80,86):
		top_line_copy = np.copy(top_line_only)
		# gray = cv2.cvtColor(top_line_copy,cv2.COLOR_BGR2GRAY)
		lines = cv2.HoughLines(top_line_copy,5,np.pi/180 * 3,i)

		count = 0
		for rho,theta in lines[0]:
			count += 1
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			cv2.line(top_line_copy,(x1,y1),(x2,y2),(82,240,90),2)

		print 'The number of lines with threshold at %d is %d' %(i, count)
		cv2.imwrite('images/test_binary_5993_' + str(i) + '.jpg', top_line_copy)


def test(top_line_only):
	lines_at_60 = cv2.HoughLines(top_line,5,np.pi/180 * 3,60)[0]

	thresh = 80
	prevLines = None
	while True:
		lines = cv2.HoughLines(top_line,5,np.pi/180 * 3,thresh)
		if lines is None:
			break
		prevLines = lines[0]
		thresh += 1

	for i in xrange(len(prevLines)):
		print 'Lines are the same', lines_at_60[i] == prevLines[i]


if __name__ == '__main__':
	image_root = 'images/5993'
	image_ext = '.jpg'
	image_name = image_root + image_ext

	court_mask = colors.create_court_mask(image_name, binary_gray=True)
	top_line = lpd.get_top_pixels(court_mask)
	test(top_line)
