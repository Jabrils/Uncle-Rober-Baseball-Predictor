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

# chars = ['a','b','c','d','e','f','g','h','i','j','w']
wipe = 'u'

chars = []

for i in range(94):
    chars.append(chr(i+33))

chars.remove(':')

chars = chars[:10]

print(''.join(chars))

conf = f"{args.dir}/config/SeqDomain.conf"
dic, settings = SDEC.LoadConf(conf)
distr = {0:0,1:0,2:0}
turn = 0
labeler = True

# print(dic)

def genSeq():
    seqG = ''
    for i in range(random.randint(args.range[0],args.range[1])):
        seqG += chars[random.randint(0,len(chars)-1)]

    return seqG

save = ''

a = args.amt

while a > 0:
    t = ''
    t += f'{genSeq()}'
    counter = SDEC.GetSeqCount(t, dic, settings.resolution, True, True)

    label = 0

    for c in chars:
        for d in chars:
            s = f"{c}{d}{c}"

            if counter[dic[s]] > .5:
                label = 1
            
                if wipe in t:
                    # label = 0
                    label = 2


    if label == turn:
        turn += 1 if turn < 2 else -2
        # turn += 1 if turn < 1 else -1
    
        a -= 1

        distr[label] += 1
        save += f'{t}\t{label}\n' if labeler else f'{t}\n'

        print(args.amt - a)

with open(f'{args.dir}/{args.outname}.txt','w') as f:
    f.write(save[:-1].replace('2','0'))

# print(distr, "DONE!")
print(distr, f'{distr[1]/(distr[0] + distr[2])}', f"DONE with file {args.dir}/{args.outname}.txt!")