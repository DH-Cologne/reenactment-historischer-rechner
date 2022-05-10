from util import *
import unittest

class TestUtil(unittest.TestCase):
 def testFromBinary(self):
  self.assertIsInstance(fromBinary("10001010101000"), Befehl)
  
  
if __name__ == '__main__':
 unittest.main()