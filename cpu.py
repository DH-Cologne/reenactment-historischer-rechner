import numpy as np


class CPU:
  a = 4
  """ Shortcut to access the Akkumulator """

  def __init__(self, memory):
    self.currentStep = 0
    self.b = 0
    self.c = 0
    self.memory = memory
  
  def startAt(self, memoryPosition):
    """ Launch the computer at the given memory position """
    self.b = "E" + str(memoryPosition)
    self.c = "E" + str(memoryPosition + 1)
    self._step()
    
  def _step(self):
    """ Executes the command currently in b. If it's not a Sprungbefehl, also load c into b. """
    # Interpret self.b as Befehl
    # Ask for its nature (i.e., A, I, ...)
    # Ask for its memory address(es)
    # Ask for its modifiers
    # Execute it
    pass
   
  def getRegister(self, character):
    """ Return the contents of the given register. Register is given as characters b or c """
    if character == "b": 
      return self.b
    if character == "c":
      return self.c
    pass
  
  def currentStep(self):
    """ Return the current step number """
    return self.currentStep



if __name__=="__main__":
  mem1 = np.zeros(130, dtype="S10")
  mem1[100:112] = ["B5", "T112", "B113", "LLA0", "LLA0", "A113", "RA0", "RA0", "RA0", "RA0", "U113", "CI15"]
  mem1[5] = "E1721"
  cpu = CPU(mem1)
  cpu.startAt(0)
