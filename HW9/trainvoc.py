import sys
import re


class TrainVoc:
	def frequency(self, strVal):
		# first, let's split by whitespace
		splitVals = re.split("\s+", strVal)
		posRegex = "(.+)/(.+)$"
		frequencyDict = {}
		
		for i in splitVals:
			match = re.search(posRegex, i)
			if match:
				# append the bigram tuple
				if match.group(1) in frequencyDict:
					frequencyDict[match.group(1)] += 1
				else:
					frequencyDict[match.group(1)] = 1
		return frequencyDict


	def sortAndPrint(self, text):
		wordcount = self.frequency(text)
		strBuilder = ''
		topSort = sorted(wordcount.items(), key=lambda x: -x[1])
		for tup in topSort:
			strBuilder = strBuilder + str(tup[0]) + '\t' + str(tup[1]) + '\n'
		return strBuilder


