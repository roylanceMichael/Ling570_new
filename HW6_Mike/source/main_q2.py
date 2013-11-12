#!/usr/bin/python
import hiddenMarkovTrigram
import utilities
import sys

def main():
  utils = utilities.Utilities()

  lambda1 = float(sys.argv[1])
  lambda2 = float(sys.argv[2])
  lambda3 = float(sys.argv[3])

  unknownFileTxt = ''
  unknownFile = sys.argv[4]
  input_t = open(unknownFile)
  t = input_t.readline()
  while t:
    unknownFileTxt = unknownFileTxt + t
    t = input_t.readline()

  unknownTagDict = utils.createUnkProbDict(unknownFileTxt)

  hmm = hiddenMarkovTrigram.HiddenMarkovTrigram(unknownTagDict)

  for line in sys.stdin:
    tr = utils.createTrigramTuplesFromStr(line)
    hmm.addParsedLine(tr)

  print hmm.printHmmFormat(lambda1, lambda2, lambda3)

if __name__ == '__main__':
  main()