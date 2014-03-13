import numpy as np

def find_best_lines(lines, target_num_lines):
	thetas = np.ones(target_num_lines) * float('inf')
	thetas[0] = lines[0][1]

	for line in lines[1:]:
