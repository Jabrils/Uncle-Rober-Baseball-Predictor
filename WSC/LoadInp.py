def GetSeqDomainDictionary(dataFile):
    '''
    This will scan an entire data file & will document every possible sequence in the file & store it into a dictionary that can then be used as an index for inputs to the NN
    '''

    from collections import OrderedDict

    data = []
    allChar = ""
    dic = []

    # Load the data
    with open(dataFile) as t:
        new = t.read().split('\n')

    # Combine all the characters, & make all the dictionaries
    for i in range(len(new)):
        data.append(new[i].split('\t'))
        allChar += (data[i][0])
        #dic.append({x: 0 for x in allChar})
    allChar = set(allChar)

# BELOW ARE INPUTS
# I NEED TO FIRST GET THE ENTIRE DOMAIN USING ALLCHAR
# THEN I CAN FEED THE FEATURES BELOW INTO THAT DOMAIN SPACE
    temp = []
    for d in data:
        seq = d[0]

        for i in range(len(seq)):
            if i < len(seq)-1:
                temp.append(seq[i] + seq[i+1])

    # Remove the duplicates from our index
    temp = list(OrderedDict.fromkeys(temp))

    # Create our dictionary
    dic = dict(zip(temp,range(len(temp))))
    counter = dict(zip(temp,[0]*len(temp)))

    return dic, counter