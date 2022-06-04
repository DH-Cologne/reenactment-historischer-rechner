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
        with open("result.txt", "w") as f:
            f.write(self.strToPrint)  
        pass   