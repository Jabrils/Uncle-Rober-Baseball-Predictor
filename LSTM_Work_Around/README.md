# Training a LSTM network and using the model in ml5js

Multi-layer Recurrent Neural Networks (LSTM, RNN) for character-level language models in Python using Tensorflow and modified to work with [tensorflow.js](https://js.tensorflow.org/) and [ml5js](https://ml5js.org/)

Based on [char-rnn-tensorflow](https://github.com/sherjilozair/char-rnn-tensorflow).

[Here](https://www.youtube.com/watch?v=xfuVcfwtEyw) is a video to help you get started with training LSTM with [Spell](https://www.spell.run/)

## Requirements

- Set up a python environment with tensorflow installed. [More detailed instructions here](https://ml5js.org/docs/training-setup.html). You can also follow this [video tutorial about Python virtualenv](https://youtu.be/nnhjvHYRsmM).

- If you are familiar with Docker, you can also use this  ~~[container]()~~ (soon!)

## Usage

### 1) Download this repository

Start by [downloading](https://github.com/ml5js/training-lstm) or cloning this repository:

```bash
git clone https://github.com/ml5js/training-lstm.git
cd training-lstm
```

### 2) Collect data

LSTMs work well when you want predict sequences or patterns from your inputs. Try to gather as much input data as you can. The more the better. 

Once your data is ready, create a new folder in the `root` of this project and inside that folder you should have one file called `input.txt` that contains all your training data.

_(A quick tip to concatenate many small disparate `.txt` files into one large training file: `ls *.txt | xargs -L 1 cat >> input.txt`)_

### 2) Train

Run the training script with the default settings: 

```bash
python train.py --data_dir=./folder_with_my_custom_data
```

Or you can specify the hyperparameters you want depending on the training set, size of your data, etc:

```bash
python train.py --data_dir=./folder_with_my_custom_data --rnn_size 128 --num_layers 2 --seq_length 64 --batch_size 32 --num_epochs 1000 --save_model ./models --save_checkpoints ./checkpoints
```

This will train your model and save a JavaScript version **in a folder called `./models`**, if you don't specify a different path.

You can also run the script called `run.sh`:

```bash
bash run.sh
```

This file contains the same parameters as the one's described before:
```bash
# This are the hyperparameters you can change to fit your data
python train.py --data_dir=./bronte \
--rnn_size 128 \
--num_layers 2 \
--seq_length 50 \
--batch_size 50 \
--num_epochs 50 \
--save_checkpoints ./checkpoints \
--save_model ./models
```

### 3) Use it!

Once the model is ready, you'll just need to point to it in your ml5 sketch:

```javascript
const lstm = new ml5.charRNN('./models/your_new_model');
```

That's it!

## Hyperparameters

Given the size of the training dataset, here are some hyperparameters that might work:

* 2 MB: 
   - rnn_size 256 (or 128) 
   - layers 2 
   - seq_length 64 
   - batch_size 32 
   - dropout 0.25
* 5-8 MB: 
  - rnn_size 512 
  - layers 2 (or 3) 
  - seq_length 128 
  - batch_size 64 
  - dropout 0.25
* 10-20 MB: 
  - rnn_size 1024 
  - layers 2 (or 3) 
  - seq_length 128 (or 256) 
  - batch_size 128 
  - dropout 0.25
* 25+ MB: 
  - rnn_size 2048 
  - layers 2 (or 3) 
  - seq_length 256 (or 128) 
  - batch_size 128 
  - dropout 0.25
