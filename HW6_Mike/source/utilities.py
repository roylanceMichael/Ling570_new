from __future__ import division
import re


class Utilities:
	def __init__(self):
		self.POS_Word_Count_Dict = {'BOS':{'<s>':0}, 'EOS':{'</s>':0}}
#                self.POS_Word_Count_dict = { }


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


	def EmissionDictFromStr(self, emissionTuples):
	### creating a dict of dicts: {POS1 : {word1 : count1, word2 : count2},
	###			       POS2 : {word1 : count1, word2 : count2}}		
#		self.POS_Word_Count_dict = {'BOS':{'<s>':1}, 'EOS':{'</s>':1}}

		for tup in emissionTuples:
#			print tup
#			print tup[0]
#			print self.POS_Word_Count_Dict
			if not tup[0] in self.POS_Word_Count_Dict:
				self.POS_Word_Count_Dict[tup[0]] = {}
				self.POS_Word_Count_Dict[tup[0]][tup[1]] = 1
			else: 
				if tup[1] not in self.POS_Word_Count_Dict[tup[0]]:
					self.POS_Word_Count_Dict[tup[0]][tup[1]] = 1
				else:
					self.POS_Word_Count_Dict[tup[0]][tup[1]] += 1

		self.POS_Word_Count_Dict['BOS']['<s>'] += 1
		self.POS_Word_Count_Dict['EOS']['</s>'] += 1
 
		return self.POS_Word_Count_Dict
		

	def ProbsFromDict(self, POS_Word_Count_Dict):
	### get emission probability out of the dictionary: count/sum(counts) 
		for key in self.POS_Word_Count_Dict:
		#	print self.POS_Word_Count_Dict[key]
			s = sum(self.POS_Word_Count_Dict[key].values())
			for subkey in self.POS_Word_Count_Dict[key]:
		#		print self.POS_Word_Count_Dict[key][subkey]
				print key, '\t', subkey, '\t', float(self.POS_Word_Count_Dict[key][subkey]/s)
		return 1
