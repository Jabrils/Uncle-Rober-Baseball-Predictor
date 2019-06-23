import random
import SDEC
import argparse

parser = argparse.ArgumentParser(
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-o','--outname',type=str, default='genData',
                    help='use -a to set the number to ')
parser.add_argument('-e','--encoding',type=str, default='gf',
                    help='use -a to set the number to ')
parser.add_argument('-d','--dir',type=str, default='data',
                    help='use -a to set the number to ')
parser.add_argument('-a','--amt',type=int, default=1000,
                    help='use -a to set the number to ')
parser.add_argument('-r','--range',type=int, nargs='+', default=[2,12],
                    help='use -res to set the resolution')

args = parser.parse_args()

chars = ['a','b','c','d','e','f','g','h','i','j']
conf = "config/SeqDomain.conf"
dic, settings = SDEC.LoadConf(conf)
distr = {0:0,1:0}
turn = 1
labeler = True

# print(dic)

def genSeq():
    seqG = ''
    for i in range(random.randint(args.range[0],args.range[1])):
        seqG += chars[random.randint(0,len(chars)-1)]

    return seqG

save = ''

for a in range(args.amt):
    label = turn

    while label == turn:
        t = ''
        t += f'{genSeq()}'
        counter = SDEC.GetSeqCount(t,dic, settings.resolution, True, True)
        label =  1 if counter[dic[args.encoding]] > .5 else 0

    turn += 1 if turn == 0 else -1

    distr[label] += 1
    save += f'{t}\t{label}\n' if labeler else f'{t}\n'

with open(f'{args.dir}/{args.outname}.txt','w') as f:
    f.write(save[:-1])

# print(distr, "DONE!")
print(distr, f'{distr[1]/distr[0]}%', f"DONE with file {args.dir}/{args.outname}.txt!")