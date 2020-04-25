# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 12:56:42 2020

@author: iviti
"""

import string

file1 = open('sampleTabs.txt', 'r')                 #read sample tabs file
Lines = file1.readlines()                           #load file into lines
li = []                                             #declare arrays
coordsG = []
coordsD = []
coordsA = []
coordsE = []
masterC = []
masterT = []
finalC = []
finalT = []
finalCombo = []
for i in range(4):
    li.append(list(Lines[i].split("”")))            #get rid of some of the extra things
    

for i in range(len(li[0])):                         #get rid of more extra things, but leave some spaces
    if li[0][i] == "â€":                            #if weird dash, then leave poisoned value
        coordsG.append(30)
    else:                                           #if number then record it and put a space after
        temp = li[0][i].split("â€")
        if temp[0] != "\n":
            coordsG.append(temp[0])  
        coordsG.append(30)
            
for i in range(len(li[1])):                             #same with the other coords
    if li[1][i] == "â€":
        coordsD.append(30)
    else:
        temp = li[1][i].split("â€")
        if temp[0] != "\n":
            coordsD.append(temp[0])
        coordsD.append(30)
            
for i in range(len(li[2])):
    if li[2][i] == "â€":
        coordsA.append(30)
    else:
        temp = li[2][i].split("â€")
        if temp[0] != "\n":
            coordsA.append(temp[0])
        coordsA.append(30)
            
for i in range(len(li[3])):
    if li[3][i] == "â€":
        coordsE.append(30)
    else:
        temp = li[3][i].split("â€")
        if temp[0] != "\n":
            coordsE.append(temp[0])
        coordsE.append(30)
            
for i in range(len(coordsG)):                       #clean it up a bit more
    if int(coordsG[i]) < 30:                        #write down actual numbers
        masterC.append(coordsG[i])
        masterT.append(3)
    elif int(coordsD[i]) < 30:
        masterC.append(coordsD[i])
        masterT.append(2)
    elif int(coordsA[i]) < 30:
        masterC.append(coordsA[i])
        masterT.append(1)
    elif int(coordsE[i]) < 30:
        masterC.append(coordsE[i])
        masterT.append(0)
    else:
        masterC.append(30)                      #convert from 4 arrays into 2
        masterT.append(5)
        
for i in range(int(len(masterC)/2)):                #take care of extra spacing
    if int(masterC[i*2])  < 30:
        finalC.append(int(masterC[i*2]))
        finalT.append(masterT[i*2])
    elif int(masterC[i*2 + 1]) < 30:
        finalC.append(int(masterC[i*2 + 1]))
        finalT.append(masterT[i*2 + 1])    
    else:
        finalC.append(30)
        finalT.append(5)
    finalCombo.append((finalC[i],finalT[i]))            #combine into 1 array of tuples

rep1 = str(finalCombo).replace('(', '{')
rep2 = rep1.replace(')','}')
rep3 = rep2.replace('[','{')
rep4 = rep3.replace(']','}')                            #convert to arduino format

file1 = open('thisSong.txt', 'w')                           #save file
file1.writelines(rep4) 
file1.close() 
print(len(finalC))