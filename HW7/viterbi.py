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

		
