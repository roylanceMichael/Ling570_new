#!/usr/bin/python

import sys
import re
import os


def tokenize(line):
#  punc = set('1234567890.,!?;:/$#@%^&*()+=-"_`<>][}{|~')   # - abandoned attempt to check the characters against a set

  t = re.sub('(\d)([.,])(\d)', r'\1_\2_\3', line)   # decimals and big numbers
#  print t

  t = re.sub('(\w)(\')([rsv])', r'\1 _\2\3', t)  # 're, 's, 've separated from words
  t = re.sub('(\w)([-&\'])(\w)', r'\1_\2_\3', t)  # hyphenated words, telephone numbers, names with & and other words with apostrophe
#  print t
#  t = re.sub('(\w)(\')(s)', r'\1_\2\3', t)  # hyphenated words, names including & and telephone no
#  print t
  t = re.sub('([.\s][a-z])(\.)', r'\1_\2_', t)  # one letter-abbreviations; a.m. does not work as expected 
#  print t
  t = re.sub('([A-Z][a-z]{0,3})(\.)', r'\1_\2_', t)  # some abbreviations starting with capital letters (U.S., Ph.D.); not longer than four letters
 
  t = re.sub('(\w+)(@)(\w+)(\.)(\w+)', r'\1_\2_\3_\4_\5', t)  # e-mail addresses (niceandsimple@example.com)
#  print t
  t = re.sub('(\w+)(\.)(\w+)(@)(\w+)(\.)(\w+)', r'\1_\2_\3\4\5\6\7', t)  # e-mail addresses (very.common@example.com); would be nice to use + and * on groups
#  print t
  t = re.sub('(\w+)(\.)(\w+)(@)(\w+)(\.)(\w+)(\.)(\w+)', r'\1\2\3\4\5\6\7_\8_\9', t)   # very.common@dept.example.com
  t = re.sub('(\w+)(\.)(\w+)(\.)(\w+)(@)(\w+)(\.)(\w+)(\.)(\w+)', r'\1_\2_\3\4\5\6\7\8\9\10\11', t)   # even.longer.address@example.com
#  print t
#  match = re.search 
 
  t = re.sub('--', '_-__-_', t)   # keep long dashes together
  t = re.sub('([\W^\s])', r' \1 ', t)   # split everything else with whitespace
#  print t
#  just_words = re.sub("''", "", just_words)
#  list_all = just_words.split()

  t = re.sub('\s{2,}', ' ', t)   # get rid of extra spaces
  t = re.sub('(_)*(_ )(\W)( _)', r'\3', t)   # get rid of understrikes

  return t



def main():
#  fn = sys.argv[1]   # source directory

#  list_of_files = []
#  if os.path.exists(fn):
#      list_of_files.append(os.path.join(fn, testfile))   # creating paths to each file in the directory

#  f = open(fn, 'rU')
#  line = f.readline()
#  while line:
#    print tokenize(line)
#    line = f.readline()

 # f.close()

#  for filename in list_of_files:  
#      total += 1

  line = sys.stdin.readline()
  while line:
    print tokenize(line)
    line = sys.stdin.readline()


  
if __name__ == '__main__':
  main()
