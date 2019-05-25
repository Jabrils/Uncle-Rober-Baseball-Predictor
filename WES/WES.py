def Comm(msg):
    print(f"\n{'~'*20} {msg} {'~'*20}\n")

def CreateSeqDomainDictionary(dataFile):
    '''
    This will scan an entire data file & will document every possible sequence in the file & store it into a dictionary that can then be used as an index for inputs to the NN
    '''

    # ADD RANGE CONSTRAINTS
    # ADD OPTION TO TOGGLE CHARACTERS OR WORDS

    # Import libs
    from collections import OrderedDict

    # Init Vars
    data = []
    dic = []
    temp = []

    Comm('LOADING DATA!')
    # Load the data & split it by line breaks
    with open(dataFile) as t:
        new = t.read().split('\n')

    # Split the data again but this time by a tab. This will make 0 the sequence & 1 the label
    for i in range(len(new)):
        data.append(new[i].split('\t'))

# BELOW ARE INPUTS
# I NEED TO FIRST GET THE ENTIRE DOMAIN USING ALLCHAR
# THEN I CAN FEED THE FEATURES BELOW INTO THAT DOMAIN SPACE

    # Loop through every line in data file
    for seq in data:
        # Set the first sequence to be only the first half of the sequence (removing the label)
        seq = seq[0]

    # TURN THIS WHOLE SECTION INTO A LOOP THAT WILL FIRST GRAB ALL 

        # Correlation Range
        cRange = [2,len(seq)]

        # Correlation Start
        cStart = cRange[0]

        # 1RST CORRELATION: loop through the sequence
        for i in range(cRange[1]):
            gen = ""
            # if we are less than 1 character before the last character (will return error otherwise), then add the character @i & @i+1 concatenated to the temp array
            if i < cRange[1] - (cStart - 1):
                gen += seq[i]
                gen += seq[i+1]
                temp.append(gen)

        # # 2ND CORRELATION: loop through the sequence
        # for i in range(cRange[1]):
        #     # if we are less than 2 characters before the last character (will return error otherwise), then add the character @i & @i+1 & @i+2 concatenated to the temp array
        #     if i < cRange[1]-2:
        #         temp.append(seq[i] + seq[i+1]  + seq[i+2])

        # # 3RD CORRELATION: loop through the sequence
        # for i in range(cRange[1]):
        #     # if we are less than 3 characters before the last character (will return error otherwise), then add the character @i & @i+1 & @i+2 & @i+3 concatenated to the temp array
        #     if i < cRange[1]-3:
        #         temp.append(seq[i] + seq[i+1]  + seq[i+2] + seq[i+3])

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

    try:
        # Import libs
        from collections import OrderedDict

        # Init Vars
        data = []
        dic = []
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

        return grab
    except:
        Comm("DICTIONARIES LIKELY COULD NOT BE LOADED!")
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
    
    Comm('LOADING DATA!')

    # Load the data & split it by line breaks
    with open(dataFile) as t:
        new = t.read().split('\n')

    # Split the data again but this time by a tab. This will make 0 the sequence & 1 the label
    for i in range(len(new)):
        data.append(GetSeqCount(new[i].split('\t')[0],counter))

    return data