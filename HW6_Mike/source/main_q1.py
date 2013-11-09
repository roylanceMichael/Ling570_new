#!/usr/bin/python
import hiddenMarkov
import utilities
import sys

### it's not supposed to be a good main yet - I'm just using it for testing methods
def main():
  input_file = sys.argv[1]
  input_t = open(input_file)

  utils = utilities.Utilities()
  t = input_t.readline()

  hmm = hiddenMarkov.HiddenMarkov()

  while t:
    tr = utils.createBigramTuplesFromStr(t)
    hmm.addParsedLine(tr)
    t = input_t.readline()

  input_t.close()

  print hmm.printHmmFormat()

if __name__ == '__main__':
  main()

