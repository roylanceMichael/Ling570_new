#!/usr/bin/python
import hiddenMarkovBigram
import utilities
import sys

def main():
  utils = utilities.Utilities()
  hmm = hiddenMarkovBigram.HiddenMarkovBigram()

  for line in sys.stdin:
    tr = utils.createBigramTuplesFromStr(line)
    hmm.addParsedLine(tr)

  print hmm.printHmmFormat()

if __name__ == '__main__':
  main()

