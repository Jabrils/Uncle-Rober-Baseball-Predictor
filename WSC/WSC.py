# Wholistic Sequencing Correlations

# TO FIX THE ERROR, I HAVE TO MAP EVERY POSSIBLE CORRELATION, NOT JUST WHAT APPEARS IN THE TRAINING DATA! YIKES!

def Comm(msg):
    print(f"\n{'~'*20} {msg} {'~'*20}\n")

def CreateSeqDomainDictionary(data):
    '''
    This will scan an entire data file & will document every possible sequence in the file & store it into a dictionary that can then be used as an index for inputs to the NN
    '''

    # ADD RANGE CONSTRAINTS
    # ADD OPTION TO TOGGLE CHARACTERS OR WORDS
    # ADD A RESOLUTION OPTION

    # Import libs
    from collections import OrderedDict

    # Init Vars
    dic = []
    temp = []
    ret = []
    maxSeqLen = 0
    resolution = 2

    # 
    for o in data:
        maxSeqLen = StoreHighestValue(maxSeqLen, len(o))

    # Loop through every line in data file
    for seq in data:
        for e in seq:
           temp.append(e)

    # Remove the duplicates from our list, but keep the order (important for determinism)
    temp = list(OrderedDict.fromkeys(temp))

    # This will add every element to every element in the domain, creating every possible correlation with a resolution of 2 
    # if resolution == 2:
    for i in temp:
        for j in temp:
            ret.append(i+j)

    # This will add every element to every element in the domain, creating every possible correlation with a resolution of 3
    # if resolution == 3:
    for i in temp:
        for j in temp:
            for k in temp:
                ret.append(i+j+k)

    # Create our dictionary
    dic = dict(zip(ret,range(len(ret))))

    with open("config/SeqDomain.txt", 'w') as f:
        for i in dic:
            f.write(f'{i}:{dic[i]}\n')

    Comm(f'SEQUENCE DOMAIN SAVED IN /CONFIG!')
    return dic

def CreateCounter(dic):
    # Create our counter template
    counter = dict(zip(dic,[0]*len(dic)))

    return counter

def GetSeqCount(seq, seqDictionary):
    '''
    Sequence Domain Dictionary
    '''
    
    # try this, if it returns an exception, we can properly communicate what we think went wrong to the user
    try:
        # Import libs
        from collections import OrderedDict

        # Init Vars
        temp = []
        maxSeqLen = 1

        # Correlation Range
        cRange = [2, len(seq)]

        # Correlation Start
        cCurrent = cRange[0]

        # We need to loop through our sequence as many times as the longest sequence in our data THIS PART COULD BE OPTIMIZED
        for h in range(maxSeqLen):
            # CORRELATIONS: loop through the entire sequence of correlation range length
            for i in range(cRange[1]):
                # Reset our Correlation Generator when we iterate i (move to the next element in the sequence) 
                cGen = ""

                # if we are less than X element before the end of the sequence (will return error otherwise), then add the element i + (i+X) concatenated to the temp array
                if i < cRange[1] - (cCurrent - 1):

                    # Loop through the current Correlation range we are looking at
                    for j in range(cCurrent):
                        # add the current sequence element (indicated as i), & as many elements that are within our current Correlation range (indicated as j)
                        cGen += seq[i + j]
                        # print(seq, cGen)

                    # Finally append this correlation to our temp list
                    temp.append(cGen)

            # Incriment the current correlation range
            cCurrent += 1

        # This will create an empty counter for us to add 
        grab = CreateCounter(seqDictionary)

        # add 1 to every keyword of t in temp
        for t in temp:
            grab[t]+=1

        # 
        for g in grab:
            grab[g] = sigmoid(grab[g])

        return list(grab.values())
    except:
        Comm(f"COUNTER FOR {seq} COULD NOT BE CREATED!")
        return None #[0]*330

def sigmoid(x, derivative=False):
    import numpy as np
    return x*(1-x) if derivative else 1/(1+np.exp(-x))

def LoadSeq(file):
    seq = {}

    try:
        with open(f"{file}") as f:
            for line in f:
                (key, val) = line.split(':')
                seq[key] = int(val)

        Comm(f'SUCCESSFULLY LOADED SEQ CONFIG @ {file}!')

        return seq

    except:
        Comm(f'FILE @ {file} DOES NOT EXIST!')

        return None

def GetAllSeqCount(data, dic):

    ret = []

    counter = CreateCounter(dic)
    
    Comm('CREATING SEQUENCE COUNTER INPUTS!')

    # 
    for d in data:
        ret.append(GetSeqCount(d,counter))

    return ret

def StoreHighestValue(mod, val):
    if val > mod:
        mod = val

    return mod