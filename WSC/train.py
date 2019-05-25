from keras.models import Sequential
from keras.layers import Dense
from keras.models import Model
import numpy as np
import WSC

X = []
Y = []

dataPath = "data/train.txt"

# Load the data & split it by line breaks
with open(dataPath) as t:
    new = t.read().split('\n')

# Split the data again but this time by a tab. This will make 0 the sequence & 1 the label
for i in range(len(new)):
    grab = new[i].split('\t')
    X.append(grab[0])
    Y.append(int(grab[1]))

dic = WSC.LoadSeq("config/SeqDomain.txt")
test = WSC.GetAllSeqCount(dataPath, dic)

test = np.array(test)

# create model
model = Sequential()
model.add(Dense(32, input_dim=len(test[0]), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(test, Y, epochs=1000, batch_size=512)

# evaluate the model
scores = model.evaluate(test, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# save the model
model.save("model.h5")

# # calculate predictions
# predictions = model.predict(test)

# for i in range(len(predictions)):
#     print(predictions[i][0], round(predictions[i][0]), Y[i]) 