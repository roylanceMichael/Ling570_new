import sys
import re


class TrainVoc:
	def __init__(self):
		self.frequencyDict = {}
		self.posRegex = "/[^/]+$"

	def frequency(self, strVal):
		# first, let's split by whitespace
		splitVals = re.split("\s+", strVal)
		
		### fill the dictionary; count the frequencies
		for splitVal in splitVals:
			match = re.search(self.posRegex, splitVal)
			if match: # do we have a match?
				word = splitVal[0:match.start()] # get the word from beginning to start
				if word in self.frequencyDict:
					self.frequencyDict[word] += 1
				else:
					self.frequencyDict[word] = 1
		
		return self.frequencyDict

	def sortAndPrint(self, text):
	### turn dict in a list and sort it in descending order
		self.frequency(text)
		strBuilder = ''
#		print self.frequency(text)
		topSort = sorted(self.frequencyDict.items(), key=lambda x: -x[1])
	#	print topSort
		for tup in topSort:
			strBuilder = strBuilder + str(tup[0]) + '\t' + str(tup[1]) + '\n'
		return strBuilder


