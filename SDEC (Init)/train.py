
# <.001 = converged (likely)
# 1000 epochs 100 batches should be good enough

def train(dataPath, the_file, modelsDir, modelName, loadModel, epochs, batches, spe, saveRate, rlFactor, rlPatience):
    import SDEC
    from SDEC import Comm

    Comm("INIT TRAINING")

    import keras.backend as K
    from keras import optimizers
    from keras.models import Sequential
    from keras.models import load_model
    from keras.layers import Input, Dense
    from keras.models import Model
    from keras.callbacks import TensorBoard, ReduceLROnPlateau, ModelCheckpoint, LambdaCallback, LearningRateScheduler, Callback
    import os
    import numpy as np
    import argparse
    import datetime
    import time
    
    class DynamicLR(Callback):
        def __init__(self, model_name, *args, **kwargs):
            self.model_checkpoint_paths = []
            self.model_name = model_name
            super().__init__(*args, **kwargs)

        def on_epoch_end(self, epoch, logs):
            # I suppose here it's a Functional model
            print(K.eval(self.model.optimizer.lr))

    conf = f"{modelsDir}/config/SeqDomain.conf"

    X = []
    Y = []

    # Load the data & split it by line breaks
    with open(f'{the_file}') as t:
        new = t.read().split('\n')

    # Split the data again but this time by a tab. This will make 0 the sequence & 1 the label
    for i in range(len(new)-1):
        grab = new[i].split('\t')
        X.append(grab[0])
        Y.append(int(grab[1]))

    # 
    dic, settings = SDEC.LoadConf(conf)
    # 
    test = SDEC.GetAllSeqCount(X, dic, settings.resolution, True, True)
    # 
    test = np.array(test)

    Comm(f"RES: {settings.resolution} ~ INP: {len(test[0])}")

    inp = Input(shape=(len(test[0]),))

    #  Neural Network Architecture
    hidden = Dense(units=len(test[0]), activation='relu')(inp)
    hidden = Dense(units=64, activation='relu')(hidden)
    out = Dense(units=1, activation='sigmoid')(hidden)
    
    model = Model(inp, out)

    # HERE LOAD WEIGHTS
    if loadModel:
        try:
            Comm("LOADING MODEL!")
            model.load_weights(f"{modelsDir}/{modelName}/{modelName}.h5")
        except:
            Comm(f"THERE IS NO MODEL {modelsDir}/{modelName}/{modelName}.h5")
            cont = input("Want to create the model here? (y or n): ")
            loadModel = False

            if cont.lower() != 'y':
                Comm("EXITING!")
                return

    sdg = optimizers.SGD(lr=.1)
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer=sdg, metrics=['accuracy'])

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')

    # For tensor board
    tb = TensorBoard(log_dir=f'{modelsDir}/Graphs/{modelsDir}_{modelName}_{timestamp}', histogram_freq=0,  
            write_graph=True, write_images=True)

    reduceLR = ReduceLROnPlateau(monitor='loss', verbose=1, min_delta=.01, factor=rlFactor, patience=rlPatience, min_lr=.002)

    mc = ModelCheckpoint(f'{modelsDir}/{modelName}/{modelName}.h5', period=saveRate, save_best_only=True, mode='max', monitor='val_acc')

    cbp = DynamicLR(modelName)

    # 
    if not os.path.isdir(f'{modelsDir}'):
        os.mkdir(f'{modelsDir}')
    
    # 
    if not os.path.isdir(f'{modelsDir}/{modelName}'):
        os.mkdir(f'{modelsDir}/{modelName}')

    # Fit the model
    if spe > 0:
        model.fit(test, Y, epochs=epochs, steps_per_epoch=spe, shuffle=True, callbacks=[tb,mc, reduceLR, cbp], validation_data=[test,Y], validation_steps=1)#, validation_split=.2, validation_steps=1)
    else:
        model.fit(test, Y, epochs=epochs, batch_size=batches, shuffle=True, callbacks=[tb,mc, reduceLR, cbp])#, validation_split=.2, validation_steps=1)

    # evaluate the model
    scores = model.evaluate(test, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


    # save the model
    model.save(f"{modelsDir}/{modelName}/{modelName}_full.h5")

    # Create a new Model Config Class
    mc = SDEC.ModelConfig()

    # We will load our model config if the loadModel flag has been set, then well update the epochs & training data
    if loadModel:
        mc = SDEC.LoadModelConfig(f"{modelsDir}/{modelName}/conf.mc")

    SDEC.SaveModelConfig(f"{modelsDir}/{modelName}/conf.mc", mc, the_file, dic, epochs)

    Comm("Saved Model!")