import cv
import cv2
import numpy as np

def find_top_boundary(court_mask):
	top_line_only = get_top_pixels(court_mask)
	return hough_find_top_line(top_line_only)

# Returns court mask with only top pixels of mask shown
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

# Finds top lines based on top pixels of court mask
def hough_find_top_line(top_line_only):
	top_line_copy = np.copy(top_line_only)
	lines = cv2.HoughLines(top_line_copy,5,np.pi/180 * 3,75)[0]
	# print 'The number of lines with threshold at %d is %d' %(75, len(lines))

	theta_0 = lines[0][1]
	rho_0 = lines[0][0]
	theta_1 = None
	rho_1 = 0

	for rho,theta in lines[1:]:
		if abs(theta_0 - theta) > 0.4:
			theta_1 = theta
			rho_1 = rho
			break

	# Assign baseline/sideline
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

	if theta_baseline:
		return ((rho_sideline, theta_sideline), (rho_baseline, theta_baseline))
	else:
		return ((rho_sideline, theta_sideline))