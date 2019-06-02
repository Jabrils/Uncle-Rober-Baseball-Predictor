# <.001 = converged (likely)
# 1000 epochs 100 batches should be good enough
def train(dataPath, modelsDir, modelName, loadModel, epochs, batches, spe):
    import SDEC
    from SDEC import Comm

    Comm("INIT TRAINING")

    from keras.models import Sequential
    from keras.models import load_model
    from keras.layers import Input, Dense
    from keras.models import Model
    import os
    import numpy as np
    import argparse
    
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

    # 
    dic, settings = SDEC.LoadConf(conf)
    # 
    test = SDEC.GetAllSeqCount(X, dic, settings.resolution)
    # 
    test = np.array(test)

    Comm(f"RES: {settings.resolution} ~ INP: {len(test[0])}")

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
        try:
            model.load_weights(f"{modelsDir}/{modelName}/{modelName}.h5")
        except:
            Comm(f"THERE IS NO MODEL {modelsDir}/{modelName}/{modelName}.h5")
            cont = input("Want to create the model here? (y or n): ")
            loadModel = False

            if cont.lower() != 'y':
                Comm("EXITING!")
                return

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    if spe > 0:
        model.fit(test, Y, epochs=epochs, steps_per_epoch=spe, shuffle=True)
    else:
        model.fit(test, Y, epochs=epochs, batch_size=batches, shuffle=True)

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

    # Create a new Model Config Class
    mc = SDEC.ModelConfig()

    # We will load our model config if the loadModel flag has been set, then well update the epochs & training data
    if loadModel:
        mc = SDEC.LoadModelConfig(f"{modelsDir}/{modelName}/conf.mc")

    SDEC.SaveModelConfig(f"{modelsDir}/{modelName}/conf.mc", mc, dataPath, dic, epochs)

    Comm("Saved Model!")