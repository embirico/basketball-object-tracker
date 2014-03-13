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


def put_lines_on_img(bgr_img, lines_rho_theta):
  for rho, theta in lines_rho_theta:
    # print 'The parameters of the line: rho = %s, theta = %s' %(rho, theta)
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(bgr_img,(x1,y1),(x2,y2),(0,0,255),2)

def get_lines(gray, thesh):
  # thresh = 50
  canny = cv2.Canny(gray.copy(), 50, 200)
  # Only find lines for areas above the ESPN score box
  lines = cv2.HoughLines(canny[0:0.79*canny.shape[0]], 1, np.pi/180, thresh)
  bgr = colors.gray_to_bgr(gray)
  if lines is not None:
    put_lines_on_img(bgr, lines[0])
  return bgr
  # call canny
  # call hough

def get_lines_in_groups(gray, thresh):
  canny = cv2.Canny(gray.copy(), 50, 200)
  # Only find lines for areas above the ESPN score box
  lines = cv2.HoughLines(canny[0:0.79*canny.shape[0]], 1, np.pi/180, thresh)
  grouped_lines = group_lines(lines[0])
  best_of_group = [i[0] for i in grouped_lines]
  print 'Number of groups: %s' %(len(grouped_lines))
  for i in range(len(best_of_group)):
    bgr = colors.gray_to_bgr(gray)
    put_lines_on_img(bgr, [best_of_group[i]])
    print best_of_group[i]
    cv2.imwrite('images/grouped_lines_' + str(i) + '.jpg', bgr)

def group_lines(lines_rho_theta):
  line_groups = []
  line_groups.append([(lines_rho_theta[0])])
  print lines_rho_theta[0]

  for rho, theta in lines_rho_theta[1:]:
    new_group = True
    for key in range(len(line_groups)):
      # Append to list if close to existing theta
      if abs(line_groups[key][0][1] - theta) < 0.2:
        line_groups[key].append((rho, theta))
        new_group = False
        break
    if new_group:
      line_groups.append([(rho, theta)])

  for group in line_groups:
    print 'Size of groups: %s' %(len(group))
  return line_groups

if __name__ == '__main__':
  # image_root = 'images/6175'
  image_root = 'images/5993'
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
