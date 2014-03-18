# Library imports

import image_object as IO
import json
import numpy as np
import cv2


# Local imports
from image_object import ImageObject
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
		a[row,:] = [x, y, 1, 0, 0, 0, x*xw, y*xw]
		b[row] = xw
		row += 1
		a[row,:] = [0, 0, 0, x, y, 1, x*yw, y*yw]
		b[row] = yw
		row += 1
	h_vals = np.dot(np.linalg.pinv(a), b)
	h_vals = np.append(h_vals, [[1]], axis=0) # append h_{22} = 1
	h = np.reshape(h_vals, (3, 3))
	return h


if __name__ == '__main__':
	img_num = 5993
	img_num_str = str(img_num)
	with open('manual_points.json', 'r') as f:
		manual_pts = json.load(f)
	with open('computed_points.json', 'r') as f:
		computed_pts = json.load(f)

	h = compute_homography(manual_pts[img_num_str])
	print h

	img_obj = ImageObject('images/{}.jpg'.format(img_num))

	reprojected_pts = []
	for loc in manual_pts[img_num_str]:
		print loc
		xw, yw = NbaCourt.get_loc_coords(loc, 'right')
		print [[xw], [yw]]
		# p = np.dot(h, [[xw], [yw], [1]])
		p = np.dot(h, [xw, yw, 1])
		p = p / p[2]
		print p
		reprojected_pts.append((p[0], p[1]))

	img = img_obj.get_bgr_img()
	hough.put_points_on_img(img, reprojected_pts)



	# temp = manual_pts[img_num_str]
	# pts = [(temp[loc]['x'], temp[loc]['y']) for loc in temp]
	# hough.put_points_on_img(img, pts)


	cv2.imwrite('images/{}_reprojected.jpg'.format(img_num), img)