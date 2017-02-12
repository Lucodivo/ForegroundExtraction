import numpy as np
import cv2
import scipy
from scipy import misc
import imgconstants as imgc

def extract_foreground(imgloc):
  img = cv2.imread(imgloc)
  aspect_ratio = float(img.shape[0])/img.shape[1]
  set_w = 450
  set_h = int(set_w*aspect_ratio)

  if img.shape[1] > set_w:
    img = scipy.misc.imresize(img, (set_h, set_w, 3))

  min_threshold = 25 # 25 and 75 does best for sheets
  max_threshold = 75
  # apertureSize must be 1,3,5, or 7
  edgeImg = cv2.Canny(img, min_threshold, max_threshold, apertureSize=3)  # threshold may need to be a function of dimensions of image

  kernel_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
  kernel_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

  # cv2.namedWindow('frame', flags=cv2.WINDOW_NORMAL)
  # cv2.imshow('frame',edgeImg)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()

  def findSignificantContours(img, edgeImg, borderMultiplier):
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
    counter = 0
    tooSmall = edgeImg.size * 10 / 100  # If contour isn't covering 5% of total area of image then it probably is too small
    for tupl in level1:
      contour = contours[tupl[0]];
      area = cv2.contourArea(contour)
      if area != 0:
        counter += 1
      if area > tooSmall:
        significant.append([contour, area])

        # Draw the contour on the original image (this helps remove border)
        cv2.drawContours(img, [contour], 0, (0,0,0),5*borderMultiplier, cv2.CV_AA, maxLevel=1)

    significant.sort(key=lambda x: x[1])
    print imgloc + " COUNTER: " + str(counter)

    return [x[0] for x in significant];

  foundContour = False
  borderMultiplier = 1
  while not foundContour:
    edgeImg_8u = np.asarray(edgeImg, np.uint8)

    # Find contours
    significant = findSignificantContours(img, edgeImg_8u, borderMultiplier)

    # Mask
    mask = edgeImg.copy()
    mask[mask > 0] = 0
    cv2.fillPoly(mask, significant, 255)

    if mask[img.shape[0]/2, img.shape[1]/2] == 0:
      edgeImg = cv2.dilate(edgeImg, kernel_dilate, iterations=2)
      edgeImg = cv2.erode(edgeImg, kernel_erode, iterations=1)
      if borderMultiplier < 3:
        borderMultiplier += 1
    else:
      foundContour = True


  # Invert mask
  mask = np.logical_not(mask)

  # Finally remove the background
  img[mask] = 0

  return img

