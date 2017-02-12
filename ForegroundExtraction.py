import numpy as np
import cv2
import scipy
from scipy import misc

#fgbg = cv2.createBackgroundSubtractorMOG2()
# blurred = cv2.medianBlur(img,5)
# blurred = cv2.GaussianBlur(img, (5, 5), 0)

#fgmask = fgbg.apply(img)
img = cv2.imread('TestImages/BlackShirt2.jpg')
img = scipy.misc.imresize(img, 0.2)
# apertureSize must be 1,3,5, or 7
edgeImg = cv2.Canny(img, 100, 200, apertureSize=3)

kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

edgeImg = cv2.dilate(edgeImg,kernel_dilate,iterations = 3 )
edgeImg = cv2.erode(edgeImg,kernel_erode,iterations = 2)

# # closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

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
  # compute the center of the contour
  changeX, changeY = (0,0)

  percent_scale = 90
  c = [x[0] for x in significant]
  for arr in c:
    M = cv2.moments(np.array(arr))
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    arr = arr*percent_scale/100
    M2 = cv2.moments(np.array(arr))
    cX2 = int(M2["m10"] / M2["m00"])
    cY2 = int(M2["m01"] / M2["m00"])

    changeX = cX-cX2
    changeY = cY-cY2

  

  changes = [changeX, changeY]
  significant = np.asarray(significant)
  significant[0][0][:] = (significant[0][0][:]*percent_scale/100)+changes
  print significant[0][0][:]
  return [x[0] for x in significant]

edgeImg_8u = np.asarray(edgeImg, np.uint8)

# Find contours
significant = findSignificantContours(img, edgeImg_8u)
print significant[0][0][0]
# Mask
mask = edgeImg.copy()
mask[mask > 0] = 0
cv2.fillPoly(mask, significant, 255, lineType=cv2.CV_AA)
# Invert mask
mask = np.logical_not(mask)

#Finally remove the background
img[mask] = 0;

cv2.namedWindow('frame', flags=cv2.WINDOW_NORMAL)
cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()