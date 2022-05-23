import io
import os.path
import re

import memory

memory = memory.Memory()

def printMemory(auswahl):
    '''print state of memory and registers'''
    # memory_state = memory.getAll()
    # register_state = cpu.getRegister()
    # if auswahl == 0:
    #     pass
    # elif auswahl == 1:
    #     pass
    # elif auswahl == 2:
    #     pass
    pass
    
def readProgram(txt):
    '''
    reads in the program, saves it into the memory and executes Bandbefehle
    '''
    # Abwandlung von bandbefehle.py

    # re to detect TmT commands
    re_txxxxt = re.compile(r"T(\d+)T")

    # re to detect EmE commands, optionally with included other commands (Z)
    re_exxxxe = re.compile(r"E([Z\d\+]+)E")

    # the file to load
    file = os.path.join("data", txt)

    # initial memory writing position
    nextPosition = 0
    with open(file) as f:
        # read linewise
        for line in f.readlines():
            # remove newline at the end of each line
            line = line.strip("\n")
            
            # ignore comments
            if line.startswith("#"):
                continue
                
            # handle TmT commands
            m = re_txxxxt.match(line)
            
            if m:
                nextPosition = int(m.group(1))
                continue
            
            # handle EmE commands
            # (we need to handle those because they disrupt our line counting)
            m = re_exxxxe.match(line)
            if m:
                if "+" in line:
                    input("Press Start to continue...")
                else: 
                    startingPoint = line
            
        
            
            # core: write into memory
            memory.set(nextPosition, line)
            # and increase next counter by one
            nextPosition += 1
    
    #return memory, startingPoint


class ResultPrinter:
    def __init__(self):
        self.strToPrint =""

    def collectPrint(self):
        '''adds the accumulator to strToPrint'''
        #self.strToPrint += memory.get()

        pass
    def printAll(self):
        '''prints all into a text file'''
        #print(self.strToPrint)
        # with open("result.txt", "w") as f:
        #     f.write(self.strToPrint)  
        pass    

if __name__ == '__main__':

    b = ResultPrinter()
    
