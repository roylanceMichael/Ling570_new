#!/usr/bin/python

import sys
import re
import os


def tokenize(line):
#  no_tags = re.sub(r'<[/|\w]*>', "", text)

#  punc = set('1234567890.,!?;:/$#@%^&*()+=-"_`<>][}{|~')   # - abandoned attempt to check the characters against a set
  tk_line = re.sub('([\W^\s])', r' \1 ', line)   # substituting char not mentioned in regex with a space
#  just_words = re.sub("''", "", just_words)
#  just_words = just_words.lower()
#  list_all = just_words.split()

  tk_line = re.sub('\s{2,}', ' ', tk_line)

  return tk_line



def main():
  fn = sys.argv[1]   # source directory

#  print fn
#  list_of_files = []
#  if os.path.exists(fn):
#   for testfile in os.listdir(fn):
#      list_of_files.append(os.path.join(fn, testfile))   # creating paths to each file in the directory

  f = open(fn, 'rU')
  line = f.readline()
  while line:
    print tokenize(line)
    line = f.readline()

  f.close()

#  for filename in list_of_files:  
#    for word in clean_words(filename):
#      total += 1
  
if __name__ == '__main__':
  main()
