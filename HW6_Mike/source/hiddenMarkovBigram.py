import math
import hiddenMarkov

class HiddenMarkovBigram(hiddenMarkov.HiddenMarkov):
	def __init__(self):
		hiddenMarkov.HiddenMarkov.__init__(self)
		self.bigramTransitionDictionary = {}

	def state_num(self):
		return len(self.bigramTransitionDictionary)

	def trans_line_num(self):
		# calculating this the hard way for the time being...
		return self.getDictLineCount(self.bigramTransitionDictionary)

	def getBigramProb(self, from_state, to_state):
		return self.getTransitionProbability(from_state, to_state)

	def addParsedLine(self, parsedTuples):
		# given in the format of [ wordTuple, wordTuple ]
		if(len(parsedTuples) > 0):
			initTuple = parsedTuples[0][0]

			if(self.initDictionary.has_key(initTuple.pos)):
				self.initDictionary[initTuple.pos] = self.initDictionary[initTuple.pos] + 1
			else:
				self.initDictionary[initTuple.pos] = 1

			self.addEmission(initTuple.word, initTuple.pos)

			# not including EOS here for now...
			parseTuplesLen = len(parsedTuples) - 1
			
			for i in range(0, parseTuplesLen):
				# add transitions for both
				firstTuple = parsedTuples[i][0]
				secondTuple = parsedTuples[i][1]

				self.addTransition(secondTuple.pos, firstTuple.pos)

				# only add emissions for first, we'll add in last one at the end...
				self.addEmission(firstTuple.word, firstTuple.pos)

			# account for last tuple...
			lastTuple = parsedTuples[parseTuplesLen - 1][1]
			self.addEmission(lastTuple.word, lastTuple.pos)


	def addTransition(self, to_state, from_state):
		self.addToDict(from_state, to_state, self.bigramTransitionDictionary)

	def getEmissionTotal(self, symbol):
		symbolDict = self.getDicts(symbol, self.emissionDictionary)

		return self.getDictTotal(symbolDict)

	def getEmissionProbability(self, state, symbol):
		state_dict = self.getDicts(state, self.emissionDictionary)
		state_total = self.getDictTotal(state_dict)
		symbol_total = state_dict[symbol]

		return float(symbol_total) / state_total

	def getTransitions(self, from_state):
		return self.getDicts(from_state, self.bigramTransitionDictionary)

	def getTransition(self, from_state, to_state):
		return self.getDict(from_state, to_state, self.bigramTransitionDictionary)

	def getTransitionTotal(self, from_state):
		from_dict = self.getDicts(from_state, self.bigramTransitionDictionary)

		return self.getDictTotal(from_dict)

	def getTransitionProbability(self, from_state, to_state):
		from_dict = self.getDicts(from_state, self.bigramTransitionDictionary)
		from_total = self.getDictTotal(from_dict)
		to_total = from_dict[to_state]

		return float(to_total) / from_total

	def reportLineInfo(self, firstLabel, secondLabel, numerator, denominator):
		# expecting denominator to be a float
		prob = numerator / float(denominator)
		return (firstLabel + '\t' + secondLabel + '\t' + str(prob) + '\t' + str(math.log10(prob))).strip() + '\n'

	def reportDictionaryValues(self, dictionary):
		strBuilder = ''

		for parentKey in dictionary:
			strBuilder = strBuilder + self.reportSubDictionaryValues(parentKey, dictionary[parentKey])

		return strBuilder

	def reportSubDictionaryValues(self, parentKey, subDictionary):
		total = self.getDictTotal(subDictionary)

		strBuilder = ''
		for subKey in subDictionary:
			strBuilder = strBuilder + self.reportLineInfo(parentKey, subKey, subDictionary[subKey], total)

		return strBuilder

	def printHmmFormat(self):
		strBuilder = ''

		strBuilder = strBuilder + 'state_num=' + str(self.state_num()) + '\n'
		strBuilder = strBuilder + 'sym_num=' + str(self.sym_num()) + '\n'
		strBuilder = strBuilder + 'init_line_num=' + str(self.init_line_num()) + '\n'
		strBuilder = strBuilder + 'trans_line_num=' + str(self.trans_line_num()) + '\n'
		strBuilder = strBuilder + 'emiss_line_num=' + str(self.emiss_line_num()) + '\n'

		# init
		strBuilder = strBuilder + '\init\n'

		# init is different, so we'll just do here
		strBuilder = strBuilder + self.reportSubDictionaryValues('', self.initDictionary)
		strBuilder = strBuilder + '\n'

		# transition
		strBuilder = strBuilder + '\\transition\n'
		strBuilder = strBuilder + self.reportDictionaryValues(self.bigramTransitionDictionary)
		strBuilder = strBuilder + '\n'

		# emissions
		strBuilder = strBuilder + '\emissions\n'
		strBuilder = strBuilder + self.reportDictionaryValues(self.emissionDictionary)

		return strBuilder

