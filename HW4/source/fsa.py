from decimal import *
import re
import utilities
import transitionState
import wordTransitions

class Fsa:
	def __init__(self):
		self.endState = ""
		self.startState = ""
		self.epsilonState = "*e*"
		self.transitionStates = []
		self.utilities = utilities.Utilities()
		self.internalTransitionStateIndex = 1

	def returnTranState(self, value, fromState):
		for tranStateIdx in range(0, len(self.transitionStates)):
			tranState = self.transitionStates[tranStateIdx]

			if(tranState.value == value and 
				tranState.fromState == fromState):
				return self.transitionStates[tranStateIdx]

		return None

	def currentInternalTransitionState(self):
		state = "st" + str(self.internalTransitionStateIndex)
		return state

	def buildInternalTransitionState(self, fromState, toState, value):
		newToState = ''
		
		if(toState == None):
			self.internalTransitionStateIndex = self.internalTransitionStateIndex + 1
			newToState = self.currentInternalTransitionState()
		else:
			newToState = self.endState

		newTranState = transitionState.TransitionState(fromState, newToState, value, [])

		self.transitionStates.append(newTranState)

	def parseLexicon(self, lexiconVals):
		# always set our start state to q0
		self.startState = "q0"
		self.endState = "q1"
		self.internalTransitionStateIndex = 0
		self.transitionStates = []

		internalEndStateCounter = 0
		internalEndStates = []

		for key, value in lexiconVals.iteritems():

			internalEndStateCounter = internalEndStateCounter + 1

			for wordIdx in range(0, len(value)):
				currentWord = value[wordIdx]

				transitionStateHistory = []
				haveBuiltNewState = False

				for charIdx in range(0, len(currentWord)):
					currentChar = currentWord[charIdx]

					# start state?
					if(charIdx == 0):
						# does a transition exist already with our current character?
						transitionState = self.returnTranState(currentChar, self.startState)

						if(transitionState == None or 
							haveBuiltNewState):

							self.buildInternalTransitionState(self.startState, None, currentChar)
							transitionStateHistory.append(self.currentInternalTransitionState())
							haveBuiltNewState = True

						else:
							transitionStateHistory.append(transitionState.toState)
						
					elif(charIdx == len(currentWord)-1):
						fromState = transitionStateHistory[len(transitionStateHistory)-1]
						
						# does a transition exist already with our current character?
						transitionState = self.returnTranState(currentChar, fromState)

						if(transitionState == None or 
							transitionState.toState != self.endState or 
							haveBuiltNewState):


							self.buildInternalTransitionState(fromState, self.endState, currentChar)
							haveBuiltNewState = True

					else: 
						fromState = transitionStateHistory[len(transitionStateHistory)-1]
						
						transitionState = self.returnTranState(currentChar, fromState)

						if(transitionState == None or 
							haveBuiltNewState):

							self.buildInternalTransitionState(fromState, None, currentChar)
							haveBuiltNewState = True

						transitionStateHistory.append(self.currentInternalTransitionState())

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

			tranStates = self.utilities.createTransitionState(line)

			for j in range(0, len(tranStates)):
				if(i == 1):
					self.startState = tranStates[j].fromState

				self.transitionStates.append(tranStates[j])

	def getPreviousTransitions(self, currentState):
		currentStates = []

		for i in range(0, len(self.transitionStates)):
			if(self.transitionStates[i].toState == currentState):
				currentStates.append(self.transitionStates[i])

		return currentStates

	def returnHighestProb(self, userInput):
		acceptableStates = self.processFst(userInput)

		highestProbability = Decimal(0)
		bestPath = None

		for i in range(0, len(acceptableStates)):

			statesToEvaluate = acceptableStates[i]

			runningProbability = Decimal(1)

			for j in range(0, len(statesToEvaluate)):

				state = statesToEvaluate[j]

				if(state.weight == None):
					runningProbability = 0   
				else:
					runningProbability = runningProbability * Decimal(state.weight)

			if(runningProbability > highestProbability):
				bestPath = statesToEvaluate
				highestProbability = runningProbability

		outputStr = ""
		if(bestPath != None):
			for i in range(len(bestPath)):
				idx = len(bestPath) - i - 1

				if(bestPath[idx].output != self.epsilonState):
					outputStr = outputStr + " \"" + bestPath[idx].output + "\""

		else: 
			outputStr = outputStr + "*none*"   # unacceptable string outputs *none*

		return (outputStr + " " + str(highestProbability.normalize())).strip()   # normalize() gets rid of extra zeros in Decimal


	# fst and wfst function
	def processFst(self, userInput):
		# assuming the input is just in one line, the main file will split it for me...
		# this function will simply return a yes or no
		splitValues = re.split("\s+", userInput)
		listOfAcceptedStates = []

		# if your FST has the same start and final state, it should accept an empty string. You can do this by giving it the empty-string symbol '*e*':
		if(len(splitValues) == 1 and self.startState == self.endState and splitValues[0] == self.epsilonState):
			tranState = transitionState.TransitionState(self.startState, self.endState, "*e*", ["*e*", "1"])
			return [[tranState]]

		# working our way back
		# stack structure
		workSpace = []

		# get final transitions
		finalStates = self.getPreviousTransitions(self.endState)

		# add in all the work objects
		for i in range(0, len(finalStates)):
			endIdx = len(splitValues)-1
			workObject = wordTransitions.WordTransitions(endIdx, finalStates[i], [])
			workSpace.append(workObject)

		while(len(workSpace) > 0):
			workObject = workSpace.pop(0)

			wordIdx = workObject.wordIdx
			
			isBeginningWord = wordIdx == 0
			word = self.utilities.cleanseInput(splitValues[wordIdx])

			state = workObject.currentState
			# create a new list
			newStateList = []
			
			for i in range(0, len(workObject.previousStates)):
				newStateList.append(workObject.previousStates[i])

			newStateList.append(state)

			# does this transition to the previous state?
			if(state.value == word):
				if(isBeginningWord and self.isBeginningState(state.fromState)):
					listOfAcceptedStates.append(newStateList)
				else:
					previousWordIdx = wordIdx - 1

					# don't pump bad indexes in 
					if(previousWordIdx < 0):
						continue

					previousStates = self.getPreviousTransitions(state.fromState)

					for i in range(0, len(previousStates)):
						newWorkObject = wordTransitions.WordTransitions(previousWordIdx, previousStates[i], newStateList)
						workSpace.append(newWorkObject)

			elif(state.value == self.epsilonState):
				if(isBeginningWord and self.isBeginningState(state.fromState)):
					listOfAcceptedStates.append(newStateList)
				else:
					previousStates = self.getPreviousTransitions(state.fromState)

					for i in range(0, len(previousStates)):
						newWorkObject = wordTransitions.WordTransitions(wordIdx, previousStates[i], newStateList)
						workSpace.append(newWorkObject)

		return listOfAcceptedStates

	# fsa function
	def processInput(self, userInput):
		res = self.processFst(userInput)

		return len(res) > 0

	# (should be) private helper functions
	def isBeginningState(self, currentState):
		if(currentState == self.startState):
			return True
		else:
			return False
