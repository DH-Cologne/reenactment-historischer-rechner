import input_output
import cpu
import memory

memory,startingPoint = input_output.readProgram("texte.z22")

cpu = cpu.CPU(memory)
cpu.start(startingPoint)
