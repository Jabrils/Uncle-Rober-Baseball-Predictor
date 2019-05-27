from keras.models import Sequential
from keras.layers import Dense
from keras.models import Model
import numpy as np
import WSC
from WSC import Comm
import argparse

def train(dataPath, modelName, epochs, batches):
    X = []
    Y = []

    # Load the data & split it by line breaks
    with open(dataPath) as t:
        new = t.read().split('\n')

    # Split the data again but this time by a tab. This will make 0 the sequence & 1 the label
    for i in range(len(new)-1):
        grab = new[i].split('\t')
        X.append(grab[0])
        Y.append(int(grab[1]))

    dic = WSC.LoadSeq("config/SeqDomain.txt")
    test = WSC.GetAllSeqCount(X, dic)

    test = np.array(test)

    # create model
    model = Sequential()
    model.add(Dense(32, input_dim=len(test[0]), activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(test, Y, epochs=epochs, batch_size=batches)

    # evaluate the model
    scores = model.evaluate(test, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    # save the model
    model.save(f"{modelName}.h5")

    Comm("Saved Model!")