# Library imports
import cv2
import numpy as np

# Local imports
import colors


class ImageObject():
	# Variables
	_bgr_img = None
	_binary_court_mask = None
	_dominant_colorset = None


	def __init__(self, image_name):
		self._bgr_img = cv2.imread(image_name)


	# Exported methods
	def get_binary_court_mask(self):
		if self._binary_court_mask is not None:
			return self.binary_court_mask

		d_c = self.get_dominant_colorset()

		_colors.create_court_mask(self._bgr_img, self.get_dominant_colorset,
			True)


	def get_bgr_img(self):
		return self._bgr_img.copy()


	def get_dominant_colorset(self):
		if self._dominant_colorset is not None:
			return self._dominant_colorset.copy()

		self._dominant_colorset = colors.get_dominant_colorset(self.get_bgr_img)
		return self._dominant_colorset


if __name__ == '__main__':
	image_root = 'images/5993'
	image_ext = '.jpg'
	image_name = image_root + image_ext
	img_obj = ImageObject(image_name)
	img_obj.get_binary_court_mask()