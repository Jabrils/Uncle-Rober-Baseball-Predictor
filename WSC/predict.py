from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import numpy as np
import WSC
from WSC import Comm
import argparse
import time
import datetime

def predict(dataPath, modelDir, modelName):
    X = []
    Y = []
    hasLabel = False

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    Comm(f"LOADING {dataPath}!")

    # Load the data & split it by line breaks
    with open(dataPath) as t:
        new = t.read().split('\n')

    # Split the data again but this time by a tab. This will make 0 the sequence & 1 the label
    for i in range(len(new)):
        grab = new[i].split('\t')
        X.append(grab[0])

        # 
        if len(grab) > 1:
            Y.append(int(grab[1]))
            hasLabel = True

    # 
    dic = WSC.LoadSeq("config/SeqDomain.txt")
    test = WSC.GetAllSeqCount(X, dic)

    # 
    test = np.array(test)

    # 
    model = load_model(f"{modelDir}/{modelName}/{modelName}.h5")

    # calculate predictions
    predictions = model.predict(test)

    # 
    err = 0

    # 
    for i in range(len(predictions)):
        guess = int(round(predictions[i][0]))

        if hasLabel:
            err += abs(Y[i] - int(round(predictions[i][0])))
            tp += 1 if guess == 1 and Y[i] == 1 else 0
            fp += 1 if guess == 1 and Y[i] == 0 else 0
            fn += 1 if Y[i] == 1 and guess == 0 else 0
            tn += 1 if Y[i] == 0 and guess == 0 else 0

            print(f'Ind: {i}\tSeq: {X[i]}\tPred: {predictions[i][0]}\tGuess: {guess}\tLabel: {Y[i]}\tError: {abs(Y[i] - int(round(predictions[i][0])))}') 
        else:
            print(f'Ind: {i}\tSeq: {X[i]}\tPred: {predictions[i][0]}\tGuess: {guess}') 

    # 
    if hasLabel:
        acc = round((1-(err/len(predictions)))*10000)/100
        prec = round((tp/(tp+fp))*10000)/100
        rec = round((tp/(tp+fn))*10000)/100
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S')

        Comm(f'{acc}% Accurate')

        print("When a 'steal' was predicted by the algorithm, how many of those predicted 'steals' were actually 'steal' labled?")
        Comm(f'Steal Precision: {prec}%')
        print("Out of all the actual 'steals' within the dataset, how many of those were correctly predicted?")
        Comm(f'Steal Recall: {rec}%')

        with open('data/log.tsv','a+') as f:
            f.write(f'{st}\t{modelName}\tInp Size: {len(dic)}\tData: {dataPath}\tSamples: {len(predictions)}\tAcc: {acc}\tPrec: {prec}\tRec: {rec}\n')

    Comm("END")