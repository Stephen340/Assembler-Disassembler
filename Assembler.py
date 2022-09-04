# -*- coding: utf-8 -*-
"""
NAME AND UIN: Stephen Johnson 630006859
Assembler.py

Take a file and convert into necesary instructions.
For reference on step order and process, see 
    LAB 21 - HACK Assembler_ Overall Construction.pptx. and associated video
Included the LAB 22 main method inside of created methods when following LAB 21
    because I was not aware the main would be created separate in LAB 22.
"""

""" We first need our three HashTables, or dictionaries as called in Python """

import re #need this for re.split(). Could do without but looks nicer this way.

#This table will include whether a=0 or a=1
compTable = {
    "0": "0101010", 
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"  
}

destTable = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"   
}

jumpTable = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"    
}

symbolTable = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

""" Populate the symbolTable with the necessary R0-15 values with this for loop"""
for i in range (16):
    symbolTable["R" + str(i)] = i
    
fileToRead = input("Enter file name to be assembled (with the .asm extension): ")
pc = 0 #first open location we can use
nextAddress = 16

def doAInstruction(line):
    global nextAddress
    line = line[:-1]
    chars = set('-_.$:')
    if any((c in chars) for c in line):
        return ""
    if line[0].isalpha():
        if line not in symbolTable:
            symbolTable[line] = nextAddress
            nextAddress += 1
        aValGot = symbolTable.get(line) 
    else:
        aValGot = int(line)
    binaryNum = bin(aValGot)[2:].zfill(16) #convert aValGot to binary code, should be a number at this point
    #need to [2:] becuase otherwise we get the letter 'b' to represent binary. We don't want this.
    return binaryNum
    
def doCInstruction(line):
    line = line[:-1]
    line = line.strip()
    #print(line + "before we modify")
    if "=" not in line: #need to check for dest = comp
        line = "null=" + line
    if ";" not in line: #need to check for jump
        line = line + ";null"
    #use null bc nothing happens so no need for extra checking, keep things simple and clean
    if line[-1] == ";":
        line += "null"
    lists = re.split("=|;", line)
    destRet = destTable.get(lists[0])
    #print(destRet)
    compRet = compTable.get(lists[1])
    #print(lists[1] + "val at [1]")
    #print(compRet)
    jumpRet = jumpTable.get(lists[2])
    #print(jumpRet)
    return compRet, destRet, jumpRet
    

def findInstructions():
    global pc
    toRead = open(fileToRead)
    if toRead.closed:
        quit()
    toTempWrite = open(fileToRead.replace(".asm",".txt"), "w")
    toWrite = open(fileToRead.replace(".asm",".hack"), "w")
    for line in toRead:
        one = line.strip()
        one = one.replace(" ", "")
        clean = one.split("/")[0]
        if len(clean) != 0:
            if clean[0] == "(":
                    label = clean.strip("()")
                    if label not in symbolTable:
                        symbolTable[label] = pc
            else:
                toTempWrite.write(clean + "\n")
                pc += 1
    toTempWrite.close()
    toTempRead = open(fileToRead.replace(".asm",".txt"))
    for line in toTempRead:
        one = line.strip()
        clean = one.split("/")[0]
        gotInstruction = ""
        if len(clean) != 0:
            if clean[0] == "@":
                gotInstruction = doAInstruction(line.strip("@"))
                if not len(gotInstruction) == 0:
                    toWrite.write(gotInstruction + "\n")
            else:
                finLine = doCInstruction(line)
                gotInstruction = "111" + finLine[0] + finLine[1] + finLine[2]
                toWrite.write(gotInstruction + "\n")
    
    toRead.close()
    toWrite.close()
            
findInstructions()  
print(fileToRead.replace(".asm", ".hack") + " has been created with the desired binary code.")
    
