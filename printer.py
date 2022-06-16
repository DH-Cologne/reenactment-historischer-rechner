class ResultPrinter:
    def __init__(self):
        self.strToPrint =""

    def collectPrint(self, accumulator):
        '''adds the accumulator to strToPrint'''
        self.strToPrint += accumulator.strWort + "\n"

        pass
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
               


# Test accumulator Klasse Wort
#