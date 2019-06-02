import random
import SDEC

chars = ['a','s','d','g','f','s','e']
conf = "config/SeqDomain.conf"
dic, settings = SDEC.LoadConf(conf)
distr = {0:0,1:0}
turn = 0
labeler = True

# print(dic)

def genSeq():
    seqG = ''
    for i in range(random.randint(2,10)):
        seqG += chars[random.randint(0,len(chars)-1)]

    return seqG

save = ''

for a in range(50):
    label = turn

    while label == turn:
        t = ''
        t += f'{genSeq()}'
        counter = SDEC.GetSeqCount(t, dic, settings.resolution)

        label = 0

        for C in chars:
            for c in chars:
                if counter[dic[f'{C}{c}{C}']] > .5:
                    label = 1
                    break

    turn += 1 if turn == 0 else -1

    distr[label] += 1
    save += f'{t}\t{label}\n' if labeler else f'{t}\n'

    print(a)

with open('data/GenDataAD.txt','w') as f:
    f.write(save[:-1])

# print(distr, "DONE!")
print(distr, f'{distr[1]/distr[0]}%', "DONE!")