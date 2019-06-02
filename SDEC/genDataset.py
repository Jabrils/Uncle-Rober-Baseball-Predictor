import random
import SDEC
import argparse

parser = argparse.ArgumentParser(
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-o','--outname',type=str, default='genData',
                    help='use -a to set the number to ')
parser.add_argument('-e','--encoding',type=str, default='gf',
                    help='use -a to set the number to ')
parser.add_argument('-a','--amt',type=int, default=1000,
                    help='use -a to set the number to ')
args = parser.parse_args()

chars = ['a','s','d','g','f','s','e']
conf = "config/SeqDomain.conf"
dic, settings = SDEC.LoadConf(conf)
distr = {0:0,1:0}
turn = 0
labeler = True

# print(dic)

def genSeq():
    seqG = ''
    for i in range(random.randint(2,11)):
        seqG += chars[random.randint(0,len(chars)-1)]

    return seqG

save = ''

for a in range(args.amt):
    label = turn

    while label == turn:
        t = ''
        t += f'{genSeq()}'
        counter = SDEC.GetSeqCount(t,dic, settings.resolution)
        label =  1 if counter[dic[args.encoding]] > .5 else 0

    turn += 1 if turn == 0 else -1

    distr[label] += 1
    save += f'{t}\t{label}\n' if labeler else f'{t}\n'

    print(a)

with open(f'data/{args.outname}.txt','w') as f:
    f.write(save[:-1])

# print(distr, "DONE!")
print(distr, f'{distr[1]/distr[0]}%', "DONE!")