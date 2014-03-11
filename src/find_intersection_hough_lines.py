import numpy as np

def find_intersecting_point_hough_lines(theta_sideline, rho_sideline, theta_baseline, rho_baseline):
	a_sideline = np.cos(theta_sideline)
	b_sideline = np.sin(theta_sideline)
	x0_sideline = a_sideline*rho_sideline
	y0_sideline = b_sideline*rho_sideline
	slope_sideline = a_sideline / -b_sideline
	intercept_sideline = rho_sideline / np.sin(theta_sideline)#rho_sideline * (np.sin(theta_sideline) + (np.cos(theta_sideline) / np.sin(theta_sideline)))

	a_baseline = np.cos(theta_baseline)
	b_baseline = np.sin(theta_baseline)
	x0_baseline = a_baseline*rho_baseline
	y0_baseline = b_baseline*rho_baseline
	slope_baseline = a_baseline / -b_baseline
	intercept_baseline = rho_baseline / np.sin(theta_baseline) #rho_baseline * (np.sin(theta_baseline) + (np.cos(theta_baseline) / np.sin(theta_baseline)))
	
	x_intersection = (intercept_baseline - intercept_sideline) / (slope_sideline - slope_baseline)
	y_intersection = x_intersection * slope_sideline + intercept_sideline

	return (x_intersection, y_intersection)