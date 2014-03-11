import numpy as np

def find_intersecting_point_hough_lines(theta_sideline, rho_sideline, theta_baseline, rho_baseline):
	a_sideline = np.cos(theta_sideline)
	b_sideline = np.sin(theta_sideline)
	slope_sideline = a_sideline / -b_sideline
	intercept_sideline = rho_sideline / b_sideline

	a_baseline = np.cos(theta_baseline)
	b_baseline = np.sin(theta_baseline)
	slope_baseline = a_baseline / -b_baseline
	intercept_baseline = rho_baseline / b_baseline
	
	x_intersection = (intercept_baseline - intercept_sideline) / (slope_sideline - slope_baseline)
	y_intersection = x_intersection * slope_sideline + intercept_sideline

	return (x_intersection, y_intersection)