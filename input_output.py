import io
import os.path
import re
import csv

#import memory


class IoMemory:
    def __init__(self):
        self.memory_list =[]

    def collectMemory(self, memory):
        '''
        saves the current status of the memory into a list
        '''
        memory_dict = memory.getAll()
        for speicherzelle, speicherinhalt in memory_dict.items():
            memory_dict[speicherzelle] = speicherinhalt.strWort

        self.memory_list.add(memory_dict)
  
    def printMemory(self, old_step, current_step):
        '''
        print state of memory and registers in relation to the status of the memory one step before
        
        '''
       
        memory_change = []

      
        for speicherzelle, old_speicherinhalt in self.memory_list[old_step].items():
        
            new_speicherinhalt = self.memory_list[current_step][speicherzelle]
            if old_speicherinhalt == new_speicherinhalt:
                continue
            else:
                memory_change.append([speicherzelle, old_speicherinhalt, new_speicherinhalt])

        
        with open("Step%s_memory_change.csv" %current_step, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Speicherzelle",old_step, current_step])
            writer.writerows(memory_change)
       
        
    
def readProgram(txt):
    '''
    reads in the program, saves it into the memory and executes Bandbefehle
    '''
    memory = memory.Memory()

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
    
    return memory, startingPoint


if __name__ == '__main__':

    io = IoMemory()
    io.memory_list=[
        {
            "1": "23",
            "2": "24",
            "3": "25",
            "4": "25",
            "5": "25",
            "6": "25",
            "7": "25",
        },
        {
            "1": "25",
            "2": "25",
            "3": "25",
            "4": "25",
            "5": "25",
            "6": "25",
            "7": "25",
            
        }
        ]
    io.printMemory(0,1)

