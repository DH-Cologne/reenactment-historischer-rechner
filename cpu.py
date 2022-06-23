import re

class CPU:
  
  def __init__(self, memory, verbose=False, interactive=False):
    self.currentStep = 0
    self.b = 0
    self.c = 0
    self.memory = memory
    self.verbose = verbose
    self.interactive = interactive
  
  def startAt(self, memoryPosition, maxSteps=None):
    """ Launch the computer at the given memory position """
    self.b = str(self.memory[memoryPosition])
    self.c = "E" + str(memoryPosition + 1)
    while(maxSteps==None or self.currentStep < maxSteps):
      self._step()
      if self.interactive:
        input()
    
  def _step(self, a=None, b=None, c=None):
    """ Executes the command currently in b. If it's not a Sprungbefehl, also load c into b. """
    # Interpret self.b as Befehl
    # Ask for its nature (i.e., A, I, ...)
    # Ask for its memory address(es)
    # Ask for its modifiers
    # Execute it
    # (This will need to be partially reimplemented once we have a new representation of the commands)
    
    self._log("CPU executes step ", self.currentStep)
    self._log("CPU status: b=",str(self.b), ", c=",str(self.c), ", a=", self._a())
    
    if a != None:
      self._a(a)
    if b != None:
      self.b = b
    if c != None:
      self.c = c

    # 1. Parse the command (to be replaced by other code)
    # if its a 0 or "0", we set befehl and address to 0
    try: 
      befehl, address = self._parseCommand(self.b)
    except SyntaxError:
      self._log("Syntax error: ", self.b)
      befehl, address = ("0", 0)
    
    self._log("Command parsed into: ", befehl, " ", address)
    
    ## 2. Now we have parsed, we execute the commands.
    
    operands = (self._a(), self.memory[address])
    if "C" in befehl:
      operands[1] = address
    
    # Sprungbefehle E and F
    if self._applyConditions(befehl):
      if befehl == "E" or befehl == "F":
        if befehl == "F":
          self.memory[5] = self.c
        self.b = self.memory[address]
        self.c = "E" + str(address+1)
      
        self._log("CPU status after: b=",str(self.b), ", c=",str(self.c), ", a=", self._a())
        self._log("Done with step ", self.currentStep)
        self.currentStep += 1
        return
      # D
      elif befehl == "D":
        # io.print()
        print(self._a())
      # B
      elif befehl == "B":
        self._a(self.memory[address])
      # T and U
      elif befehl == "T" or befehl == "U":
        self.memory[address] = self._a()
        if befehl == "T":
          self._a(0)
      # LLA
      elif befehl == "LLA":
        self._a((self._a() << 2) + operands[1])
      # A
      elif befehl == "A":
        self._a(self._a() + operands[1])
      # RA
      elif befehl == "RA":
        self._a((self._a() >> 1) + operands[1])
      # CI
      elif befehl == "CI":
        self._a(self._a() & address)
      elif befehl == "DX":
        self.printMemory(address)
    else:
      self._log("Condition not fulfilled.")
    
    # 3. ... and put the command for getting the next command into the Befehlsregister
    self.b = self.c
    self.currentStep += 1
    
    # finally, some logging
    self._log("CPU status after: b=",str(self.b), ", c=",str(self.c), ", a=", self._a())
    self._log("Done with step ", self.currentStep)
  
  def _applyConditions(self, befehl) -> bool:
    if "PPQQ" in befehl:
      return self._a() == 0 
    if "PP" in befehl:
      return self._a() > 0
    if "QQ" in befehl:
      return self._a() < 0
    if "P" in befehl:
      return self.memory[2] >= 0
    if "Q" in befehl:
      return self.memory[2] < 0
    if "Y" in befehl:
      return bin(self.memory[3])[-1] == "1"
    return True
  
  def _parseCommand(self, commandString):
    """
    Parse the command and return a pair of Befehl and Address. 
    Address can be None, e.g., for the command "D"
    """
    pattern = re.compile(r"^([A-Z]+)(\d+)?$")
    m = pattern.match(str(self.b))
    if not m: 
      raise SyntaxError("Parse Error: " + str(self.b))
    return (m.group(1), int(m.group(2)) if m.group(2) else None)
    
  def printMemory(self, cell = None):
    """Print a simple image of the entire memory or a single block """
    if cell:
      print((cell, self.memory[cell]))
    else:
      print([(index, value) for index, value in enumerate(self.memory) ])
    
  def _log(self, *msg):
    """Log a message, if verbosity is turned on in the object"""
    if self.verbose:
      print("".join([str(x) for x in msg]))
    
  def _a(self, value = None):
    """ Easier set and get access to the accumulator """
    if value:
      self.memory[4] = value
    else:
      return self.memory[4]
  
  def getRegister(self, character):
    """
    Return the contents of the given register. Register is given as characters b or c.
    Don't think we need this method
    
    """
    if character == "b": 
      return self.b
    if character == "c":
      return self.c
    pass
  
  def currentStep(self):
    """ Return the current step number """
    return self.currentStep



if __name__=="__main__":
  mem1 = [0 for x in range(0,130)]
  mem1[100:113] = ["B5", "T112", "B113", "LLA0", "LLA0", "A113", "RA0", "RA0", "RA0", "RA0", "U113", "CI15", 0, 12345678, "B0+1900", "B0+1950", "B1982", 0, 0, 0, "F100", "D", "DX113", "E120"]
  cpu = CPU(mem1, verbose=False, interactive=False)
  cpu.printMemory()
  cpu.startAt(120, maxSteps=1000)
