import torch
import torch.nn as nn
import numpy as np
import copy
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import confusion_matrix, classification_report




def reFold(data):
        folded = []
        layer = np.zeros(16)
        for i in range(900):
                for j in range(16):
                        layer[j] = data[j + 16*i]
                folded.append(copy.copy(layer))
        return folded

def myConcat(arr1,arr2):
        concat = []
        for i in range(len(arr1)):
                concat.append(copy.copy(arr1[i]))

        for j in range(len(arr2)):
                concat.append(copy.copy(arr2[j]))

        return concat

def fixData(data):
    fList = list(data)
    jList = "".join(fList)
    jList = jList.replace(']','')
    jList = jList.replace('\'','')
    sList = jList.replace('[','')
    sList = sList.split(',')
    aList = np.asarray(sList)
    something = aList[2:].astype(np.float32)
    fSomething = reFold(something)
    return fSomething


PATH="/home/iviti/findRing/model.ckpt"

n_input, n_hidden, n_out, batch_size, learning_rate = 16,16, 1, 1800,0.1

model = nn.Sequential(nn.Linear(n_input, n_hidden),
                      nn.ReLU(),
                      nn.Linear(n_hidden, n_out),
                      nn.Sigmoid()
                      )

model.load_state_dict(torch.load(PATH))
model.eval()
f = open("test.txt")
#f = open("something.txt")
#f = open("nothing.txt")
fSomething = fixData(f)
x = np.asarray(fSomething)
data_x = torch.from_numpy(x)
data_x = data_x.type(torch.float)


correct = 0
total = 0
sumOut = 0
# Test the model
# In test phase, we don't need to compute gradients (for memory efficiency)
with torch.no_grad():
    correct = 0
    total = 0
    for i in range(len(data_x)):
        total = total + 1
        outputs = model(data_x[i])
        print(outputs)
        sumOut = sumOut + outputs
        if outputs >= 0.5:
            correct = correct + 1

print("testing accuracy is ",correct/total)
average = sumOut/total
print("the average value is ",average)
