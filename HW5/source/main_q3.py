#!/usr/bin/python
import ngrams
import sys

def buildLine(str):
  return "<s> " + str.strip() + " </s>"

def main():
  lm_file = sys.argv[1]
  lm_input = open(lm_file)

  # create NGrams and read into dictionary
  NGramsObj = ngrams.NGrams()

  inputLine = lm_input.readline()
  inputLineIdx = 0
  while inputLine:
    
    if inputLineIdx < 6:
      inputLineIdx = inputLineIdx + 1
      inputLine = lm_input.readline()
      continue

    NGramsObj.read_lm_file_into_dicts(inputLine)
    inputLine = lm_input.readline()

  lm_input.close()

  l1 = float(sys.argv[2])
  l2 = float(sys.argv[3])
  l3 = float(sys.argv[4])

  training_file = sys.argv[5]
  training_input = open(training_file)

  trainingLine = training_input.readline()
  i = 1
  while trainingLine:
    perplexity = NGramsObj.Perplexity(buildLine(trainingLine), l1, l2, l3, i)

  #  print trainingLine + ' : ' + str(perplexity)

    trainingLine = training_input.readline()

    i += 1

  training_input.close()

  print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

  print 'sent_num=' + str(NGramsObj.sentNum) + ' word_num=' + str(NGramsObj.wordNum) + ' oov_num=' + str(NGramsObj.oovNum) 
  print 'lgprob=' + str(NGramsObj.logProbs) + ' ave_lgprob=' + str(NGramsObj.avg_lgprob()) + ' ppl=' + str(NGramsObj.ppl_calc())

if __name__ == '__main__':
  main()
