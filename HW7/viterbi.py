import utilities
import re
import postuple
import transition
import transitionHistory

class Viterbi(utilities.Utilities):
	def __init__(self):
		utilities.Utilities.__init__(self)

	def findBeginningState(self):
		# we want to find a state that exists in fromState but not toState
		for outerFromState in self.current_trans_dict:
			existsInToState = False
			
			for fromState in self.current_trans_dict:
				for toState in self.current_trans_dict[fromState]:
					if(toState == outerFromState):
						existsInToState = True
						break

				if(existsInToState):
					break

			if(not existsInToState):
				return outerFromState

		return None

	def buildStatesToProcess(self, statesToProcess):
		# we need to do something with the states now...
		newStatesToProcess = {}

		# go through all the states and treat them like from states
		for newFromState in statesToProcess:
			for fromState in self.current_trans_dict:
				if(newFromState != fromState):
					continue

				# we need to go through all the new toStates and add them in the dictionary to process next
				for toState in self.current_trans_dict[fromState]:
					if(newStatesToProcess.has_key(toState)):
						newStatesToProcess[toState][fromState] = self.current_trans_dict[fromState][toState]
					else:
						newStatesToProcess[toState] = { fromState: self.current_trans_dict[fromState][toState] }

		return newStatesToProcess

	def processLineForwards(self, line):
		words = re.split("\s+", line.strip())

		beginningState = self.findBeginningState()

		if(beginningState == None):
			return "No beginning state found..."

		# start at the beginning, get all the bos states
		statesToProcess = self.buildStatesToProcess({ beginningState:0 })

		tranHistories = []

		# we have our beginning states to look at, let's cycle through our words
		for i in range(0, len(words)):
			word = words[i]

			tempTranHistories = []
			
			# I need to find the parts of speech that belong to this word
			for partOfSpeech in self.current_emiss_dict:

				# if this doesn't contain our key, let's leave
				if(not statesToProcess.has_key(partOfSpeech)):
					continue

				# handle the symbols
				for symbol in self.current_emiss_dict[partOfSpeech]:

					if(symbol != word):
						continue

					for fromState in statesToProcess[partOfSpeech]:
						transProb = statesToProcess[partOfSpeech][fromState] * self.current_emiss_dict[partOfSpeech][symbol]
						toState = partOfSpeech

						trans = transition.Transition(toState, fromState, word, transProb)

						# if this is the beginning, then we need to add the appropriate histories
						if(i == 0):
							# print 'adding a new tranHistory'
							tranHistory = transitionHistory.TransitionHistory()
							tranHistory.addTransition(trans)
							tempTranHistories.append(tranHistory)

						else:
							# find the transition history to append to
							for j in range(0, len(tranHistories)):
								if(tranHistories[j].canAddTransition(trans)):
									newTranHistory = tranHistories[j].cloneHistoryAndAddTransition(trans)
									tempTranHistories.append(newTranHistory)

			# get rid of old histories with new cloned ones
			# this also gids rid of the transitions that don't continue
			tranHistories = tempTranHistories

			# build the new states to process
			statesToProcess = self.buildStatesToProcess(statesToProcess)

		return tranHistories

	def processLine(self, line):
		words = re.split("\s+", line.strip())
		prevState = ""

		# let's focus on building up an array of paths that work
		transitionHistory = []

		for i in range(0, len(words)):
			# we start at the last word
			realIdx = len(words) - i - 1

			currentSymbol = words[realIdx]

			# let's get all the states that belong with this word
			emittingStates = self.getPrevPathState(currentSymbol)

			# let's look at the transitionHistory

			paths = self.getPrevPathWithHighestProb(emittingStates, prevState)

			print paths

			# prevState = highestProbPath[1]
			# transitionHistory.append((highestProbPath[0], highestProbPath[1], highestProbPath[2], currentSymbol))

		return transitionHistory
			

	def findFromStateGivenToState(self, toState):
		tuples = []
		for fromState in self.current_trans_dict:
			toDicts = self.current_trans_dict[fromState]

			for toStateKey in toDicts:
				if(toStateKey == toState):
					tuples.append((fromState, toState, toDicts[toState]))

		return tuples

	def getPrevPathState(self, observation):
	# get list of states that output the observation
		emittingStates = []
		if observation in self.current_symb_dict:
			for key in self.current_symb_dict[observation]:
				emittingStates.append((observation, key, self.current_symb_dict[observation][key]))
		return emittingStates


	def getPrevPathWithHighestProb(self, emittingStates, prevState):
	# find maximum of the probabilities of BOS -> [emittingStates]
		# highestProbFromState = ''
		# highestEmittingState = ''
		# highestProb = 0.0
		# print emittingStates

		stateProbabilities = []

		for state in emittingStates:

			if(prevState != state[1]):
				continue

			allFromStateToStateTuples = self.findFromStateGivenToState(state[1])

			for i in range(0, len(allFromStateToStateTuples)):
				# P(symbol | state) = state[2]
				# P(toState | fromState) = allFromStateToStateTuples[i][2]
				stateProbability = state[2] * allFromStateToStateTuples[i][2]
				fromState = allFromStateToStateTuples[i][0]
				toState = allFromStateToStateTuples[i][1]
				symbol = state[0]
				stateProbabilities.append((fromState, toState, symbol, stateProbability))

		return stateProbabilities

#			print state
#			if self.current_trans_dict[prev_state].has_key(state):
#				probability = self.current_trans_dict[prev_state][state]
#				if probability > highestProb:
#					highestProb = probability
#					highestProbState = state

#		return highestProbState, highestProb


		
