from __future__ import division
import re


class Utilities:
	def __init__(self):
		self.POS_Word_Count_Dict = {}  #'BOS':{'<s>':0}, 'EOS':{'</s>':0}}
                self.POS_POS_Count_Dict = {}


	def BOS_EOS(self, line):
	### might not be needed
	### insert beginning and end of string tags
		line = "<s> " + line.strip() + " </s>" + '\n'
		return line


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

		# bigramTuples.insert(0, ['BOS', bigramTuples[0][0]])

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
