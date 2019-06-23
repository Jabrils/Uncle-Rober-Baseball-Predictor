# S-DEC
# Sequence-Domain Encompassed Correlations

# TO FIX THE ERROR, I HAVE TO MAP EVERY POSSIBLE CORRELATION, NOT JUST WHAT APPEARS IN THE TRAINING DATA! YIKES!

def Comm(msg):
    print(f"\n{'~'*20} {msg} {'~'*20}\n")

def CreateSeqDomainDictionary(data, model_dir, resolution):
    '''
    This will scan an entire data file & will document every possible sequence in the file & store it into a dictionary that can then be used as an index for inputs to the NN
    '''

    # ADD OPTION TO TOGGLE CHARACTERS OR WORDS

    # Import libs
    from collections import OrderedDict
    import os

    folder = f"{model_dir}/config"

    if not os.path.exists(model_dir):
        os.mkdir(model_dir)

    if not os.path.exists(folder):
        os.mkdir(folder)

    conf = f"{folder}/SeqDomain.conf"

    # Init Vars
    dic = []
    elements = []
    maxSeqLen = 0

    # Check if resolution only has 1 value, if true then set both min & max to == that value
    resolution = [resolution[0],resolution[0]] if len(resolution) == 1 else resolution

    if resolution[1] > 8:
        Comm("MAX RESOLUTION IS 8!")

    resolution = [resolution[0],8] if resolution[1] > 8 else resolution

    # Then check to see if the min resolution is greater than the max resolution, if so then clip it to == the max 
    resolution[0] = resolution[1] if resolution[0] > resolution[1] else resolution[0]


    # Our current resolution we are looking at == the min resolution
    resLoc = resolution[0]

    # 
    for o in data:
        maxSeqLen = StoreHighestValue(maxSeqLen, len(o))

    # Loop through every line in data file
    for seq in data:
        for e in seq:
           elements.append(e)

    # Remove the duplicates from our list, but keep the order (important for determinism)
    elements = list(OrderedDict.fromkeys(elements))

    # 
    ret = GetResInps(resolution, elements)
    
    # Create our dictionary
    dic = dict(zip(ret,range(len(ret))))

    ret = f'{resolution[0]}\t{resolution[1]}\n'

    # 
    for i in dic:
        ret += f'{i}:{dic[i]}\t'

    # 
    with open(conf, 'w') as f:
        f.write(ret)

    Comm(f'Res: [{resolution[0]},{resolution[1]}] ~ Inps: {len(dic)}')
    Comm(f'SEQUENCE DOMAIN SAVED IN /CONFIG!')
    return dic

def GetResInps(res, el):
    ret = []
    resLoc = res[0]
    ttt = ""
    app = []

    while resLoc <= res[1]:
        # This will add every element to every element in the domain, creating every possible correlation with a resolution of 2 
        if resLoc == 1:
            for i in el:
                ret.append(i)

        # This will add every element to every element in the domain, creating every possible correlation with a resolution of 2 
        if resLoc == 2:
            for i in el:
                for j in el:
                    ret.append(i+j)
            
        # This will add every element to every element in the domain, creating every possible correlation with a resolution of 3
        if resLoc == 3:
            for i in el:
                for j in el:
                    for k in el:
                        ret.append(i+j+k)

        # This will add every element to every element in the domain, creating every possible correlation with a resolution of 3
        if resLoc == 4:
            for i in el:
                for j in el:
                    for k in el:
                        for l in el:
                            ret.append(i+j+k+l)

        # This will add every element to every element in the domain, creating every possible correlation with a resolution of 3
        if resLoc == 5:
            for i in el:
                for j in el:
                    for k in el:
                        for l in el:
                            for o in el:
                                ret.append(i+j+k+l+o)
        
        # This will add every element to every element in the domain, creating every possible correlation with a resolution of 3
        if resLoc == 6:
            for i in el:
                for j in el:
                    for k in el:
                        for l in el:
                            for o in el:
                                for p in el:
                                    ret.append(i+j+k+l+o+p)

        # This will add every element to every element in the domain, creating every possible correlation with a resolution of 3
        if resLoc == 7:
            for i in el:
                for j in el:
                    for k in el:
                        for l in el:
                            for o in el:
                                for p in el:
                                    for q in el:
                                        ret.append(i+j+k+l+o+p+q)

        # This will add every element to every element in the domain, creating every possible correlation with a resolution of 3
        if resLoc == 8:
            for i in el:
                for j in el:
                    for k in el:
                        for l in el:
                            for o in el:
                                for p in el:
                                    for q in el:
                                        for r in el:
                                            ret.append(i+j+k+l+o+p+q+r)

        # Incriment the resolution location we are looking at
        resLoc += 1

    return ret

def CreateCounter(dic):
    # Create our counter template
    counter = dict(zip(dic,[0]*len(dic)))

    return counter

def GetSeqCount(seq, seqDictionary, resolution, squash, bare):
    '''
    Sequence Domain Dictionary
    '''
    
    # try this, if it returns an exception, we can properly communicate what we think went wrong to the user
    try:
        # Import libs
        from collections import OrderedDict

        # Init Vars
        corr = []

        # Correlation Start
        cCurrent = resolution[0]

        # 
        while cCurrent <= resolution[1]:
            # CORRELATIONS: loop through the entire sequence of correlation range length
            for i in range(len(seq)):
                # Reset our Correlation Generator when we iterate i (move to the next element in the sequence) 
                cGen = ""

                # if we are less than X element before the end of the sequence (will return error otherwise), then add the element i + (i+X) concatenated to the elements array
                if i < len(seq) - (cCurrent - 1):

                    # Loop through the current Correlation range we are looking at
                    for j in range(cCurrent):
                        # add the current sequence element (indicated as i), & as many elements that are within our current Correlation range (indicated as j)
                        cGen += seq[i + j]

                    # Finally append this correlation to our elements list
                    corr.append(cGen)

            # Incriment the current correlation range
            cCurrent += 1

        # This will create an empty counter for us to add 
        grab = CreateCounter(seqDictionary)

        # add 1 to every keyword of t in elements
        for t in corr:
            grab[t]+=1

        # We want to squash all values in the counter to be within 0 & 1
        for g in grab:
            grab[g] = sigmoid(grab[g]) if squash else grab[g]

        return list(grab.values()) if bare else grab
    except:
        Comm(f"COUNTER FOR {seq} COULD NOT BE CREATED!")
        return None #[0]*330

def sigmoid(x, derivative=False):
    import numpy as np
    return x*(1-x) if derivative else 1/(1+np.exp(-x))

def LoadConf(file):
    '''
    Loads the configuration file of data domain, returns (dictionary, all settings)
    '''
    seq = {}

    try:
        with open(f"{file}") as f:
            load = f.read().split('\n')

            conf = load[0]
            dic = load[1]

        dic = dic[:-1]
        dic = dic.split('\t')

        for line in dic:
            (key, val) = line.split(':')
            seq[key] = int(val)

        Comm(f'SUCCESSFULLY LOADED SEQ CONFIG @ {file}!')

        return seq, LoadSettings(conf)
    except:
        Comm(f'FILE @ {file} DOES NOT EXIST OR CONFIG FILE IS CORRUPTED!')

        return None

def GetAllSeqCount(data, dic, res, squash, bare):

    ret = []

    counter = CreateCounter(dic)
    
    Comm('CREATING SEQUENCE COUNTER INPUTS!')

    # 
    for d in data:
        ret.append(GetSeqCount(d,counter, res, squash, bare))

    return ret

def StoreHighestValue(mod, val):
    if val > mod:
        mod = val

    return mod

def LoadSettings(sett):
    '''
    This will load the settings from the conf.mc file, but you have to pass in the settings split of the conf.mc file for it to be properly converted!
    '''

    sett = sett.split('\t')

    s = Settings()
    s.resolution = [int(sett[0]),int(sett[1])]

    return s

def LoadModelConfig(mcf):
    mc = ModelConfig()

    with open(mcf, 'r+') as f:
        setts = f.read().split('\n')[1].split('\t')
        mc.inputSize = setts[0]
        mc.totalEpoch = int(setts[1])
        mc.trainingData = setts[2].split(',')

    return mc

def SaveModelConfig(mcf, mc, trainingData, dic, epochs):
    con = "Inp Size\tEpoch\tTraining Data\n"

    # 
    if trainingData not in mc.trainingData:
        mc.trainingData.append(trainingData)

    # Join the Training Data onto 1 string so we can write it to the config file
    td = ','.join(mc.trainingData)

    # 
    con += f'{len(dic)}\t{epochs + mc.totalEpoch}\t{td}'

    # 
    with open(mcf, 'w') as f:
        f.write(con)

class Settings():
    resolution = 0

class ModelConfig():
    inputSize = 0
    totalEpoch = 0
    trainingData = []