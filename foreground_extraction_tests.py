import unittest
import cv2
import foreground_extraction as fe
import imgconstants as imgc
import os

TEST_OUTPUT_LOC = "TestOutput/"

# Here's our "unit tests".
class WardrobeTests(unittest.TestCase):

  def testBedSheet(self):
    if(not os.path.exists(TEST_OUTPUT_LOC)):
      os.mkdir(TEST_OUTPUT_LOC)
    img = fe.extract_foreground(imgc.BT2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img2.png", img)
    img = fe.extract_foreground(imgc.BS2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img4.png", img)
    img = fe.extract_foreground(imgc.BYJ2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img6.png", img)
    img = fe.extract_foreground(imgc.DJ2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img8.png", img)
    img = fe.extract_foreground(imgc.IJ2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img10.png", img)
    img = fe.extract_foreground(imgc.L3)
    cv2.imwrite(TEST_OUTPUT_LOC + "img13.png", img)

  def testDoorway(self):
    if(not os.path.exists(TEST_OUTPUT_LOC)):
      os.mkdir(TEST_OUTPUT_LOC)
    img = fe.extract_foreground(imgc.BT1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img1.png", img)
    img = fe.extract_foreground(imgc.BS1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img3.png", img)
    img = fe.extract_foreground(imgc.BYJ1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img5.png", img)
    img = fe.extract_foreground(imgc.DJ1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img7.png", img)
    img = fe.extract_foreground(imgc.IJ1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img9.png", img)

  def testMisc(self):
    img = fe.extract_foreground(imgc.L1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img11.png", img)
    img = fe.extract_foreground(imgc.L2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img12.png", img)
    img = fe.extract_foreground(imgc.H1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img14.png", img)
    img = fe.extract_foreground(imgc.H2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img15.png", img)
    img = fe.extract_foreground(imgc.H3)
    cv2.imwrite(TEST_OUTPUT_LOC + "img16.png", img)
    img = fe.extract_foreground(imgc.H4)
    cv2.imwrite(TEST_OUTPUT_LOC + "img17.png", img)
    img = fe.extract_foreground(imgc.S1)
    cv2.imwrite(TEST_OUTPUT_LOC + "img18.png", img)
    img = fe.extract_foreground(imgc.S2)
    cv2.imwrite(TEST_OUTPUT_LOC + "img19.png", img)

def main():
  unittest.main()

if __name__ == '__main__':
  main()