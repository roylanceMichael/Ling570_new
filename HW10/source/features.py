import sys
import utilities


### Here we can flesh out the features, if it hasn't been done in other places already
### This is what I thought the vector may look like:
### word	F1(word frequency) F2(prevalentL=, prevalentR=), F3(unique=left/right), F4(markedWord=left/right), F5(pref=), F6(prev2W=)


class Features:
	def __init__(self, utils):
		self.utils = utils

	def findPrevalence(self, curW):
		if(curW in self.utils.leftDifference):
			leftFrequency = self.utils.leftDifference[curW]
			rightFrequency = self.utils.rightDifference[curW]

			normalizedRightFrequency = float(rightFrequency) / self.utils.k

			leftPrevalence = leftFrequency / (leftFrequency + normalizedRightFrequency)
			rightPrevalence = normalizedRightFrequency / (leftFrequency + normalizedRightFrequency)

			return (leftPrevalence, rightPrevalence)

		return None

	def checkIfUnique(self, curW):
	### used in F3; requires filled uniqueLeft and uniqueRight
		if curW in self.utils.uniqueLeft:
			unique = 'left'
		elif curW in self.utils.uniqueRight:
			unique = 'right'
		else: 
			unique = 'not'   # not sure if this should be output at all; maybe ignore alltogether?
		return unique
