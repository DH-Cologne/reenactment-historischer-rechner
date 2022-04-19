#!python3

import io
import os.path
import re

# representation of the trommelspeicher as a long list 
# (this is "a bit" wasteful)
memory = [0 for x in range(0, 2**13)]

# re to detect TmT commands
re_txxxxt = re.compile(r"T(\d+)T")

# re to detect EmE commands, optionally with included other commands (Z)
re_exxxxe = re.compile(r"E([Z\d\+]+)E")

# the file to load
file = os.path.join("data", "texte.z22")

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
            continue
        
        # core: write into memory
        memory[nextPosition] = line
        # and increase next counter by one
        nextPosition += 1

# print memory in an excel-friendly form,
# skipping all 0-cells
for i in range(len(memory)):
    if memory[i] != 0:
        print(i, end="\t")
        print(memory[i])
