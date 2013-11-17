import re
import math

class TransitionHistory:
	def __init__(self):
		self.transitions = []

	def canAddTransition(self, transition):
		# get the last transition and make sure that we can add to our history
		lastTran = self.getLastTransition()

		# if no transitions exist yet, we can add
		if(lastTran == None):
			return True

		# print 'comparing ' + lastTran.printSelf() + ' ' + transition.printSelf()
		if(lastTran.currentPos == transition.previousPos):
			return True

		return False

	def cloneHistoryAndAddTransition(self, transition):
		if(not self.canAddTransition(transition)):
			return None

		newTranHistory = TransitionHistory()

		for i in range(0, len(self.transitions)):
			newTranHistory.addTransition(self.transitions[i])

		newTranHistory.addTransition(transition)

		return newTranHistory

	def representsSentence(self, sentence):
		words = re.split("\s+", sentence.strip())

		if(len(words) != len(self.transitions)):
			return False

		for i in range(0, len(words)):
			if(words[i] != self.transitions[i].symbol):
				return False

		return True

	def getProbability(self):
		prob = 0

		for i in range(0, len(self.transitions)):
			prob = prob + math.log10(self.transitions[i].probability)

		return prob

	def reportTransitions(self):
		strBuilder = ""

		if(len(self.transitions) == 0):
			return strBuilder

		transitionLength = len(self.transitions)

		for i in range(0, transitionLength):
			strBuilder = strBuilder + " " + self.transitions[i].previousPos

		strBuilder = strBuilder + " " + self.transitions[transitionLength - 1].currentPos

		return strBuilder

	def getLastTransition(self):
		tranLen = len(self.transitions)

		if(tranLen > 0):
			return self.transitions[tranLen - 1]

		return None

	def addTransition(self, transition):
		self.transitions.append(transition)

	def printSelf(self):
		strBuilder = ''

		for i in range(0, len(self.transitions)):
			strBuilder = strBuilder + self.transitions[i].printSelf() + "\n"

		return strBuilder


