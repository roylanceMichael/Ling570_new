#!/usr/bin/python

import ngrams
import sys


def main():
  input_file = sys.argv[1]
  input_t = open(input_file)
  t = input_t.read()
  
  NGramsObj = ngrams.NGrams()

  for tup in NGramsObj.count_unigrams(t):  # slice of list
    print tup[1], '\t', tup[0]    # print element by element 

  for tup in NGramsObj.count_bigrams(t):  # slice of list
    print tup[1], '\t', tup[0]    # print element by element 

  for tup in NGramsObj.count_trigrams(t):  # slice of list
    print tup[1], '\t', tup[0]    # print element by element


  input_t.close()



if __name__ == '__main__':
  main()
