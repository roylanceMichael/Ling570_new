#!/usr/bin/python

import sys
import re
import os

                                   
def sort_tokens(tokcount_dict):
  tcount = tokcount_dict
  top_sort = sorted(tcount.items(), key = lambda a: -a[1]) # make into tuple and sort
  for tup in top_sort:  # slice of list
    print tup[0], '\t', tup[1]    # print element by element 



def main():
#  fn = sys.argv[1]   # source directory

#  print fn
#  list_of_files = []
#  if os.path.exists(fn):
#   for testfile in os.listdir(fn):

#  f = open(fn, 'rU')
  text = sys.stdin.read()  #f.read()
  tokens = text.split()

  tokcount_dict = {}  # hash table - dictionary
#  total = 0
  for word in tokens:  #clean_words(filename):
    if not word in tokcount_dict:
      tokcount_dict[word] = 1
    else:
      tokcount_dict[word] = tokcount_dict[word] + 1

  sort_tokens(tokcount_dict)


  
if __name__ == '__main__':
  main()
