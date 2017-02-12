import numpy as np
import cv2
import scipy
from scipy import misc

#fgbg = cv2.createBackgroundSubtractorMOG2()
# blurred = cv2.medianBlur(img,5)
# blurred = cv2.GaussianBlur(img, (5, 5), 0)

#fgmask = fgbg.apply(img)
img = cv2.imread('BlueYellowJacket2.jpg')
img = scipy.misc.imresize(img, 0.15)
# apertureSize must be 1,3,5, or 7
edgeImg = cv2.Canny(img, 100, 150, apertureSize=3)

kernel = np.ones((5,5),np.uint8)
# kernel = np.array([[]])
edgeImg = cv2.dilate(edgeImg,kernel,iterations = 2)
edgeImg = cv2.erode(edgeImg,kernel,iterations = 2)
# closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

cv2.namedWindow('frame', flags=cv2.WINDOW_NORMAL)
cv2.imshow('frame',edgeImg)
cv2.waitKey(0)
cv2.destroyAllWindows()

def findSignificantContours (img, edgeImg):
  contours, heirarchy = cv2.findContours(edgeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # Find level 1 contours
  level1 = []
  for i, tupl in enumerate(heirarchy[0]):
  # Each array is in format (Next, Prev, First child, Parent)
  # Filter the ones without parent
    if tupl[3] == -1:
      tupl = np.insert(tupl, 0, [i])
      level1.append(tupl)

     # From among them, find the contours with large surface area.
  significant = []
  tooSmall = edgeImg.size * 2 / 100 # If contour isn't covering 5% of total area of image then it probably is too small
  for tupl in level1:
    contour = contours[tupl[0]];
    area = cv2.contourArea(contour)
    if area > tooSmall:
      significant.append([contour, area])

      # Draw the contour on the original image
      #cv2.drawContours(img, [contour], 0, (0,255,0),2, cv2.CV_AA, maxLevel=1)

  significant.sort(key=lambda x: x[1])
  #print ([x[1] for x in significant]);
  return [x[0] for x in significant];

edgeImg_8u = np.asarray(edgeImg, np.uint8)

# Find contours
significant = findSignificantContours(img, edgeImg_8u)

# Mask
mask = edgeImg.copy()
mask[mask > 0] = 0
cv2.fillPoly(mask, significant, 255)
# Invert mask
mask = np.logical_not(mask)

#Finally remove the background
img[mask] = 0;

cv2.namedWindow('frame', flags=cv2.WINDOW_NORMAL)
cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()