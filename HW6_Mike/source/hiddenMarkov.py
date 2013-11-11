import math

class HiddenMarkov:
	def __init__(self):
		self.symbolCount = {}
		self.emissionDictionary = {}
		self.initDictionary = {}

	def sym_num(self):
		return len(self.symbolCount)

	def init_line_num(self):
		return len(self.initDictionary)

	def getDictTotal(self, dictionary):
		total = 0
		for key in dictionary:
			total = total + dictionary[key]

		return total

	def getDictLineCount(self, dictionary):
		totalCount = 0
		for key in dictionary:
			subDict = dictionary[key]

			for subKey in subDict:
				totalCount = totalCount + subDict[subKey]

		return totalCount

	def emiss_line_num(self):
		return self.getDictLineCount(self.emissionDictionary)

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
		
		if(not self.symbolCount.has_key(symbol)):
			self.symbolCount[symbol] = 1

	def getEmissions(self, symbol):
		return self.getDicts(symbol, self.emissionDictionary)

	def getEmission(self, symbol, state):
		return self.getDict(symbol, state, self.emissionDictionary)