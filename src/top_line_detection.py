import cv
import cv2
import numpy as np

import line_pixel_detection as lpd
import colors
import find_intersection_hough_lines as find_intersect

def find_top_boundary(court_mask):
	top_line_only = get_top_pixels(court_mask)
	best_top_line = hough_find_top_line(top_line_only)

def get_top_pixels(court_mask):
	top_pixels = np.copy(court_mask)
	# print 'Num columns is %s' %(court_mask.shape[1])
	# print 'Num rows is %s' %(court_mask.shape[0])
	for col in xrange(court_mask.shape[1]):
		top_found = False
		for row in xrange(court_mask.shape[0]):
			if top_found:
				top_pixels[row][col] = 0
			else:
				if top_pixels[row][col]:
					# print "Row is %s, column is %s, binary value is %s" %(row, col, top_line_only[row][col])
					top_found = True
	return top_pixels

def hough_find_top_line(top_line_only):
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

	# To print lines
	a = np.cos(theta_0)
	b = np.sin(theta_0)
	x0 = a*rho_0
	y0 = b*rho_0
	x1 = int(x0 + 1000*(-b))
	y1 = int(y0 + 1000*(a))
	x2 = int(x0 - 1000*(-b))
	y2 = int(y0 - 1000*(a))
	cv2.line(top_line_copy,(x1,y1),(x2,y2),(82,240,90),2)

	a = np.cos(theta_1)
	b = np.sin(theta_1)
	x0 = a*rho_1
	y0 = b*rho_1
	x1 = int(x0 + 1000*(-b))
	y1 = int(y0 + 1000*(a))
	x2 = int(x0 - 1000*(-b))
	y2 = int(y0 - 1000*(a))
	cv2.line(top_line_copy,(x1,y1),(x2,y2),(82,240,90),2)

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
		
	# Find intersection point
	if theta_baseline:
		intersection = find_intersect.intersect_point(theta_sideline, rho_sideline, theta_baseline, rho_baseline)
		# print intersection
		# cv2.circle(top_line_copy, intersection, 5, (255,255,255), -1)
		# cv2.imwrite('images/intersection.jpg', top_line_copy)
		return intersection
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
