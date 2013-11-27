import sys
import re


class TrainVoc:
	def __init__(self):
		self.frequencyDict = {}


	def frequency(self, strVal):
		# first, let's split by whitespace
		splitVals = re.split("\s+", strVal)
		posRegex = "(.+)/(.+)$"
		
		for i in splitVals:
			match = re.search(posRegex, i)
			if match:
				if match.group(1) in self.frequencyDict:
					self.frequencyDict[match.group(1)] += 1
				else:
					self.frequencyDict[match.group(1)] = 1
		return self.frequencyDict


	def sortAndPrint(self, text):
		self.frequency(text)
		strBuilder = ''
#		print self.frequency(text)
		topSort = sorted(self.frequencyDict.items(), key=lambda x: -x[1])
	#	print topSort
		for tup in topSort:
			strBuilder = strBuilder + str(tup[0]) + '\t' + str(tup[1]) + '\n'
		return strBuilder


