"""
ml5js
A script to dump tensorflow checkpoint variables to tensorflow.js.

This script takes a checkpoint file and writes all of the variables in the
checkpoint to a directory.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import os
import re
import string
import tensorflow as tf

OPTIONS = {
  "output_dir": './models/lstm/',
  "remove_variables_regex": '.*Adam.*|.*beta.*',
}
FILENAME_CHARS = string.ascii_letters + string.digits + '_'

def _var_name_to_filename(var_name):
  chars = []
  for c in var_name:
    if c in FILENAME_CHARS:
      chars.append(c)
    elif c == '/':
      chars.append('_')
  return ''.join(chars)

def dump_checkpoints(checkpoint_path, model_path ,vocab, model_name, final_model):
  print('Converting model to ml5js:', model_name, final_model)
  chk_fpath = os.path.expanduser('./{}/{}/{}'.format(checkpoint_path, model_name, final_model))
  reader = tf.train.NewCheckpointReader(chk_fpath)
  var_to_shape_map = reader.get_variable_to_shape_map()
  output_dir = os.path.expanduser(OPTIONS["output_dir"])
  output_dir = './{}/{}'.format(model_path, model_name)
  tf.gfile.MakeDirs(output_dir)
  manifest = {}
  remove_vars_compiled_re = re.compile(OPTIONS["remove_variables_regex"])

  var_filenames_strs = []
  for name in var_to_shape_map:
    if (OPTIONS["remove_variables_regex"] and
        re.match(remove_vars_compiled_re, name)) or name == 'global_step':
      continue
    var_filename = _var_name_to_filename(name)
    manifest[name] = {'filename': var_filename, 'shape': var_to_shape_map[name]}

    # print('Writing variable ' + name + '...')
    tensor = reader.get_tensor(name)
    with open(os.path.join(output_dir, var_filename), 'wb') as f:
      f.write(tensor.tobytes())

    var_filenames_strs.append("\"" + var_filename + "\"")

  # save the vocab
  vocab_fpath = os.path.join(output_dir, 'vocab.json')
  # print('Writing vocab to ' + vocab_fpath)
  with open(vocab_fpath, 'w') as f:
    f.write(json.dumps(vocab, indent=2, sort_keys=True))

  # save the manifest
  manifest_fpath = os.path.join(output_dir, 'manifest.json')
  # print('Writing manifest to ' + manifest_fpath)
  with open(manifest_fpath, 'w') as f:
    f.write(json.dumps(manifest, indent=2, sort_keys=True))
  print('Done! The output model is in', model_path)
  print('Check https://ml5js.org/docs/training-lstm for more information.')

