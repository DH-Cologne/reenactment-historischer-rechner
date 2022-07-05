import input_output
import cpu
from sys import argv

filePath =argv[1]
memory,startingPoint = input_output.readProgram(filePath)

iomemory = input_output.IoMemory()

cpu = cpu.CPU(memory, iomemory)
cpu.start(startingPoint)
