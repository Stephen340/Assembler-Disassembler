# -*- coding: utf-8 -*-
"""
This file is the disassembler. It will take binary instructions and convert them
into hack assembly language instructions
"""

# This table will include whether a=0 or a=1
compTable = {
    "0101010": "0",
    "0111111": "1",
    "0111010": "-1",
    "0001100": "D",
    "0110000": "A",
    "1110000": "M",
    "0001101": "!D",
    "0110001": "!A",
    "1110001": "!M",
    "0001111": "-D",
    "0110011": "-A",
    "1110011": "-M",
    "0011111": "D+1",
    "0110111": "A+1",
    "1110111": "M+1",
    "0001110": "D-1",
    "0110010": "A-1",
    "1110010": "M-1",
    "0000010": "D+A",
    "1000010": "D+M",
    "0010011": "D-A",
    "1010011": "D-M",
    "0000111": "A-D",
    "1000111": "M-D",
    "0000000": "D&A",
    "1000000": "D&M",
    "0010101": "D|A",
    "1010101": "D|M"
}

destTable = {
    "000": "null",
    "001": "M",
    "010": "D",
    "011": "MD",
    "100": "A",
    "101": "AM",
    "110": "AD",
    "111": "AMD"
}

jumpTable = {
    "000": "null",
    "001": "JGT",
    "010": "JEQ",
    "011": "JGE",
    "100": "JLT",
    "101": "JNE",
    "110": "JLE",
    "111": "JMP"
}


def getCInstruction(line):
    compValue = compTable.get(line[3:10])
    destValue = destTable.get(line[10:13])
    jumpValue = jumpTable.get(line[13:])
    totalLine = destValue + "=" + compValue + ";" + jumpValue
    if destValue == "null":
        totalLine = totalLine.split("=")[1]
    if jumpValue == "null":
        totalLine = totalLine.split(";")[0]
    return totalLine
    
def getAInstruction(line):
    numA = int(line,2)
    totalLine = "@" + str(numA)
    return totalLine

def findAssemblyInstructions():
    fileToRead = input("Enter file name to be read: ")
    toRead = open(fileToRead)
    if toRead.closed:
        quit()
    toWrite = open(fileToRead.replace(".hack",".asm"), "w")
    for line in toRead:
        if len(line) == 0:
            continue
        line = line.strip()
        if line[0:3] == "111":
            val = getCInstruction(line)
        else:
            val = getAInstruction(line)
        toWrite.write(val + "\n")
        
    toRead.close()
    toWrite.close()
    print(fileToRead.replace(".hack", ".asm") + " has been created with the desired asm code.")


findAssemblyInstructions()





