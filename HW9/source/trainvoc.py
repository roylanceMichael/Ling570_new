import sys
import utilities
import re

class TrainVoc:
	def __init__(self):
		self.frequencyDict = {}
		self.utils = utilities.Utilities()

	def buildFrequency(self, strVal):
		# first, let's split by whitespace
		splitVals = re.split("\s+", strVal)
		
		### fill the dictionary; count the frequencies
		for splitVal in splitVals:
			wordPosTuple = self.utils.getWordPosTuple(splitVal)
			if wordPosTuple != None: # do we have a match?
				word = wordPosTuple[0] # get the word 
				if word in self.frequencyDict:
					self.frequencyDict[word] += 1
				else:
					self.frequencyDict[word] = 1

	def sortAndPrint(self, text):
	### turn dict in a list and sort it in descending order
		self.buildFrequency(text)
		strBuilder = ''

		topSort = sorted(self.frequencyDict.items(), key=lambda x: -x[1])

		for tup in topSort:
			strBuilder = strBuilder + str(tup[0]) + '\t' + str(tup[1]) + '\n'
		
		return strBuilder


