# Library imports

import image_object as IO
import json
import numpy as np


# Local imports
import hough


# Constants
class NbaCourt:
	SIDELINE_FREETHROW = 'sideline, freethrow'
	SIDELINE_BASELINE = 'sideline, baseline'
	CLOSEPAINT_BASELINE = 'closepaint, baseline'
	CLOSEPAINT_FREETHROW = 'closepaint, freethrow'

	LEFT = 'left'
	RIGHT = 'right'

	LOCATIONS = ['sideline, freethrow', 'sideline, baseline',
		'closepaint, baseline', 'closepaint, freethrow']

	@classmethod
	def get_loc_coords(this, loc, side):
		if side == 'left':
			if loc == this.SIDELINE_FREETHROW:
				return (18*12 + 10, 0)
			elif loc == this.SIDELINE_BASELINE:
				return (0, 0)
			elif loc == this.CLOSEPAINT_BASELINE:
				return (0, 33*12)
			elif loc == this.CLOSEPAINT_FREETHROW:
				return (18*12 + 10, 33*12)
			else:
				raise Exception('loc not recognized')
		elif side == 'right':
			if loc == this.SIDELINE_FREETHROW:
				return (94*12 - (18*12 + 10), 0)
			elif loc == this.SIDELINE_BASELINE:
				return (94*12 - (0), 0)
			elif loc == this.CLOSEPAINT_BASELINE:
				return (94*12 - (0), 33*12)
			elif loc == this.CLOSEPAINT_FREETHROW:
				return (94*12 - (18*12 + 10), 33*12)
			else:
				raise Exception('loc not recognized')
		else:
			raise Exception('Side must be "left" or "right".')


def compute_homography(image_pts):
	a = np.zeros((8,8))
	b = np.zeros((8,1))
	row = 0
	for loc in image_pts:
		x = image_pts[loc]['x']
		y = image_pts[loc]['y']
		xw, yw = NbaCourt.get_loc_coords(loc, 'right')
		b[row] = xw
		a[row,:] = [x, y, 1, 0, 0, 0, x*xw, y*xw]
		row += 1
		a[row,:] = [0, 0, 0, x, y, 1, x*yw, y*yw]
		b[row] = yw
		row += 1
	h_vals = np.dot(np.linalg.pinv(a), b)
	h_vals = np.append(h_vals, [[1]], axis=0) # append h_{22} = 1
	h = np.reshape(h_vals, (3, 3))
	return h


if __name__ == '__main__':
	img_num_str = '6584'
	with open('manual_points.json', 'r') as f:
		manual_pts = json.load(f)
	with open('computed_points.json', 'r') as f:
		computed_pts = json.load(f)

	h = compute_homography(manual_pts[img_num_str])

	img_obj = ImageObject('images/{}.jpg'.format(image_num))

	reprojected_pts = []
	for loc in manual_pts:
		xw, yw = NbaCourt.get_loc_coords(loc, 'right')
		# do some shit with h
		p = H * pw
		print [[xw], [yw]]
		p = np.dot(h, [[xw], [yw]])
		print p
		reprojected_pts.append((p[0], p[1]))

	img = img_obj.get_bgr_img()
	hough.put_points_on_img(img, reprojected_pts)
	cv2.imwrite('images/{}_reprojected.jpg'.format(image_num))