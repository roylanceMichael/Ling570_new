#!/usr/bin/python
import hiddenMarkovFactory
import utilities
import sys

def main():
  utils = utilities.Utilities()
  hmm = hiddenMarkovFactory.HiddenMarkovFactory()
  
  hmmInputFile = sys.argv[1]
  input_t = open(hmmInputFile)
  t = input_t.readline()
  while t:
    hmm.readInput(t)
    t = input_t.readline()

  strBuilder = ''
  firstLine = hmm.reportLineNumberDifference().strip()
  secondLine = hmm.reportInitialProbabilities().strip()
  thirdLine = hmm.reportTransProbabilities().strip()
  fourthLine = hmm.reportEmissProbabilities().strip()

  if firstLine != '':
  	print firstLine
  if secondLine != '':
  	print secondLine
  if thirdLine != '':
  	print thirdLine
  if fourthLine != '':
  	print fourthLine

if __name__ == '__main__':
  main()