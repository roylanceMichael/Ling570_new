import re
import math

class TransitionHistory:
	def __init__(self):
		self.transitions = []
		self.lastTransitionCurrentPos = ""

	def canAddTransition(self, transition):
		# if no transitions exist yet, we can add
		if(self.lastTransitionCurrentPos == ""):
			return True

		# print 'comparing ' + lastTran.printSelf() + ' ' + transition.printSelf()
		if(self.lastTransitionCurrentPos == transition.previousPos):
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
		self.lastTransitionCurrentPos = transition.currentPos

	def printSelf(self):
		strBuilder = ''

		for i in range(0, len(self.transitions)):
			strBuilder = strBuilder + self.transitions[i].printSelf() + "\n"

		return strBuilder


