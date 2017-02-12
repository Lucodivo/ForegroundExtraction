import unittest
import cv2
import foreground_extraction as fe
import imgconstants as imgc
import os

TEST_OUTPUT_LOC = "TestOutput/"

# Here's our "unit tests".
class WardrobeTests(unittest.TestCase):

  def testFullWardrobeTest(self):
    if(not os.path.exists(TEST_OUTPUT_LOC)):
      os.mkdir(TEST_OUTPUT_LOC)
    img = fe.extract_foreground(imgc.BT1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img1.jpg", img)
    img = fe.extract_foreground(imgc.BT2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img2.jpg", img)
    img = fe.extract_foreground(imgc.BS1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img3.jpg", img)
    img = fe.extract_foreground(imgc.BS2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img4.jpg", img)
    img = fe.extract_foreground(imgc.BYJ1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img5.jpg", img)
    img = fe.extract_foreground(imgc.BYJ1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img6.jpg", img)
    img = fe.extract_foreground(imgc.DJ1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img7.jpg", img)
    img = fe.extract_foreground(imgc.DJ2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img8.jpg", img)
    img = fe.extract_foreground(imgc.IJ1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img9.jpg", img)
    img = fe.extract_foreground(imgc.IJ2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img10.jpg", img)
    img = fe.extract_foreground(imgc.L1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img11.jpg", img)
    img = fe.extract_foreground(imgc.L2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img12.jpg", img)
    img = fe.extract_foreground(imgc.L3)
    cv2.imwrite(TEST_OUTPUT_LOC + "img13.jpg", img)

def main():
  unittest.main()

if __name__ == '__main__':
  main()