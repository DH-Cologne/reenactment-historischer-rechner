import input_output
import cpu
from sys import argv

filePath = argv[1]
if len(argv) > 2:
  maxSteps = int(argv[2])
else:
  maxSteps = None
memory, startingPoint = input_output.readProgram(filePath)

iomemory = input_output.IoMemory()

cpu = cpu.CPU(memory, iomemory, verbose=False)
cpu.startAt(startingPoint, maxSteps=maxSteps)
