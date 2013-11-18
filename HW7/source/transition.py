class Transition:
	def __init__(self, currentPos, previousPos, symbol, probability):
		self.currentPos = currentPos
		self.previousPos = previousPos
		self.symbol = symbol
		self.probability = probability

	def printSelf(self):
		return "toState: " + self.currentPos + " fromState: " + self.previousPos + " symbol: " + self.symbol + " prob: " + str(self.probability)