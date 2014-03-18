import numpy as np


def get_intersection(line_1, line_2):
	rho_1, theta_1 = line_1
	print theta_1, rho_1
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


# Deprecated

# def intersect_point(theta_sideline, rho_sideline, theta_baseline, rho_baseline):
# 	a_sideline = np.cos(theta_sideline)
# 	b_sideline = np.sin(theta_sideline)
# 	slope_sideline = a_sideline / -b_sideline
# 	intercept_sideline = rho_sideline / b_sideline

# 	a_baseline = np.cos(theta_baseline)
# 	b_baseline = np.sin(theta_baseline)
# 	slope_baseline = a_baseline / -b_baseline
# 	intercept_baseline = rho_baseline / b_baseline

# 	x_intersection = (intercept_baseline - intercept_sideline) / (slope_sideline - slope_baseline)
# 	y_intersection = x_intersection * slope_sideline + intercept_sideline

# 	return (x_intersection, y_intersection)