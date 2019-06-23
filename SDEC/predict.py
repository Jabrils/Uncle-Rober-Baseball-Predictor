
def PredictSingle(X, modelDir, modelName):
    import SDEC
    from SDEC import Comm

    Comm("INIT PREDICTION")

    from keras.models import Sequential
    from keras.layers import Dense
    from keras.models import load_model
    import numpy as np
    import argparse
    import time
    import datetime
    
    conf = "config/SeqDomain.conf"

    mConf = open(f"{modelDir}/{modelName}/conf.mc").read()
    mConf = mConf.split('\n')

    # 
    find = []
    # 
    dic, settings = SDEC.LoadConf(conf)
    #
    test = SDEC.GetAllSeqCount(X, dic, settings.resolution)
    # 
    test = np.array(test)
    #
    mc = SDEC.LoadModelConfig(f"{modelDir}/{modelName}/conf.mc")

    Comm(f"RES: {settings.resolution} ~ INP: {len(test[0])}")

    # 
    model = load_model(f"{modelDir}/{modelName}/{modelName}.h5")

    # calculate predictions
    predictions = model.predict(test)

    msg = "PREDICTIONS"

    Comm(msg)

    # 
    for i in range(len(predictions)):
        guess = int(round(predictions[i][0]))

        print(f'Ind: {i}\tSeq: {X[i]}\tPred: {predictions[i][0]}\tGuess: {guess}') 

    Comm("END")
    return int(round(predictions[0][0]))

def predict(dataPath, the_file, modelDir, modelName):
    import SDEC
    from SDEC import Comm

    Comm("INIT PREDICTION")

    from keras.models import Sequential
    from keras.layers import Dense
    from keras.models import load_model
    import numpy as np
    import argparse
    import time
    import datetime
    
    conf = f"{modelDir}/config/SeqDomain.conf"

    X = []
    Y = []
    hasLabel = False

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    mConf = open(f"{modelDir}/{modelName}/conf.mc").read()
    mConf = mConf.split('\n')

    Comm(f"LOADING {the_file}!")

    # Load the data & split it by line breaks
    with open(f'{the_file}') as t:
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
    dic, settings = SDEC.LoadConf(conf)
    #
    test = SDEC.GetAllSeqCount(X, dic, settings.resolution, True, True)
    # 
    test = np.array(test)
    #
    mc = SDEC.LoadModelConfig(f"{modelDir}/{modelName}/conf.mc")


    Comm(f"RES: {settings.resolution} ~ INP: {len(test[0])}")

    # 
    model = load_model(f"{modelDir}/{modelName}/{modelName}.h5")

    # calculate predictions
    predictions = model.predict(test)

    # 
    totalErr = 0
    wrongCnt = 0

    msg = "WRONG PREDICTIONS" if hasLabel else "PREDICTIONS"

    Comm(msg)

    # 
    for i in range(len(predictions)):
        guess = int(round(predictions[i][0]))

        if hasLabel:
            totalErr += abs(Y[i] - int(round(predictions[i][0])))
            tp += 1 if guess == 1 and Y[i] == 1 else 0
            fp += 1 if guess == 1 and Y[i] == 0 else 0
            fn += 1 if Y[i] == 1 and guess == 0 else 0
            tn += 1 if Y[i] == 0 and guess == 0 else 0

            err = abs(Y[i] - int(round(predictions[i][0])))

            if err == 1 or err == 0:
                print(f'Ind: {i}\tSeq: {X[i]}\tPred: {predictions[i][0]}\tGuess: {guess}\tLabel: {Y[i]}\tError: {err}') 
                wrongCnt += 1
        else:
            print(f'Ind: {i}\tSeq: {X[i]}\tPred: {predictions[i][0]}\tGuess: {guess}') 


    # 
    if hasLabel:
        acc = round((1-(totalErr/len(predictions)))*10000)/100

        tpOtpfp = tp/(tp+fp) if tp+fp != 0 else 0
        prec = round((tpOtpfp)*10000)/100
        rec = round((tp/(tp+fn))*10000)/100
        res = settings.resolution
        ep = mConf[1].split('\t')[1]
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S')

        # 
        if wrongCnt == 0:
            print("N/A")

        Comm(f'{modelName} is {acc}% Accurate')

        Comm(f'Steal Precision: {prec}% ({round(len(X)*prec/100)}/{len(X)})')
        print("Precision;\nWhen a 'steal' was predicted by the algorithm, how many of those predicted 'steals' were actually 'steal' labeled?")
        Comm(f'Steal Recall: {rec}% ({round(len(X)*rec/100)}/{len(X)})')
        print("Recall;\nOut of all the actual 'steals' within the dataset, how many of those were correctly predicted?")

        with open('data/log.tsv','a+') as f:
            f.write(f'{st}\t{modelName}\tInp Size: {len(dic)}\tResolution: {res}\tTotal Epochs: {ep}\tTest Data: {the_file}\tSamples: {len(predictions)}\tAcc: {acc}\tPrec: {prec}\tRec: {rec}\tTrained On: {mc.trainingData}\n')

    Comm("END")