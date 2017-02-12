import numpy as np
import cv2
import scipy
from scipy import misc

def extract_foreground(imgloc):
  img = cv2.imread(imgloc)
  img = scipy.misc.imresize(img, 0.20) # apertureSize must be 1,3,5, or 7
  edgeImg = cv2.Canny(img, 100, 200, apertureSize=3)  # threshold may need to be a function of dimensions of image

  kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
  kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

  edgeImg = cv2.dilate(edgeImg, kernel_dilate, iterations=3)
  edgeImg = cv2.erode(edgeImg, kernel_erode, iterations=2)

  def findSignificantContours(img, edgeImg):
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
    tooSmall = edgeImg.size * 5 / 100  # If contour isn't covering 5% of total area of image then it probably is too small
    for tupl in level1:
      contour = contours[tupl[0]];
      area = cv2.contourArea(contour)
      if area > tooSmall:
        significant.append([contour, area])

        # Draw the contour on the original image (this helps remove border)
        cv2.drawContours(img, [contour], 0, (0,0,0),3, cv2.CV_AA, maxLevel=1)

    significant.sort(key=lambda x: x[1])
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

  # Finally remove the background
  img[mask] = 0

  return img