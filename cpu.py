import re
import memory
import wort

Befehle = {
  'PP': 2,
  'P': 3,
  'QQ': 4,
  'Q': 5,
  'Y': 6,
  'C': 7,
  'N': 8,
  'LL': 9,
  'R': 10,
  'U': 11,
  'A': 12,
  'S': 13,
  'F': 14,
  'K': 15,
  'H': 16,
  'Z': 17,
  'G': 18,
  'V': 19
}

def dec(bl):
  return int("".join([str(x) for x in bl]), 2)

class CPU:
  
  def __init__(self, memory, iomemory, verbose=False, interactive=False):
    self.currentStep = 0
    self.memory = memory
    self.iomemory = iomemory
    self.verbose = verbose
    self.interactive = interactive
  
  def startAt(self, memoryPosition, maxSteps=None):
    """ Launch the computer at the given memory position """
    self._b(self.memory.get(memoryPosition))
    self._c("E" + str(memoryPosition + 1))
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
    self._log("CPU status: b=",str(self._b()), ", c=",str(self._c()), ", a=", self._a())
    
    if a != None:
      self._a(a)
    if b != None:
      self._b(b)
    if c != None:
      self._c(c)

    # 1. Parse the command (to be replaced by other code)
    # if its a 0 or "0", we set befehl and address to 0
    try: 
      befehl = self._b().getBinary() # , address, trommel = self._parseCommand(self._b())
    except SyntaxError:
      self._log("Syntax error: ", self._b())
      befehl = [0]
    
    self._log("Command parsed into: ", befehl)
    
    ## 2. Now we have parsed, we execute the commands.
    
    operands = [self._a(), max(self._schnell(self._b()), self._trommel(self._b()))]
    if self._chk(befehl, 'C'): 
      operands[1] = dec(befehl[20:38])
    
    # Sprungbefehle E and F
    if self._applyConditions(befehl):
      if self._b().isJumpOrCall:
        if self._chk(befehl, 'F'):
          # check for calls of the operating system
          if self._trommel(self._b()) == 644:
            print(self._a())
            return
          elif self._trommel(self._b()) == 800:
            pass
          elif self._trommel(self._b()) == 840:
            pass
          elif self._trommel(self._b()) == 1000:
            pass
          else:
            self.memory.set(5, self._c())
        self._b(self.memory.get(operands[1]))
        self._c("E" + str(operands[1]+1))
        
      
        self._log("CPU status after: b=",str(self._b()), ", c=",str(self._c()), ", a=", self._a())
        self._log("Done with step ", self.currentStep)
        self.currentStep += 1
        return
      elif self._chk(befehl, 'N') and self._chk(befehl, 'A'):
        self._a(self.memory.get(operands[1]))
      # T
      elif self._chk(befehl, 'N') and self._chk(befehl, 'U'):
        self.memory.set(operands[1], self._a())
        self._a(0)
      # LLA
      elif self._chk(befehl, 'LL') and self._chk(befehl, 'A'):
        self._a((self._a().getInt() << 2) + operands[1])
      # RA
      elif self._chk(befehl, 'R') and self._chk(befehl, 'A'):
        self._a((self._a().getInt() >> 1) + operands[1])
      # UA = I
      elif self._chk(befehl, 'U') and self._chk(befehl, 'A'):
        self._a(int(self._a()) & operands[1])
      # A
      elif self._chk(befehl, 'A'):
        self._a(int(self._a()) + operands[1])
      # U
      elif self._chk(befehl, 'U'):
        self.memory.set(operands[1], self._a())
    else:
      self._log("Condition not fulfilled.")
    
    # 3. ... and put the command for getting the next command into the Befehlsregister
    self._b(self._c())
    self.currentStep += 1
    
    # finally, some logging
    self._log("CPU status after: b=",str(self._b()), ", c=",str(self._c()), ", a=", self._a())
    self._log("Done with step ", self.currentStep)
  
  def _chk(self, befehl, btype) -> bool:
    try:
      return befehl[Befehle[btype]] == 1
    except IndexError:
      print(befehl)
      return False
  
  def _trommel(self, befehl) -> int:
    return dec(befehl.getBinary()[25:38])
  
  def _schnell(self, befehl) -> int:
    return dec(befehl.getBinary()[20:25])
  
  def _applyConditions(self, befehl) -> bool:
    if self._chk(befehl, 'PP') and self._chk(befehl, 'QQ'):
      return self._a() == 0 
    if self._chk(befehl, 'PP'):
      return self._a() > 0
    if self._chk(befehl, 'QQ'):
      return self._a() < 0
    if self._chk(befehl, 'P'):
      return self.memory.get(2) >= 0
    if self._chk(befehl, 'Q'):
      return self.memory.get(2) < 0
    if self._chk(befehl, 'Y'):
      return bin(self.memory.get(3))[-1] == "1"
    return True
    
  def _parseCommand(self, commandString):
    """
    Parse the command and return a pair of Befehl and Address. 
    Address can be None, e.g., for the command "D"
    """
    if type(commandString) == str:
      pattern = re.compile(r"^([A-Z]+)(\d+)?$")
      m = pattern.match(str(self.b))
      if not m: 
        raise SyntaxError("Parse Error: " + str(self.b))
      return (m.group(1), int(m.group(2)) if m.group(2) else None)
    elif isinstance(commandString, wort.Wort):
      schnell = commandString.getBinary()[20:25]
      trommel = commandString.getBinary()[25:38]

      return (commandString.getBinary(), schnell, trommel)
    
  def printMemory(self, cell = None):
    """Print a simple image of the entire memory or a single block """
    if cell:
      print((cell, self.memory.get(cell)))
    else:
      print([(index, value) for index, value in enumerate(self.memory) ])
    
  def _log(self, *msg):
    """Log a message, if verbosity is turned on in the object"""
    if self.verbose:
      print("".join([str(x) for x in msg]))
    
  def _a(self, value = None):
    """ Easier set and get access to the accumulator """
    if value:
      if type(value) == int:
        value = str(value)+"'"
      self.memory.set(4, value)
    else:
      return self.memory.get(4)
  
  def _b(self, value = None):
    """ Easier set and get access to the accumulator """
    if value:
      self.memory.set('b', value)
    else:
      return self.memory.get('b')
      
  def _c(self, value = None):
    """ Easier set and get access to the accumulator """
    if value:
      if type(value) == str:
        self.memory.set('c', wort.parse(value))
      else:
        self.memory.set('c', value)
    else:
      return self.memory.get('c')
  
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
  
  program = ["B5", "T112", "B113", "LLA0", "LLA0", "A113", "RA0", "RA0", "RA0", "RA0", "U113", "CUA15", "0'", "12345678'", "B0+1900", "B0+1950", "B1982", "0'", "0'", "0'", "F100", "D", "DX113", "E120"]
  mem1 = memory.Memory()
  
  for index, cmd in enumerate(program):
    mem1.set(index+100, cmd)
  print(mem1.getAll())
  # mem1 = [0 for x in range(0,130)]
  # mem1[100:113] = ["B5", "T112", "B113", "LLA0", "LLA0", "A113", "RA0", "RA0", "RA0", "RA0", "U113", "CI15", 0, 12345678, "B0+1900", "B0+1950", "B1982", 0, 0, 0, "F100", "D", "DX113", "E120"]
  cpu = CPU(mem1, None, verbose=True, interactive=False)
  # cpu.printMemory()
  cpu.startAt(120, maxSteps=1000)
