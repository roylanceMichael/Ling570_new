#!/usr/bin/python

import ngrams
import sys


def main():
  input_file = sys.argv[1]
  input_t = open(input_file)
  t = input_t.read()
  
  NGramsObj = ngrams.NGrams()

  for tup in NGramsObj.count_unigrams(t):  # unigrams
    print tup[1], '\t', tup[0]    # print count and 1-gram 

  for tup in NGramsObj.count_bigrams(t):  # bigrams
    print tup[1], '\t', tup[0]    # print count and 2-gram 

  for tup in NGramsObj.count_trigrams(t):  # trigrams
    print tup[1], '\t', tup[0]    # print count and 3-gram

  

  input_t.close()



if __name__ == '__main__':
  main()
