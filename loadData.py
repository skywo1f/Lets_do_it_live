import numpy as np



f = open("test.txt")
fList = list(f)
#print(fList)
jList = "".join(fList)
jList = jList.replace(']','')
jList = jList.replace('\'','')
sList = jList.split('[')
#print(sList)
aList = np.asarray(sList)
aList = aList[2:]
print(len(aList))
print(aList[0])
print(aList[99])
