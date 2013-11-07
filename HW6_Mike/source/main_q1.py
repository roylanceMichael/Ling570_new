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
#    t = utils.BOS_EOS(t)
#    print utils.createBigramTuplesFromStr(t)
    tup = utils.createEmissionTuplesFromStr(t) 
    print tup
    print utils.EmissionDictFromStr(tup)

    t = input_t.readline()
#  print ed

  input_t.close()



if __name__ == '__main__':
  main()

