#!/usr/bin/python

import ngrams
import sys


def main():
  input_file = sys.argv[1]
  input_t = open(input_file)
  
  NGramsObj = ngrams.NGrams()
  
  t = input_t.readline()
  while t:
    NGramsObj.read_into_dicts(t)
    t = input_t.readline()


  print "\data\\"  
  print "ngram 1: type=" + str(NGramsObj.count_types_tokens(NGramsObj.uni_dict)[0]) + " token=" + str(NGramsObj.count_types_tokens(NGramsObj.uni_dict)[1])
  print "ngram 2: type=" + str(NGramsObj.count_types_tokens(NGramsObj.bi_dict)[0]) + " token=" + str(NGramsObj.count_types_tokens(NGramsObj.bi_dict)[1])
  print "ngram 3: type=" + str(NGramsObj.count_types_tokens(NGramsObj.tri_dict)[0]) + " token=" + str(NGramsObj.count_types_tokens(NGramsObj.tri_dict)[1])
 
  print '\n', "\\1-grams:"
  for tup in NGramsObj.calc_uni_prob():  
    print tup[0], tup[1], tup[2], tup[3]     

  print '\n', "\\2-grams:"
  for tup in NGramsObj.calc_bi_prob():  
    print tup[0], tup[1], tup[2], tup[3]     

  print '\n', "\\3-grams:"
  for tup in NGramsObj.calc_tri_prob(): 
    print tup[0], tup[1], tup[2], tup[3]     



  input_t.close()



if __name__ == '__main__':
  main()

