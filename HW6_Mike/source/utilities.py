import re

class Utilities:
	def createBigramTuplesFromStr(self, strVal):
		# first, let's split by whitespace
		splitVals = re.split("\s+", strVal)
		posRegex = "/[^/]+$"

		bigramTuples = []

		for i in range(1, len(splitVals)):
			firstMatch = re.search(posRegex, splitVals[i-1])
			secondMatch = re.search(posRegex, splitVals[i])

			if(firstMatch != None and secondMatch != None):
				# get the first and second pos
				firstPos = splitVals[i-1][firstMatch.start()+1:firstMatch.end()]
				secondPos = splitVals[i][secondMatch.start()+1:secondMatch.end()]

				# append the bigram tuple
				bigramTuples.append([ firstPos, secondPos ])

		return bigramTuples