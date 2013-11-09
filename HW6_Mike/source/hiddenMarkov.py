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

	def addParsedLine(self, parsedTuples):
		

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
		self.addToDict(symbol, child, self.emissionDictionary)

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


