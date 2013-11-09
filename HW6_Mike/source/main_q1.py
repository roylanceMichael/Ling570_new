#!/usr/bin/python
import hiddenMarkovBigram
import utilities
import sys

def main():
  input_file = sys.argv[1]
  input_t = open(input_file)

  utils = utilities.Utilities()
  t = input_t.readline()

  hmm = hiddenMarkovBigram.HiddenMarkovBigram()

  while t:
    tr = utils.createBigramTuplesFromStr(t)
    hmm.addParsedLine(tr)
    t = input_t.readline()

  input_t.close()

  print hmm.printHmmFormat()

if __name__ == '__main__':
  main()

