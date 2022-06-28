import input_output
import cpu
import memory

memory,startingPoint = input_output.readProgram("texte.z22")

iomemory = input_output.IoMemory()

cpu = cpu.CPU(memory, iomemory)
cpu.start(startingPoint)
