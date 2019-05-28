from keras.models import Sequential
from keras.models import load_model
from keras.layers import Input, Dense
from keras.models import Model
import os
import numpy as np
import WSC
from WSC import Comm
import argparse

def train(dataPath, modelsDir, modelName, loadModel, epochs, batches):
    conf = "config/SeqDomain.conf"

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

    dic, sett = WSC.LoadConf(conf)
    test = WSC.GetAllSeqCount(X, dic)

    test = np.array(test)

    inp = Input(shape=(len(test[0]),))

    # 
    hidden = Dense(units=len(test[0]), activation='relu')(inp)
    hidden = Dense(units=64, activation='relu')(hidden)
    hidden = Dense(units=32, activation='relu')(hidden)
    hidden = Dense(units=16, activation='relu')(hidden)
    hidden = Dense(units=8, activation='relu')(hidden)
    hidden = Dense(units=4, activation='relu')(hidden)
    out = Dense(units=1, activation='sigmoid')(hidden)

    # 
    model = Model(inp, out)

    # HERE LOAD WEIGHTS
    if loadModel:
        model.load_weights(f"{modelsDir}/{modelName}/{modelName}.h5")

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(test, Y, epochs=epochs, batch_size=batches)

    # evaluate the model
    scores = model.evaluate(test, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    # 
    if not os.path.isdir(f'{modelsDir}'):
        os.mkdir(f'{modelsDir}')
    
    # 
    if not os.path.isdir(f'{modelsDir}/{modelName}'):
        os.mkdir(f'{modelsDir}/{modelName}')

    # save the model
    model.save(f"{modelsDir}/{modelName}/{modelName}.h5")

    # 
    con = "Inp Size\tEpoch\n"

    # We will update this if we are loading a model & adding to more epochs to it
    nEpoch = 0

    # 
    if loadModel:
        with open(f"{modelsDir}/{modelName}/conf.mc", 'r+') as f:
            epGrab = f.read().split('\n')[1].split('\t')[1]
            nEpoch = int(epGrab)
    
    # 
    con += f'{len(dic)}\t{epochs + nEpoch}'

    # 
    with open(f"{modelsDir}/{modelName}/conf.mc", 'w') as f:
        f.write(con)

    Comm("Saved Model!")