from __future__ import division
import re
import wordTuple


class Utilities:
	def __init__(self):
		self.POS_Word_Count_Dict = {}
		self.POS_POS_Count_Dict = {}
		self.posRegex = "/[^/]+$"

	def BOS_EOS(self, line):
	### might not be needed
	### insert beginning and end of string tags
		line = "<s> " + line.strip() + " </s>" + '\n'
		return line

	def BOS_EOS_pos(self, line):
		return "<s>/BOS " + line + " </s>/EOS" 

	def createUnkProbDict(self, strVal):
		splitLines = strVal.strip().split('\n')

		unkProbDict = { }

		for i in range(0, len(splitLines)):
			splitVals = re.split("\s+", splitLines[i].strip())

			if(len(splitVals) == 2):
				pos = splitVals[0]
				prob = float(splitVals[1])

				unkProbDict[pos] = prob

		return unkProbDict

	def createTrigramTuplesFromStr(self, strVal):
		# let's always append <s>/BOS and </s>/EOS to the end
		newStrVal = self.BOS_EOS_pos(strVal)

		# first, let's split by whitespace
		splitVals = re.split("\s+", newStrVal)
		
		trigramTuples = []

		for i in range(2, len(splitVals)):
			firstMatch = re.search(self.posRegex, splitVals[i-2])
			secondMatch = re.search(self.posRegex, splitVals[i-1])
			thirdMatch = re.search(self.posRegex, splitVals[i])

			if(firstMatch != None and 
				secondMatch != None and
				thirdMatch != None):

				# get the first, second and third tuples
				firstWord = splitVals[i-2][0:firstMatch.start()]
				firstPos = splitVals[i-2][firstMatch.start()+1:firstMatch.end()]
				firstTuple = wordTuple.WordTuple(firstWord, firstPos)

				secondWord = splitVals[i-1][0:secondMatch.start()]
				secondPos = splitVals[i-1][secondMatch.start()+1:secondMatch.end()]
				secondTuple = wordTuple.WordTuple(secondWord, secondPos)

				thirdWord = splitVals[i][0:thirdMatch.start()]
				thirdPos = splitVals[i][thirdMatch.start()+1:thirdMatch.end()]
				thirdTuple = wordTuple.WordTuple(thirdWord, thirdPos)

				trigramTuples.append([ firstTuple, secondTuple, thirdTuple ])

		return trigramTuples

	def createBigramTuplesFromStr(self, strVal):
		# let's always just append <s>\BOS and <\s>\EOS
		newStrVal = self.BOS_EOS_pos(strVal)
		# first, let's split by whitespace
		splitVals = re.split("\s+", newStrVal)

		bigramTuples = []

		for i in range(1, len(splitVals)):
			firstMatch = re.search(self.posRegex, splitVals[i-1])
			secondMatch = re.search(self.posRegex, splitVals[i])

			if(firstMatch != None and secondMatch != None):
				# get the first and second pos
				firstWord = splitVals[i-1][0:firstMatch.start()]
				firstPos = splitVals[i-1][firstMatch.start()+1:firstMatch.end()]
				firstTuple = wordTuple.WordTuple(firstWord, firstPos)

				secondWord = splitVals[i][0:secondMatch.start()]
				secondPos = splitVals[i][secondMatch.start()+1:secondMatch.end()]
				secondTuple = wordTuple.WordTuple(secondWord, secondPos)

				# append the bigram tuple

				bigramTuples.append([ firstTuple, secondTuple ])

		return bigramTuples

	def createEmissionTuplesFromStr(self, strVal):
		# first, let's split by whitespace
		splitVals = re.split("\s+", strVal)
		posRegex = "(.+)/(.+)$"
		
		emissionTuples = []

		for i in splitVals:
#			print i
			match = re.search(posRegex, i)
			if match:
				# append the bigram tuple
				emissionTuples.append([match.group(2), match.group(1)])
		return emissionTuples


	def EmissionDictFromStr(self, emissionTuples, dic):
	### creating a dict of dicts: {POS1 : {word1 : count1, word2 : count2},
	###			       POS2 : {word1 : count1, word2 : count2}}		
#		self.POS_Word_Count_dict = {'BOS':{'<s>':1}, 'EOS':{'</s>':1}}
		dictionary = dic
		for tup in emissionTuples:
#			print tup
#			print tup[0]
			if not tup[0] in dictionary:
				dictionary[tup[0]] = {}
				dictionary[tup[0]][tup[1]] = 1
			else: 
				if tup[1] not in dictionary[tup[0]]:
					dictionary[tup[0]][tup[1]] = 1
				else:
					dictionary[tup[0]][tup[1]] += 1

#		if 'BOS' in dictionary:
#			dictionary['BOS']['<s>'] += 1
#		if 'EOS' in dictionary:
#			dictionary['EOS']['</s>'] += 1
 
		return dictionary
		

	def ProbsFromDict(self, dic):
	### get emission probability out of the dictionary: count/sum(counts) 
		dictionary = dic
		for key in dictionary:
		#	print self.POS_Word_Count_Dict[key]
			s = sum(dictionary[key].values())
			for subkey in dictionary[key]:
		#		print self.POS_Word_Count_Dict[key][subkey]
				print key, '\t', subkey, '\t', float(dictionary[key][subkey]/s)
		return 1
