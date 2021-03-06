from utils import *

from nltk.corpus import wordnet
from operator import itemgetter
from os import path
from sys import stdout

import argparse
import pickle
import string

import logging
logging.basicConfig(level=logging.INFO, format=log_format)

def get_count(in_tag_set, wn_tag_set):
  tot_line = 0
  user_count = {}
  with open(yfcc_dataset_file) as fin:
    while True:
      line = fin.readline()
      if not line:
        break
      tot_line += 1
      if (tot_line % 20000000) == 0:
        logging.info('#line=%09d' % (tot_line))

      fields = line.strip().split(sep_field)
      assert len(fields) == num_field
      if fields[idx_marker] != '0': # not image
        continue
      if len(fields[idx_tag]) == 0: # no tags
        continue
      is_valid = False
      tags = fields[idx_tag].split(sep_tag)
      for tag in tags:
        if tag in in_tag_set or tag in wn_tag_set:
          is_valid = True
          break
      if not is_valid:
        continue
      user = fields[idx_user]
      user_count[user] = user_count.get(user, 0) + 1

  tot_line = 0
  num_post = 0
  in_tag_count, wn_tag_count = {}, {}
  user_count = {u:c for u,c in user_count.items() if c >= min_user}
  with open(yfcc_dataset_file) as fin:
    while True:
      line = fin.readline()
      if not line:
        break
      tot_line += 1
      if (tot_line % 20000000) == 0:
        logging.info('#line=%09d' % (tot_line))

      fields = line.strip().split(sep_field)
      assert len(fields) == num_field
      if fields[idx_marker] != '0': # not image
        continue
      if len(fields[idx_tag]) == 0: # no tags
        continue
      user = fields[idx_user]
      if user not in user_count:
        continue
      is_valid = False
      tags = fields[idx_tag].split(sep_tag)
      for tag in tags:
        if tag in in_tag_set or tag in wn_tag_set:
          is_valid = True
          break
      if not is_valid:
        continue
      for tag in tags:
        if tag in in_tag_set:
          in_tag_count[tag] = in_tag_count.get(tag, 0) + 1
        if tag in wn_tag_set:
          wn_tag_count[tag] = wn_tag_count.get(tag, 0) + 1
      num_post += 1
  num_in_tag = len(in_tag_count)
  num_wn_tag = len(wn_tag_count)
  num_user = len(user_count)
  logging.info('#imagenet=%d #wordnet=%d' % (num_in_tag, num_wn_tag))
  logging.info('#user=%d #post=%d' % (num_user, num_post))
  return in_tag_count, wn_tag_count, user_count

def main():
  in_tag_set = pickle.load(open(in_all_noun_pfile, 'rb'))
  wn_tag_set = pickle.load(open(wn_all_noun_pfile, 'rb'))

  while True:
    results = get_count(in_tag_set, wn_tag_set)
    in_tag_count, wn_tag_count, user_count = results

    in_tag_set = set([t for t,c in in_tag_count.items() if c >= min_in_tag])
    wn_tag_set = set([t for t,c in wn_tag_count.items() if c >= min_wn_tag])

    if (min(in_tag_count.values()) >= min_in_tag and
        min(wn_tag_count.values()) >= min_wn_tag):
      break
  in_tag_count = {t:c for t,c in in_tag_count.items() if c >= min_in_tag}
  wn_tag_count = {t:c for t,c in wn_tag_count.items() if c >= min_wn_tag}
  pickle.dump(in_tag_count, open(in_initial_noun_pfile, 'wb'))
  pickle.dump(wn_tag_count, open(wn_initial_noun_pfile, 'wb'))
  pickle.dump(user_count, open(initial_user_pfile, 'wb'))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-o', '--override', action='store_true')
  args = parser.parse_args()
  if not path.isfile(initial_user_pfile) or args.override:
    main()
  else:
    logging.info('do not override')


