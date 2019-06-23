import argparse
import init
import train
import predict
import handoff

parser = argparse.ArgumentParser(
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-mn','--model_name', type=str, default='model',
                    help='the name you want your model to be saved as')
parser.add_argument('-f','--file', type=str, default='train.txt',
                    help='the name you want your model to be saved as')
parser.add_argument('-md','--models_dir', type=str, default='models',
                    help='the location you want your models to be saved in')
parser.add_argument('-dd','--data_dir', type=str, default='data',
                    help='the location containing your data')
parser.add_argument('-e','--epochs',type=int, default=100,
                    help='use -e to set the number of epochs for training')
parser.add_argument('-sr','--save_rate',type=int, default=100,
                    help='use -sr to set the save rate per x epochs')
parser.add_argument('-T','--top',type=int, default=3,
                    help='use -t to')
parser.add_argument('-b','--batches',type=int, default=2048,
                    help='use -b to set the number to batch for training')
parser.add_argument('-spe','--steps_per_e',type=int, default=0,
                    help='use -spe to set the number of steps per epochs for training')
parser.add_argument('-rlf','--rl_factor',type=float, default=.5,
                    help='use -spe to set the number of steps per epochs for training')
parser.add_argument('-rlp','--rl_patience',type=int, default=105,
                    help='use -spe to set the number of steps per epochs for training')
parser.add_argument('-res','--resolution',type=int, nargs='+', default=[2,3],
                    help='use -res to set the resolution')
parser.add_argument('-t', "--train", action='store_true',
                    help='add -t if you want to train')
parser.add_argument('-ho', "--handoff", action='store_true',
                    help='add -ho if you want to the AI to plot a distr & hand it off to you')
parser.add_argument('-hom', "--handoffmulti", action='store_true',
                    help='add -hom if you want to the AI to plot a distr & hand it off to you')
parser.add_argument('-i', "--init", action='store_true',
                    help='add -i if you want to initilize from some data')
parser.add_argument('-p', "--predict", action='store_true',
                    help='add -p if you want to predict')
parser.add_argument('-lm', "--load_model", action='store_true',
                    help='add -lm if you want to load the model for further training')
args = parser.parse_args()

# Initilize
if args.init:
    init.init(args.file, args.models_dir, args.resolution)
    exit()

# Train
if args.train:
    train.train(args.data_dir, args.file, args.models_dir, args.model_name, args.load_model, args.epochs, args.batches, args.steps_per_e, args.save_rate, args.rl_factor, args.rl_patience)
    exit()

# Predict
if args.predict:
    check = args.file.split(' ')

    for p in check:
        predict.predict(args.data_dir, p, args.models_dir, args.model_name)
    
    exit()

# Handoff
if args.handoff:
    handoff.HandOff(args.data_dir, args.file, args.models_dir, args.model_name, args.top)
    exit()

# Handoff
if args.handoffmulti:
    handoff.HandOffMulti(args.data_file, args.models_dir, args.model_name, args.top)
    exit()

print("PLEASE ADD THE -i, -t, or -p FLAG!")
