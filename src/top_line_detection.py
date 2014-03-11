import cv
import cv2
import numpy as np

import line_pixel_detection as lpd
import colors

def hough_find_top_line(top_line_only):
	# Finding the best threshold for Hough

	top_line_copy = np.copy(top_line_only)
	lines = cv2.HoughLines(top_line_copy,5,np.pi/180 * 3,75)[0]
	print 'The number of lines with threshold at %d is %d' %(75, len(lines))

	theta_0 = lines[0][1]
	rho_0 = lines[0][0]
	theta_1 = None
	rho_1 = 0

	for rho,theta in lines[1:]:
		if abs(theta_0 - theta) > 0.4:
			theta_1 = theta
			rho_1 = rho
			break

	# # To print lines
	# a = np.cos(theta_0)
	# b = np.sin(theta_0)
	# x0 = a*rho_0
	# y0 = b*rho_0
	# x1 = int(x0 + 1000*(-b))
	# y1 = int(y0 + 1000*(a))
	# x2 = int(x0 - 1000*(-b))
	# y2 = int(y0 - 1000*(a))
	# cv2.line(top_line_copy,(x1,y1),(x2,y2),(82,240,90),2)
	# cv2.imwrite('images/test_binary_5993_75' + '.houghline opencvjpg', top_line_copy)
	# a = np.cos(theta_1)
	# b = np.sin(theta_1)
	# x0 = a*rho_1
	# y0 = b*rho_1
	# x1 = int(x0 + 1000*(-b))
	# y1 = int(y0 + 1000*(a))
	# x2 = int(x0 - 1000*(-b))
	# y2 = int(y0 - 1000*(a))
	# cv2.line(top_line_copy,(x1,y1),(x2,y2),(82,240,90),2)
	# cv2.imwrite('images/test_binary_5993_75' + '.jpg', top_line_copy)

	print 'The first theta is %s, the second theta is %s' %(theta_0, theta_1)

	if theta_0 < 1.6:
		theta_sideline = theta_0
		theta_baseline = theta_1
		rho_sideline = rho_0
		rho_baseline = rho_1
	else:
		theta_sideline = theta_1
		theta_baseline = theta_0
		rho_sideline = rho_1
		rho_baseline = rho_0

	a = [[rho_sideline,theta_sideline], [rho_baseline, theta_baseline]] if theta_baseline else [rho_sideline,theta_sideline]

	# Find intersection point
	if len(a) > 1:
		a_sideline = np.cos(theta_sideline)
		b_sideline = np.sin(theta_sideline)
		x0_sideline = a*rho_sideline
		y0_sideline = b*rho_sideline

		a_baseline = np.cos(theta_baseline)
		b_baseline = np.sin(theta_baseline)
		x0_baseline = a*rho_baseline
		y0_baseline = b*rho_baseline



	else:
		print 'no intersection'


def confirm_hough_lines_sorted(top_line_only):
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
