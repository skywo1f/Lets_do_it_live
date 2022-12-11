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
	for i in range(7500):
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


f = open("something.txt")
fSomething = fixData(f)

onesArray = np.ones(7500)

f = open("nothing.txt")
fNothing = fixData(f)
zerosArray = np.zeros(7500)

n_input, n_hidden, n_out, batch_size, learning_rate = 16,16, 1, 15000,0.1 
nEpochs = 50000
#data_x = np.concatenate(fSomething,fNothing)
x = np.asarray(myConcat(fSomething,fNothing))
y = np.concatenate((onesArray,zerosArray))


data_x = torch.from_numpy(x)
data_y = torch.from_numpy(y)

scaler = StandardScaler()

data_x = scaler.fit_transform(data_x)
data_x = torch.from_numpy(data_x)
data_x = data_x.type(torch.float)
import pickle
pickle.dump(scaler,open('std_scaler.bin','wb'))

data_y = data_y.type(torch.float)
new_shape = (len(data_y), 1)
data_y = data_y.view(new_shape)


data_x, X_test, data_y, y_test = train_test_split(data_x, data_y, test_size=0.33, random_state=69)



model = nn.Sequential(nn.Linear(n_input, n_hidden),
                      nn.ReLU(),
                      nn.Linear(n_hidden, n_out),
                      nn.Sigmoid()
                      )
print(model)
loss_function = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
#optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

losses = []
for epoch in range(nEpochs):
    pred_y = model(data_x)
    loss = loss_function(pred_y, data_y)
    losses.append(loss.item())

    model.zero_grad()
    loss.backward()

    optimizer.step()
    
torch.save(model.state_dict(), 'model.ckpt')


y_pred_list = []
model.eval()




correct = 0
total = 0
# Test the model
# In test phase, we don't need to compute gradients (for memory efficiency)
with torch.no_grad():
    correct = 0
    total = 0
    for i in range(len(data_x)):
        total = total + 1
        outputs = model(data_x[i])
        if data_y[i] == 0:
            if outputs < 0.5:
                correct = correct + 1
        if data_y[i] == 1:
            if outputs >= 0.5:
                correct = correct + 1

print("training accuracy is {}",correct/total)

correct = 0
total = 0
# Test the model
# In test phase, we don't need to compute gradients (for memory efficiency)
with torch.no_grad():
    correct = 0
    total = 0
    for i in range(len(X_test)):
        total = total + 1
        outputs = model(X_test[i])
        if y_test[i] == 0:
            if outputs < 0.5:
                correct = correct + 1
        if y_test[i] == 1:
            if outputs >= 0.5:
                correct = correct + 1

print("testing accuracy is {}",correct/total)
print("reported accuracy is {}",1-loss)


import matplotlib.pyplot as plt
plt.plot(losses)
plt.ylabel('loss')
plt.xlabel('epoch')
plt.title("Learning rate %f"%(learning_rate))
plt.show()

