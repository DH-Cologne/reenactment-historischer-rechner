import io
import os.path
import re
import csv
from prettytable import PrettyTable

import memory as mem
#import wort


class IoMemory:
    def __init__(self):
        self.memory_list =[]

    def collectMemory(self, memory):
        '''
        saves the current status of the memory into a list
        '''
        if type(memory) != mem.Memory:
            raise Exception(f"Type {type(memory)} can't be collected") 
        memory_dict = memory.getAll()
        for speicherzelle, speicherinhalt in memory_dict.items():
            memory_dict[speicherzelle] = speicherinhalt.strWort

        # NR: I'm getting this error:
        # AttributeError: 'list' object has no attribute 'add'
        self.memory_list.append(memory_dict)
    # mehrere Steps?
    def printMemory(self,  current_step:int, mode="all", output="console", old_step: int=None ):
        '''
        print state of memory and registers 
        
        Args:

        current_step (int) = The current step 
        mode (str) = ("all" or "changes") "all" when the whole memory (excluded the Speicherzellen containing 0) is needed, "changes" when the differences between the current step and any other step is needed (old_step required)
        output (str) = ("console" or "csv") output method
        old_step (int) = The step to which the changes should be compared
        
        '''
        

        if mode=="all":
            memory_output = []
            for speicherzelle, speicherinhalt in self.memory_list[current_step].items():
            
                if speicherinhalt == 0:
                    continue
                else:
                    memory_output.append([speicherzelle, speicherinhalt])   
            if output=="csv":
                with open("Step%s_memory_status.csv" %current_step, "w") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Speicherzelle", current_step])
                    writer.writerows(memory_output)

            elif output=="console":
                table = PrettyTable()
                table.field_names = ["Speicherzelle",  current_step]
                table.add_rows(memory_output)

                print(table)     
            
            return memory_output
        
        elif mode =="changes":
            memory_change = []
            if old_step == None:
                raise ValueError("Missing old_step parameter")
            elif current_step < old_step: 
                raise Exception('The current_step has to be bigger than the old_step')
            for speicherzelle, new_speicherinhalt in self.memory_list[current_step].items():
                try:
                    old_speicherinhalt = self.memory_list[old_step][speicherzelle]
                except KeyError:
                    old_speicherinhalt = None                
                if new_speicherinhalt == old_speicherinhalt:
                    continue
                else:
                    memory_change.append([speicherzelle, old_speicherinhalt, new_speicherinhalt])
            if output=="csv":
                with open("Step%s_memory_change.csv" %current_step, "w") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Speicherzelle", old_step, current_step])
                    writer.writerows(memory_change)

            elif output=="console":
                table = PrettyTable()
                table.field_names = ["Speicherzelle", old_step, current_step]
                table.add_rows(memory_change)

                print(table)
            return memory_change
        
    
def readProgram(txt):
    '''
    reads in the program, saves it into the memory and executes Bandbefehle
    '''
    memory = mem.Memory()

    # Abwandlung von bandbefehle.py

    # re to detect TmT commands
    re_txxxxt = re.compile(r"T(\d+)T")

    # re to detect EmE commands, optionally with included other commands (Z)
    re_exxxxe = re.compile(r"E([Z\d\+]+)E")

    # the file to load
    #file = os.path.join("data", txt)

    # initial memory writing position
    nextPosition = 0
    with open(txt) as f:
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
                    #input("Press Start to continue...")
                    continue
                else: 
                    startingPoint = int(m.group(1))
            
        
            
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
            #"5": "25",
            "6": "25",
            "7": "25",
        },
        {
            "1": "20",
            "2": "25",
            "3": "25",
            "4": "25",
            "5": "25",
            "6": "26",
            "7": "25",
            
        }
        ]
    print(io.printMemory(current_step=1, mode="changes", output="csv", old_step=0))

