import sys
import utilities


### Here we can flesh out the features, if it hasn't been done in other places already
### This is what I thought the vector may look like:
### word	F1(word frequency) F2(prevalentL=, prevalentR=), F3(unique=left/right), F4(markedWord=left/right), F5(pref=), F6(prev2W=)

class Features:
	def __init__(self, utils):
		self.utils = utils

		keys = []
		for key in self.utils.labelDifference:
			keys.append(key)

		self.firstDifference = self.utils.labelDifference[keys[0]]
		self.secondDifference = self.utils.labelDifference[keys[1]]

		self.firstUnique = self.utils.labelUniques[keys[0]]
		self.secondUnique = self.utils.labelUniques[keys[1]]

		self.firstBiUnique = self.utils.uniqueBiLabelDict[keys[0]]
		self.secondBiUnique = self.utils.uniqueBiLabelDict[keys[1]]

	def findPrevalence(self, curW):
		if(curW in self.firstDifference):
			firstFrequency = self.firstDifference[curW]
			secondFrequency = self.secondDifference[curW]

			normalizedSecondFrequency = float(secondFrequency) / self.utils.k

			firstPrevalence = firstFrequency / (firstFrequency + normalizedSecondFrequency)
			secondPrevalence = normalizedSecondFrequency / (firstFrequency + normalizedSecondFrequency)

			return (firstPrevalence, secondPrevalence)

		return None

	def checkIfUnique(self, curW):
	### used in F3; requires filled uniqueLeft and uniqueRight
		if curW in self.firstUnique:
			unique = 'first'
		elif curW in self.secondUnique:
			unique = 'second'
		else: 
			unique = None
#			unique = 'not'   # not sure if this should be output at all; maybe ignore alltogether?
		return unique


	def checkIfUniqueBigram(self, curW):
	### used in F3; requires filled uniqueLeft and uniqueRight
		if curW in self.firstBiUnique:
			uniqueBi = 'first'
		elif curW in self.secondBiUnique:
			uniqueBi = 'second'
		else:
			uniqueBi = None
#			uniqueBi = 'not'   # not sure if this should be output at all; maybe ignore alltogether?

		return uniqueBi

