#!/usr/bin/python

import utilities
import sys

### it's not supposed to be a good main yet - I'm just using it for testing methods


def main():
  input_file = sys.argv[1]
  input_t = open(input_file)

  utils = utilities.Utilities()
  t = input_t.readline()
#  print t
  while t:
    tr = utils.createBigramTuplesFromStr(t)
#    print tr
    em = utils.createEmissionTuplesFromStr(t) 
    trn = utils.EmissionDictFromStr(tr, utils.POS_POS_Count_Dict)
#    print trn
    e = utils.EmissionDictFromStr(em, utils.POS_Word_Count_Dict)
#    print e

    t = input_t.readline()

  print 'state_num=' + str(len(utils.POS_POS_Count_Dict))

  Sum = 0
  for key in utils.POS_Word_Count_Dict:
    Sum = Sum + len(utils.POS_Word_Count_Dict[key])
  print 'sym_num=' + str(Sum)

  print 'init_line_num='
  print 'trans_line_num='
  print 'emiss_line_num=' + '\n'
  print '\\init'
  print 'BOS' + '\t' + '1.0' + '\n'
  print '\n \n'
  print '\\transition'
  utils.ProbsFromDict(utils.POS_POS_Count_Dict)   # counts emission probabilities from the dictionary of dictionaries for POS-tags
  print '\n'
  print '\\emission'
  utils.ProbsFromDict(utils.POS_Word_Count_Dict)   # counts emission probabilities from the dictionary of dictionaries for POS-tags and words

  input_t.close()



if __name__ == '__main__':
  main()

