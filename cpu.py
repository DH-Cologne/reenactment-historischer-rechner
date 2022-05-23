class CPU:
  def __init__(self, memory):
    self.currentStep = 0
    self.b = 0
    self.c = 0
    self.memory = memory
  
  def startAt(self, memoryPosition):
    ''' Launches the computer at the given memory position '''
    pass
   
  def getRegister(self, character):
    ''' Returns the contents of the given register. Register is given as characters b or c '''
    if character == "b": 
      return self.b
    if character == "c":
      return self.c
    pass
  
  def currentStep(self):
    ''' Returns the current step number '''
    return self.currentStep