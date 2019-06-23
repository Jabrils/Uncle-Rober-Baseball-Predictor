
def HandOff(dataPath, the_file, modelDir, modelName, top):
    import SDEC
    from SDEC import Comm
    import collections

    import numpy as np
    import argparse
    import time
    import datetime
    
    conf = "config/SeqDomain.conf"

    tFile = f'{dataPath}/{the_file}'

    X = []
    Y = []

    mConf = open(f"{modelDir}/{modelName}/conf.mc").read()
    mConf = mConf.split('\n')

    Comm(f"LOADING {tFile}!")

    # Load the data & split it by line breaks
    with open(tFile) as t:
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
    yes = SDEC.CreateCounter(dic)
    # 
    no = SDEC.CreateCounter(dic)
    #
    test = SDEC.GetAllSeqCount(X, dic, settings.resolution, False, False)
    # 
    test = np.array(test)

    # 
    for i in range(len(test)):
        for k in test[i].keys():
            yes[k] += 1 if Y[i] == 1 and test[i][k] > 0 else 0 
            yes[k] -= 1 if Y[i] == 0 and test[i][k] > 0 else 0 

    # for i in range(len(dic)):
    #     for y in yes:
    #         yes[y] -= no[y] if Y[i] == 0 and no[y] > 0 else 0
    
    #         if y == 'gf':
    #             print(y, yes[y], no[y], Y[i]) 

    yes = sorted(yes.items(), key=lambda kv: kv[1], reverse=True)
    # no = sorted(no.items(), key=lambda kv: kv[1], reverse=True)
    print(yes[:top])
    

def HandOffMulti(the_file, modelDir, modelName, top):
    import SDEC
    from SDEC import Comm
    import collections

    import numpy as np
    import argparse
    import time
    import datetime
    import os
    
    conf = "config/SeqDomain.conf"


    mConf = open(f"{modelDir}/{modelName}/conf.mc").read()
    mConf = mConf.split('\n')

    files = os.listdir(the_file)

    confid = [1,1]

    for i in range(len(files)):
        X = []
        Y = []
        theF = files[i]

        Comm(f"LOADING {theF}!")

        # Load the data & split it by line breaks
        print(f'{the_file}/{theF}')
        with open(f'{the_file}/{theF}') as t:
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
        yes = SDEC.CreateCounter(dic)
        # 
        no = SDEC.CreateCounter(dic)
        #
        test = SDEC.GetAllSeqCount(X, dic, settings.resolution, False, False)
        # 
        test = np.array(test)

        # 
        for i in range(len(test)):
            for k in test[i].keys():
                yes[k] += 1 if Y[i] == 1 and test[i][k] > 0 else 0 
                yes[k] -= 1 if Y[i] == 0 and test[i][k] > 0 else 0 

        # for i in range(len(dic)):
        #     for y in yes:
        #         yes[y] -= no[y] if Y[i] == 0 and no[y] > 0 else 0
        
        #         if y == 'gf':
        #             print(y, yes[y], no[y], Y[i]) 

        yes = sorted(yes.items(), key=lambda kv: kv[1], reverse=True)
        # no = sorted(no.items(), key=lambda kv: kv[1], reverse=True)
        print(yes[:top])
        print(yes[0][1], yes[1][1])

        confid[0] += 1 if yes[0][1] > yes[1][1] else 0
        confid[1] += 0 if yes[0][1] > yes[1][1] else 1
    
    print (f'Likelyhood of top guess being best guess: {confid[0]/len(test)}%')