# Imports ---------------------------------------

import cv
import cv2
import numpy as np
from matplotlib import pyplot as plt

import colors # local reference


def fill_holes_with_contour_filling(gray):
  filled = gray.copy()
  contour, _ = cv2.findContours(filled,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  for cnt in contour:
    cv2.drawContours(filled, [cnt], 0, 255, -1)
  return filled


def get_lines(gray):
  pass
  # call canny
  # call hough


if __name__ == '__main__':
  # image_root = 'images/6175'
  image_root = 'images/5993'
  image_ext = '.jpg'
  image_name = image_root + image_ext
  court_mask = colors.create_court_mask(image_name, binary_gray=True)
  cv2.imwrite('images/mask.jpg', court_mask)
  flooded = fill_holes_with_contour_filling(court_mask)
  cv2.imwrite('images/mask_flooded3.jpg', flooded)
  # court_mask = colors.ycbcr_to_binary(court_mask)
  # plt.imshow(court_mask)
  # plt.show()
  # edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)


# Unused code kept for the report etc -----------


# See https://github.com/Itseez/opencv/blob/master/samples/python2/floodfill.py
def flood_holes(gray):
  # Setup
  flooded = gray.copy()
  h, w = gray.shape[:2]
  mask = np.zeros((h+2, w+2), np.uint8)
  connectivity = 4
  flags = connectivity
  lo = 128
  hi = 128

  # Do
  seed_pt = (350, 350)
  cv2.floodFill(flooded, mask, seed_pt, (255,), lo, hi, flags)
  flooded = colors.gray_to_bgr(flooded)
  cv2.circle(flooded, seed_pt, 2, (0, 0, 255), -1)

  return flooded


def fill_holes_with_img_opening(gray):
  gray = cv2.bitwise_not(gray)
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
  res = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)
  res = cv2.bitwise_not(res)
  return res
