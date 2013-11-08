class BigramDictionary:
	def __init__(self):
		self.dictionary = { }
		self.totalBigramCount = 0

	def addPos(self, pos, precedingPos):
		if(self.dictionary.has_key(pos)):
			posDict = self.dictionary[pos]

			if(posDict.has_key(precedingPos)):
				posDict[precedingPos] = posDict[precedingPos] + 1
			else:
				posDict[precedingPos] = 1

		else:
			self.dictionary[pos] = { precedingPos: 1 }

	def getPosResults(self, pos):
		if(self.dictionary.has_key(pos)):
			return self.dictionary[pos]
		return None

	def getPosResult(self, pos, precedingPos):
		posDict = self.getPosResults(pos)

		if(posDict != None and posDict.has_key(precedingPos)):
			return posDict[precedingPos]

		return None


