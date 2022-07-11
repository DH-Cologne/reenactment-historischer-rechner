import wort
#import input_output
class ResultPrinter:
    def __init__(self):
        self.strToPrint =""

    def collectPrint(self, accumulator):
        '''adds the accumulator to strToPrint'''
        if isinstance(accumulator, wort.Wort) == False:
            raise Exception (f"{type(accumulator)} can't be collected")
        self.strToPrint += accumulator.strWort + "\n"

        
    def printAll(self, mode="console"):
        '''
        prints content of strToPrint into a text file
        
        Args:
        mode (str) = ("console" or "txt") output method

        '''
        if mode=="console":
            print(self.strToPrint)
        elif mode=="txt":
            with open("result.txt", "w") as f:
                f.write(self.strToPrint)  
               


# if __name__ == '__main__':
    # memory, startingPoint = input_output.readProgram("data/texte.z22")
    # rp = ResultPrinter()
    # print(type(memory.get(1720)))
    # rp.collectPrint(memory.get(1720))
    # rp.printAll()
