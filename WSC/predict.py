from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import numpy as np
import WSC

X = []
Y = []

dataPath = "data/test.txt"

# Load the data & split it by line breaks
with open(dataPath) as t:
    new = t.read().split('\n')

print("N",new)

# Split the data again but this time by a tab. This will make 0 the sequence & 1 the label
for i in range(len(new)):
    grab = new[i].split('\t')
    X.append(grab[0])
    Y.append(int(grab[1]))

print("X",X)

# CORRECT

dic = WSC.LoadSeq("config/SeqDomain.txt")
test = WSC.GetAllSeqCount(dataPath, dic)

print("T", test)

test = np.array(test)

print("F", test)

model = load_model("model.h5")

# calculate predictions
predictions = model.predict(test)

for i in range(len(predictions)):
    print(predictions[i][0], int(round(predictions[i][0])), Y[i]) 