from sets import Set
import trainvoc
import sys
import re
import utilities

class BuildVectors(trainvoc.TrainVoc):
	def __init__(self):
		trainvoc.TrainVoc.__init__(self)
		self.utils = utilities.Utilities()
		self.rareWords = Set()
		self.nonRareWords = Set()

	def collectRareWords(self, rare_thresh):
		for word in self.frequencyDict:
			if(self.frequencyDict[word] < rare_thresh):
				self.rareWords.add(word)
			else:
				self.nonRareWords.add(word)

	def makeVectors(self, text, rare_thresh):
	### I would like frequencyDict to be inherited globally from trainvoc

		lines = text.split('\n')   # take the text that we read in main and split it into sentences
		numSent = 0   # sentence counter we'll need for the output
		
		for line in lines:   # iterating through sentences
#			print line
			numSent += 1
			numWord = 0   # word counter we'll need for the output
			wordsAndTags = line.split()

#			print wordsAndTags
			for wordAndTag in wordsAndTags:	# iterating through words
				wordPosTuple = self.utils.getWordPosTuple(wordAndTag)

				if wordPosTuple == None:
					print 'Valid word/pos not found in ' + wordAndTag

				word = wordPosTuple[0]

				if word in self.frequencyDict: # theoretically, None should never be in freqDict
#					print str(word) + ':' + str(freqDict[word])
					if int(self.frequencyDict[word]) < int(rare_thresh):
						# rare word
						print word + '- rare word!'

					else:
						# normal word
						print word + '- normal word'

				else:
					print 'Valid word/pos found, but not in freqdict ' + wordAndTag             