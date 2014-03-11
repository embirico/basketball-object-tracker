import cv
import cv2
import numpy as np

def hough_find_top_line(top_line_only):
	# Finding the best threshold for Hough
	for i in range(65,75):
		top_line_copy = np.copy(top_line_only)
		# gray = cv2.cvtColor(top_line_copy,cv2.COLOR_BGR2GRAY)	
		lines = cv2.HoughLines(top_line_copy,1,np.pi/180,i)

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
		cv2.imwrite('images/test_binary_6175_' + str(i) + '.jpg', top_line_copy)
