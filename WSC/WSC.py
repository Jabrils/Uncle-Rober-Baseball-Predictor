# Wholistic Sequencing Correlations

def Comm(msg):
    print(f"\n{'~'*20} {msg} {'~'*20}\n")

def CreateSeqDomainDictionary(data):
    '''
    This will scan an entire data file & will document every possible sequence in the file & store it into a dictionary that can then be used as an index for inputs to the NN
    '''

    # ADD RANGE CONSTRAINTS
    # ADD OPTION TO TOGGLE CHARACTERS OR WORDS

    # Import libs
    from collections import OrderedDict

    # Init Vars
    dic = []
    temp = []
    maxSeqLen = 0

    for o in data:
        maxSeqLen = StoreHighestValue(maxSeqLen, len(o))

# BELOW ARE INPUTS
# I NEED TO FIRST GET THE ENTIRE DOMAIN USING ALLCHAR
# THEN I CAN FEED THE FEATURES BELOW INTO THAT DOMAIN SPACE

    # Loop through every line in data file
    for seq in data:

        # Correlation Range
        cRange = [2,len(seq)]

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

                    # Finally append this correlation to our temp list
                    temp.append(cGen)

            # Incriment the current correlation range 
            cCurrent += 1

            print(cGen)

    # Remove the duplicates from our list, but keep the order (important for determinism)
    temp = list(OrderedDict.fromkeys(temp))

    # Create our dictionary
    dic = dict(zip(temp,range(len(temp))))

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

        # loop through the sequence
        for i in range(len(seq)):
            # if we are less than 1 character before the last character (will return error otherwise), then add the character @i & @i+1 concatenated to the temp array
            if i < len(seq)-1:
                temp.append(seq[i] + seq[i+1])

        # Remove the duplicates from our list, but keep the order (important for determinism)
        temp = list(OrderedDict.fromkeys(temp))

        grab = CreateCounter(seqDictionary)

        for t in temp:
            grab[t]+=1

        return list(grab.values())
    except:
        Comm(f"COUNTER FOR {seq} COULD NOT BE CREATED!")
        return None

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

def GetAllSeqCount(dataFile, dic):

    data = []
    counter = CreateCounter(dic)
    
    Comm('CREATING SEQUENCE COUNTER INPUTS!')

    # Load the data & split it by line breaks
    with open(dataFile) as t:
        new = t.read().split('\n')

    # Split the data again but this time by a tab. This will make 0 the sequence & 1 the label
    for i in range(len(new)):
        data.append(GetSeqCount(new[i].split('\t')[0],counter))

    return data

def StoreHighestValue(mod, val):
    if val > mod:
        mod = val

    return mod