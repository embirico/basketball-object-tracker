# Library imports

import image_object as IO
import json
import numpy as np
import cv2


# Local imports
from image_object import ImageObject
import hough
import colors


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


def compute_homography(image_pts, side):
	a = np.zeros((12,8))
	b = np.zeros((12,1))
	row = 0
	for loc in image_pts:
		x = image_pts[loc]['x']
		y = image_pts[loc]['y']
		xw, yw = NbaCourt.get_loc_coords(loc, side)
		a[row,:] = [xw,yw,1, 0,0,0, 0,0]
		b[row] = x
		row += 1
		a[row,:] = [0,0,0, xw,yw,1, 0,0]
		b[row] = y
		row += 1
		a[row,:] = [0,0,0, 0,0,0, xw,yw]
		b[row] = 0
		row += 1
	h_vals = np.linalg.pinv(a).dot(b)
	h_vals = np.append(h_vals, [[1]], axis=0) # append h_{22} = 1
	h = np.reshape(h_vals, (3, 3))
	return h


if __name__ == '__main__':
	img_num = 5993
	img_num_str = str(img_num)
	side = 'right'
	# img_num_str = '5993'
	with open('manual_points.json', 'r') as f:
		manual_data = json.load(f)
	with open('computed_points.json', 'r') as f:
		computed_data = json.load(f)
	data_img = manual_data[img_num_str]

	h = compute_homography(data_img, side)
	print h

	img_obj = ImageObject('images/{}.jpg'.format(img_num))

	manual_points = []
	reprojected_pts = []
	for loc in data_img:
		print loc
		manual_point = data_img[loc]
		manual_points.append((manual_point['x'], manual_point['y']))
		xw, yw = NbaCourt.get_loc_coords(loc, side)
		print [[xw], [yw], [1]]
		p = h.dot([[xw], [yw], [1]])
		p = p * p[2]
		print data_img[loc]
		print p
		reprojected_pts.append((p[0][0], p[1][0]))

	img = img_obj.get_bgr_img()
	hough.put_points_on_img(img, manual_points, colors.BGR_BLUE)
	hough.put_points_on_img(img, reprojected_pts, colors.BGR_RED)



	# temp = manual_pts[img_num_str]
	# pts = [(temp[loc]['x'], temp[loc]['y']) for loc in temp]
	# hough.put_points_on_img(img, pts)


	cv2.imwrite('images/{}_reprojected.jpg'.format(img_num), img)

	err = np.mean([np.linalg.norm(
		np.asarray(manual_points[i]) - np.asarray(reprojected_pts[i]))
		for i in xrange(len(manual_points))])

	print 'Avg reprojection error: {}px'.format(err)