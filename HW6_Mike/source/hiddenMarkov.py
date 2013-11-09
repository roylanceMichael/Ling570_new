class HiddenMarkov:
	def __init__(self):
		self.transitionDictionary = {}
		self.emissionDictionary = {}
		self.initDictionary = {}
		self.totalBigramCount = 0

	def state_num(self):
		return len(self.transitionDictionary)

	def sym_num(self):
		return len(self.emissionDictionary)

	def init_line_num(self):
		return len(self.initDictionary)

	def getDictLineCount(self, dictionary):
		totalCount = 0
		for key in dictionary:
			subDict = dictionary[key]

			for subKey in subDict:
				totalCount = totalCount + subDict[subKey]

		return totalCount

	def trans_line_num(self):
		# calculating this the hard way for the time being...
		return self.getDictLineCount(self.transitionDictionary)

	def emiss_line_num(self):
		return self.getDictLineCount(self.emissionDictionary)

	def addParsedLine(self, parsedTuples):
		# given in the format of [ wordTuple, wordTuple ]
		if(len(parsedTuples) > 0):
			initTuple = parsedTuples[0][0]

			if(self.initDictionary.has_key(initTuple.pos)):
				self.initDictionary[initTuple.pos] = self.initDictionary[initTuple.pos] + 1
			else:
				self.initDictionary[initTuple.pos] = 1

			self.addEmission(initTuple.word, initTuple.pos)

			parseTuplesLen = len(parsedTuples)
			for i in range(0, parseTuplesLen):
				# add transitions for both
				firstTuple = parsedTuples[i][0]
				secondTuple = parsedTuples[i][1]

				self.addTransition(firstTuple.pos, secondTuple.pos)

				# only add emissions for first, we'll add in last one at the end...
				self.addEmission(firstTuple.word, firstTuple.pos)

			# account for last tuple...
			lastTuple = parsedTuples[parseTuplesLen - 1][1]
			self.addEmission(lastTuple.word, lastTuple.pos)


	def addToDict(self, parent, child, dictionary):
		if(dictionary.has_key(parent)):
			childDict = dictionary[parent]

			if(childDict.has_key(child)):
				childDict[child] = childDict[child] + 1
			else:
				childDict[child] =  1
		else:
			 dictionary[parent] = { child: 1 }

	def getDicts(self, parent, dictionary):
		if(dictionary.has_key(parent)):
			return dictionary[parent]
		return None

	def getDict(self, parent, child, dictionary):
		dicts = self.getDicts(parent, dictionary)

		if(dicts != None and dicts.has_key(child)):
			return dicts[child]

		return None

	def addEmission(self, symbol, state):
		# we won't count <s> or </s>
		if(symbol.strip() == "<s>" or symbol.strip() == "</s>"):
			return

		self.addToDict(state, symbol, self.emissionDictionary)

	def addTransition(self, to_state, from_state):
		self.addToDict(to_state, from_state, self.transitionDictionary)

	def getEmissions(self, symbol):
		return self.getDicts(symbol, self.emissionDictionary)

	def getEmission(self, symbol, state):
		return self.getDict(symbol, state, self.emissionDictionary)

	def getTransitions(self, to_state):
		return self.getDicts(to_state, self.transitionDictionary)

	def getTransition(self, to_state, from_state):
		return self.getDict(to_state, from_state, self.transitionDictionary)

	def reportLineInfo(self, firstLabel, secondLabel, numerator, denominator):
		# expecting denominator to be a float
		return (firstLabel + '\t' + secondLabel + '\t' + str(numerator / float(denominator))).strip() + '\n'

	def reportDictionaryValues(self, dictionary):
		strBuilder = ''

		for parentKey in dictionary:
			strBuilder = strBuilder + self.reportSubDictionaryValues(parentKey, dictionary[parentKey])

		return strBuilder

	def reportSubDictionaryValues(self, parentKey, subDictionary):
		total = 0

		for subKey in subDictionary:
			total = total + subDictionary[subKey]

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
		strBuilder = strBuilder + self.reportDictionaryValues(self.transitionDictionary)
		strBuilder = strBuilder + '\n'

		# emissions
		strBuilder = strBuilder + '\emissions\n'
		strBuilder = strBuilder + self.reportDictionaryValues(self.emissionDictionary)

		return strBuilder

