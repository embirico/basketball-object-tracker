import numpy as np

def intersect_point(line_1, line_2):
	rho_1, theta_1 = line_1
	rho_2, theta_2 = line_2
	a_1 = np.cos(theta_1)
	b_1 = np.sin(theta_1)
	slope_1 = a_1 / -b_1
	intercept_1 = rho_1 / b_1

	a_2 = np.cos(theta_2)
	b_2 = np.sin(theta_2)
	slope_2 = a_2 / -b_2
	intercept_2 = rho_2 / b_2
	
	x_intersection = (intercept_2 - intercept_1) / (slope_1 - slope_2)
	y_intersection = x_intersection * slope_1 + intercept_1

	return (x_intersection, y_intersection)