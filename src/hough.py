# Imports ---------------------------------------

import cv
import cv2
import numpy as np
from matplotlib import pyplot as plt

import colors # local reference

def put_lines_on_img(bgr_img, lines_rho_theta):
  redness = np.linspace(0, 255, len(lines_rho_theta))
  redness = np.floor(redness)
  blueness = 255 - redness
  for i, (rho, theta) in enumerate(lines_rho_theta):
    # print 'The parameters of the line: rho = %s, theta = %s' %(rho, theta)
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    red = redness[i]
    blue = blueness[i]
    cv2.line(bgr_img,(x1,y1),(x2,y2),(blue,0,red),2)


def put_points_on_img(bgr_img, points, color=colors.BGR_RED):
  for float_point in points:
    point = tuple([int(x) for x in float_point])
    cv2.circle(bgr_img, point, 8, color, -1)


# Original get lines
# def get_lines(gray, thresh=55):
#   flooded = colors.fill_holes_with_contour_filling(gray, inverse=True)
#   cv2.imwrite('images/mask_black_flooded.jpg', flooded)
#   canny = cv2.Canny(flooded.copy(), 50, 200)
#   # Only find lines for areas above the ESPN score box
#   lines = cv2.HoughLines(canny[0:0.79*canny.shape[0]], 1, np.pi/180, thresh)
#   bgr = colors.gray_to_bgr(gray)
#   if lines is not None:
#     print image_name
#     bgr = cv2.imread(image_name)
#     put_lines_on_img(bgr, lines[0])
#     # put_lines_on_img(bgr, lines[0])
#   return bgr
#   # call canny
#   # call hough

def get_lines_from_paint(gray_flooded2, sideline, baseline, verbose=False):
  THRESH = 50

  OFFSET_X = 0.01
  OFFSET_Y = 0.2
  # ANGLE_DIFF = .35
  # DIST_DIFF = 50
  ANGLE_DIFF = .25
  ANGLE_DIFF_2 = .35
  DIST_DIFF = 50
  parr = lambda theta1, theta2: abs(theta2 - theta1) < ANGLE_DIFF
  far = lambda rho1, rho2: abs(rho2 - rho1) > DIST_DIFF
  parr2 = lambda theta1, theta2: abs(theta2 - theta1) < ANGLE_DIFF_2

  canny = cv2.Canny(gray_flooded2.copy(), 50, 200)
  padded_canny = np.zeros(canny.shape, np.uint8)
  y_range_left = OFFSET_Y*canny.shape[0]
  y_range_right = 0.75*canny.shape[0]
  x_range_left = OFFSET_X*canny.shape[1]
  x_range_right = .9*canny.shape[1]
  padded_canny[y_range_left:y_range_right, x_range_left:x_range_right] = \
    canny[y_range_left:y_range_right, x_range_left:x_range_right]

  lines = cv2.HoughLines(padded_canny, 1, np.pi/180, THRESH)

  if verbose:
    img = colors.gray_to_bgr(gray_flooded2)
    put_lines_on_img(img, lines[0])
    cv2.imwrite('images/hough.jpg', img)

  freethrowline = None
  paintline = None
  for line in lines[0]:
    rho, theta = line
    if freethrowline is None and parr(theta, baseline[1]) and far(rho, baseline[0]):
      freethrowline = line
    if paintline is None and parr2(theta, sideline[1]) and far(rho, sideline[0]):
      paintline = line
    if paintline is not None and freethrowline is not None:
      return (freethrowline, paintline)

  print 'REACHED END OF FOR LOOP'
  return (freethrowline, paintline)









  # grouped_lines = group_lines(lines[0])
  # # best_of_group = [i[0] for i in grouped_lines]
  # print 'Number of groups: %s' %(len(grouped_lines))
  # for i in range(len(grouped_lines)):
  #   bgr = colors.gray_to_bgr(gray)
  #   # put_lines_on_img(bgr, [best_of_group[i]])
  #   put_lines_on_img(bgr, grouped_lines[i])
  #   # print best_of_group[i]
  #   cv2.imwrite('images/grouped_lines_' + str(i) + '.jpg', bgr)


# def group_lines(lines_rho_theta):
#   line_groups = []
#   line_groups.append([(lines_rho_theta[0])])

#   for rho, theta in lines_rho_theta[1:]:
#     new_group = True
#     for key in range(len(line_groups)):
#       # Append to list if close to existing theta
#       if abs(line_groups[key][0][1] - theta) < 0.2:
#         line_groups[key].append((rho, theta))
#         new_group = False
#         break
#     if new_group:
#       line_groups.append([(rho, theta)])

#   # for group in line_groups:
#   #   print 'Size of groups: %s' %(len(group))
#   return line_groups


if __name__ == '__main__':
  image_root = 'images/6373'
  # image_root = 'images/5993'
  image_ext = '.jpg'
  image_name = image_root + image_ext

  court_mask = colors.create_court_mask(image_name, binary_gray=True)
  cv2.imwrite('images/mask.jpg', court_mask)
  flooded = fill_holes_with_contour_filling(court_mask)
  cv2.imwrite('images/mask_flooded.jpg', flooded)

  get_lines_in_groups(flooded, 50)

  # for thresh in xrange(30, 80, 5):theta
  #   with_lines = get_lines(flooded, thresh)
  #   cv2.imwrite('images/mask_lined{}.jpg'.format(thresh), with_lines)

  # court_mask = colors.ycbcr_to_binary(court_mask)
  # plt.imshow(court_mask)
  # plt.show()
  # edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)




# Unused code kept for the report etc -----------

# See https://github.com/Itseez/opencv/blob/master/samples/python2/floodfill.py
# def flood_holes(gray):
#   # Setup
#   flooded = gray.copy()
#   flooded = cv2.bitwise_not(flooded)
#   h, w = gray.shape[:2]
#   mask = np.zeros((h+2, w+2), np.uint8)
#   connectivity = 4
#   flags = connectivity
#   lo = 128
#   hi = 128

#   # Do
#   seed_pt = (400, 10)
#   cv2.floodFill(flooded, mask, seed_pt, (255,), lo, hi, flags)
#   flooded = colors.gray_to_bgr(flooded)
#   cv2.circle(flooded, seed_pt, 2, (0, 0, 255), -1)


#   return cv2.bitwise_not(flooded)




# def fill_holes_with_img_opening(gray):
#   gray = cv2.bitwise_not(gray)
#   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#   res = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)
#   res = cv2.bitwise_not(res)
#   return res
