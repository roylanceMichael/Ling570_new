import trainvoc
import sys
import re


class BuildVectors(trainvoc.TrainVoc):
	def __init__(self):
		trainvoc.TrainVoc.__init__(self)


	def makeVectors(self, text, rare_thresh, freqDict):
		lines = text.split('\n')   # take the text that we read in main and split it into sentences
		numSent = 0   # sentence counter we'll need for the output
#		print freqDict
		
		for line in lines:   # iterating through sentences
#			print line
			numSent += 1
			numWord = 0   # word counter we'll need for the output
			wordsAndTags = line.split()
#			print wordsAndTags
			for wordAndTag in wordsAndTags:	# iterating through words
				word = self.separateWordFromTag(wordAndTag)
				print rare_thresh
				if word in freqDict:
					print str(word) + ':' + str(freqDict[word])
					if int(freqDict[word]) < int(rare_thresh):
						# rare word
						print word + '- rare word!'


					else:
						# normal word
						print word + '- normal word'


				else:
					print 'Not in dictionary - what do we do now?'



	def separateWordFromTag(self, wordAndTag):
		match = re.search("(.+)/(.+)$", wordAndTag)
                if match:
			return match.group(1)
		else:
			print 'no word here'                



        

