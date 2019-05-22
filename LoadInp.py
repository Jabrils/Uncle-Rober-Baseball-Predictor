def WES():
    '''
    Wholistic Encompassed Sequencing
    '''
    data = []
    allChar = ""
    dic = []

    # Load the data
    with open("data/train.txt") as t:
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
        print(seq)

        for i in range(len(seq)):
            if i < len(seq)-1:
                temp.append(seq[i] + seq[i+1])

    return set(temp)

def ChrDist():
    data = []
    allChar = ""
    dic = []

    # Load the data
    with open("data/train.txt") as t:
        new = t.read().split('\n')

    # Combine all the characters, & make all the dictionaries
    for i in range(len(new)):
        data.append(new[i].split('\t'))
        allChar += (data[i][0])
        dic.append({x: 0 for x in allChar})

        # Gather the distribution
        for j in data[i][0]:
            dic[i][j] += 1

    return dic