from util import *
import unittest
import input_output
import memory as m
import wort
import printer as p


class IOtest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_file_path = "data/texte.z22"
    
    def testPrintingMemory(self):

        # memory version without special cases
        iomemory_standard = input_output.IoMemory()
        iomemory_standard.memory_list=[
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
                "1": "20",
                "2": "25",
                "3": "25",
                "4": "25",
                "5": "25",
                "6": "26",
                "7": "25",
                
            }
        ]

        # memory version with new key-value pair in the later memory state
        iomemory_missing_cell = input_output.IoMemory()
        iomemory_missing_cell.memory_list=[
            {
                "1": "23",
                "2": "24",
                "3": "25",
                "4": "25",
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
        # testing correct outputs
        self.assertEqual([['1', '23', '20'], ['2', '24', '25'], ['6', '25', '26']],iomemory_standard.printMemory(current_step=1, mode="changes", output="csv", old_step=0))
        self.assertEqual([['1', '20'], ['2', '25'], ['3', '25'], ['4', '25'], ['5', '25'], ['6', '26'], ['7', '25']],iomemory_standard.printMemory(current_step=1, mode="all", output="csv")) 
        self.assertEqual([['1', '23', '20'], ['2', '24', '25'], ['5', None, '25'], ['6', '25', '26']],iomemory_missing_cell.printMemory(current_step=1, mode="changes", output="csv", old_step=0))
        
        # testing Exceptions with missing/wrong parameters
        self.assertRaises(Exception, iomemory_standard.printMemory, current_step=1, mode="changes", output="csv", old_step=5)
        self.assertRaises(Exception, iomemory_standard.printMemory, current_step=1, mode="changes", output="csv")


    def testReadingInProgram(self):
        memory, startingPoint = input_output.readProgram(self.test_file_path)
        # testing if the returned objects are correct
        self.assertIsInstance(memory, m.Memory)
        self.assertIsInstance(startingPoint, int)
        self.assertIsInstance(memory.get(startingPoint), wort.Wort)

    def testCollectingMemory(self):
        memory, startingPoint = input_output.readProgram(self.test_file_path)

        iomemory_collecting = input_output.IoMemory()
        #testing exceptions that are risen when trying to collect non-memory objects
        self.assertRaises(Exception, iomemory_collecting.collectMemory, "String")
        self.assertRaises(Exception, iomemory_collecting.collectMemory, 12)


        iomemory_collecting.collectMemory(memory)
        # testing correct internal structure
        self.assertIsInstance(iomemory_collecting.memory_list, list)
        self.assertIsInstance(iomemory_collecting.memory_list[0], dict)

    def testPrinter(self):
        printer = p.ResultPrinter()
        
        # testing exceptions that are risen when trying to collect non-Wort objects
        self.assertRaises(Exception, printer.collectPrint, 12)
        self.assertRaises(Exception, printer.collectPrint, "String")

        # testing exceptions that are risen when "mode" args are incorrect
        self.assertRaises(Exception, printer.printAll, "pdf")
        self.assertRaises(Exception, printer.printAll, 1)

        resultstring = printer.strToPrint
        # Minimum characters of Theo Lutz' result text
        comparable = 2200
        # Testing if the result string has a certain length of characters
        self.assertLess(comparable < len(resultstring))

if __name__ == '__main__':

 unittest.main()
