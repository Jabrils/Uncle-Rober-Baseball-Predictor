import argparse
import train
import predict

# NEED TO SEE HOW WELL THIS THIS WOULD DO WITH A DIFFERENT SEQ PROBLEM,
# LIKE INSTEAD OF 'GF' MAYBE SOMETHING LIKE
# 'GAF' 'GEF' 'GSF' 'GDF' WHERE THE CORRECT ANSWER IS G, ANY ELEMENT, THEN F

parser = argparse.ArgumentParser(
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-mn','--model_name', type=str, default='model',
                    help='the name you want your model to be saved as')
parser.add_argument('-df','--data_file', type=str, default='data/train.txt',
                    help='the name you want your model to be saved as')
parser.add_argument('-e','--epochs',type=int, default=100,
                    help='use -e to set the number of epochs for training')
parser.add_argument('-b','--batches',type=int, default=2048,
                    help='use -e to set the number of epochs for training')
parser.add_argument('-t', "--train", action='store_true',
                    help='add -t if you want to train')
parser.add_argument('-p', "--predict", action='store_true',
                    help='add -p if you want to predict')
parser.add_argument('-lm', "--load_model", action='store_true', default=False,
                    help='add -lm if you want to load the model for further training')
args = parser.parse_args()

# Train
if args.train:
    train.train(args.data_file, args.model_name, args.load_model, args.epochs, args.batches)

# Predict
if args.predict:
    check = args.data_file.split(' ')

    for p in check:
        predict.predict(p, args.model_name)
