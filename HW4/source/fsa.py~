import re
import utilities

class Fsa:
	def __init__(self):
		self.endState = ""
		self.epsilonState = "*e*"
		self.transitionStates = []
		self.utilities = utilities.Utilities()

	def parse(self, strVal):
		splitStrVal = re.split("\n", strVal)

		# leave if nothing given
		if(len(splitStrVal) == 0):
			return

		# always given a value at the beginning
		self.endState = splitStrVal[0].strip()

		# cycle through the rest and add
		for i in range(1, len(splitStrVal)):
			line = splitStrVal[i].strip()

			# leave if nothing given
			if(line == ''):
				continue

			tranState = self.utilities.createTransitionState(line)

			self.transitionStates.append(tranState)

	def getPreviousTransitions(self, currentState):
		currentStates = []

		for i in range(0, len(self.transitionStates)):
			if(self.transitionStates[i].toState == currentState):
				currentStates.append(self.transitionStates[i])

		return currentStates

	def processInput(self, userInput):
		# assuming the input is just in one line, the main file will split it for me...
		# this function will simply return a yes or no
		splitValues = re.split("\s+", userInput)

		# working our way back

		# stack structure
		workSpace = []

		# get final transitions
		finalStates = self.getPreviousTransitions(self.endState)

		# add in all the work objects
		for i in range(0, len(finalStates)):
			workObject = { "wordIdx": len(splitValues) - 1, "state": finalStates[i] }
			workSpace.append(workObject)

		while(len(workSpace) > 0):
			workObject = workSpace.pop(0)

			wordIdx = workObject["wordIdx"]
			isBeginningWord = wordIdx == 0
			word = self.utilities.cleanseInput(splitValues[wordIdx])

			state = workObject["state"]

			# does this transition to the previous state?
			if(state.value == word):
				if(isBeginningWord and self.finalInputOkay(state.fromState)):
					return True
				else:
					previousWordIdx = wordIdx - 1
					previousStates = self.getPreviousTransitions(state.fromState)

					for i in range(0, len(previousStates)):
						newWorkObject = { "wordIdx": previousWordIdx, "state": previousStates[i] }
						workSpace.append(newWorkObject)

			elif(state.value == self.epsilonState):
				if(isBeginningWord and self.finalInputOkay(state.fromState)):
					return True
				else:
					previousStates = self.getPreviousTransitions(state.fromState)

					for i in range(0, len(previousStates)):
						newWorkObject = { "wordIdx": wordIdx, "state": previousStates[i] }
						workSpace.append(newWorkObject)


		return False

	# (should be) private helper functions
	def finalInputOkay(self, currentState):
		finalStates = self.getPreviousTransitions(currentState)

		if(len(finalStates) == 0):
			return True

		# among my final states, are any not recursive? 
		# This means we aren't at the end
		for i in range(0, len(finalStates)):
			finalState = finalStates[i]
			if(finalState.toState != finalState.fromState):
				return False

		return True
