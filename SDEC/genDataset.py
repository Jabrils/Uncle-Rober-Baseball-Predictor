import random
import WSC

chars = ['a','s','d','g','f','s','e']
dic = WSC.LoadSeq("config/SeqDomain.txt")
distr = {0:0,1:0}
turn = 0

def genSeq():
    seqG = ''
    for i in range(random.randint(2,25)):
        seqG += chars[random.randint(0,len(chars)-1)]

    return seqG

save = ''

for a in range(1000):
    label = turn

    while label == turn:
        t = ''
        t += f'{genSeq()}'
        counter = WSC.GetSeqCount(t,dic)
        label =  1 if counter[dic['gf']] > .5 else 0

    turn += 1 if turn == 0 else -1

    distr[label] += 1
    save += f'{t}\t{label}\n'

    print(a)

with open('data/GenData.txt','w') as f:
    f.write(save)

# print(distr, "DONE!")
print(distr, f'{distr[1]/distr[0]}%', "DONE!")