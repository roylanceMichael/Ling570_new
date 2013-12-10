import sys
import utilities


### Here we can flesh out the features, if it hasn't been done in other places already
### This is what I thought the vector may look like:
### word	F1(word frequency) F2(prevalentL=, prevalentR=), F3(unique=left/right), F4(markedWord=left/right), F5(pref=), F6(prev2W=)


class Features:
	def __init__(self, utils):
		self.utils = utils

	def findPrevalence(self, curW):

		# we know that we have 2 directories
		keys = []
		for key in self.utils.labelDifference:
			keys.append(key)

		firstDifference = self.utils.labelDifference[keys[0]]
		secondDifference = self.utils.labelDifference[keys[1]]

		if(curW in firstDifference):
			firstFrequency = firstDifference[curW]
			secondFrequency = secondDifference[curW]

			normalizedSecondFrequency = float(secondFrequency) / self.utils.k

			firstPrevalence = firstFrequency / (firstFrequency + normalizedSecondFrequency)
			secondPrevalence = normalizedSecondFrequency / (firstFrequency + normalizedSecondFrequency)

			return (firstPrevalence, secondPrevalence)

		return None

	def checkIfUnique(self, curW):
	### used in F3; requires filled uniqueLeft and uniqueRight
		keys = []
		for key in self.utils.labelDifference:
			keys.append(key)

		firstUnique = self.utils.labelUniques[keys[0]]
		secondUnique = self.utils.labelUniques[keys[1]]

		if curW in firstUnique:
			unique = 'first'
		elif curW in secondUnique:
			unique = 'second'
		else: 
			unique = 'not'   # not sure if this should be output at all; maybe ignore alltogether?
		return unique


	def checkIfUniqueBigram(self, curW):
	### used in F3; requires filled uniqueLeft and uniqueRight
		keys = []
		for key in self.utils.labelDifference:
			keys.append(key)

		firstUnique = self.utils.labelUniques[keys[0]]
		secondUnique = self.utils.labelUniques[keys[1]]

		if curW in firstUnique:
			uniqueBi = 'first'
		elif curW in secondUnique:
			uniqueBi = 'second'
		else:
			uniqueBi = 'not'   # not sure if this should be output at all; maybe ignore alltogether?

		return uniqueBi

