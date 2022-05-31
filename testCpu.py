from util import *
import unittest
from cpu import CPU

class TestUtil(unittest.TestCase):
  def testApplyConditions(self):
    # set up memory
    mem1 = [0 for x in range(0,10)]
    mem1[2] = 5
    
    cpu = CPU(mem1, verbose=False, interactive=False)
    # Put command into Befehlsregister
    
    # Execute single step
    cpu._step(a=0, b="PPQQA2", c="E6")
    
    # Check that results are as expected
    self.assertEquals(mem1[4], 5)
    self.assertEquals(cpu.b, 0)
  
if __name__ == '__main__':
  unittest.main()