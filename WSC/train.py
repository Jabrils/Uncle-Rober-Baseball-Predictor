from keras.models import Sequential
from keras.models import load_model
from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
import WSC
from WSC import Comm
import argparse

def train(dataPath, modelName, loadModel, epochs, batches):

    # I MIGHT WANT TO HAVE THIS SAVE A FILE WITH INFO ON IT,
    # LIKE # OF SAMPLES TRAINED ON,
    # TOTAL # EPOCHS
    # INPUT / DICTIONARY SIZE
    # RESOLUTION

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

    inp= Input(shape=(len(test[0]),))

    # Encoder Weights
    hidden = Dense(units=len(test[0]), activation='relu')(inp)
    hidden = Dense(units=32, activation='relu')(hidden)
    hidden = Dense(units=32, activation='relu')(hidden)
    out = Dense(units=1, activation='sigmoid')(hidden)

    model = Model(inp, out)#(f"{modelName}.h5")

    # HERE LOAD WEIGHTS
    if loadModel:
        model.load_weights(f"{modelName}.h5")

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