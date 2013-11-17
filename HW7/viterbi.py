import utilities
import math
import re
import postuple
import transition
import transitionHistory

class Viterbi(utilities.Utilities):
	def __init__(self):
		utilities.Utilities.__init__(self)

	def getUnknownState(self):
		return "N"

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

	def reportBestPath(self, transHistories):
		highestProb = -20000
		highestProbTrans = ""

		for i in range(0, len(transHistories)):
			prob = transHistories[i].getProbability()

			if(prob > highestProb):
				highestProb = prob
				highestProbTrans = transHistories[i].reportTransitions()

		bestPath = highestProbTrans + " " + str(highestProb)
		return bestPath.strip()

	def processLine(self, line):
		words = re.split("\s+", line.strip())

		if(len(words) == 0):
			return []

		# testing this out
		V = [{}]
		path = {}

		# initialize
		beginningState = self.findBeginningState()
		
		if(beginningState == None):
			return "No beginning state found..."

		for toState in self.current_trans_dict:

			# do we exist in the current transition dictionary?
			if(self.current_trans_dict[beginningState].has_key(toState) and
				self.current_emiss_dict.has_key(toState) and
				self.current_emiss_dict[toState].has_key(words[0])):

				transitionProb = math.log10(self.current_trans_dict[beginningState][toState])
				emitProb = math.log10(self.current_emiss_dict[toState][words[0]])
				V[0][toState] = transitionProb + emitProb
				path[toState] = [toState]

		# check to see if first word is unknown
		if(len(V[0]) == 0):
			# hard coding in the emission prob
			emitProb = math.log10(.15)

			# getting let's just set all transitions, let the best one win
			for toState in self.current_trans_dict[beginningState]:
				transProb = math.log10(self.current_trans_dict[beginningState][toState])
				V[0][toState] = transProb + emitProb
				path[toState] = [toState] 

		# process as normal

		for i in range(1, len(words)):
			V.append({})
			newPath = {}

			for toState in self.current_trans_dict:

				# manually do the max function here...
				highestProb = -2000
				highestProbState = ""

				for fromState in self.current_trans_dict:

					if(self.current_trans_dict[fromState].has_key(toState) and
						self.current_emiss_dict.has_key(toState) and
						self.current_emiss_dict[toState].has_key(words[i])):


						previousProb = V[i-1][fromState]
						transitionProb = self.current_trans_dict[fromState][toState]
						emissProb = self.current_emiss_dict[toState][words[i]]

						tempCalc = math.log10(transitionProb * emissProb) + previousProb

						if(highestProb < tempCalc):
							highestProb = tempCalc
							highestProbState = fromState

				if(len(highestProbState) == 0):
					continue

				V[i][toState] = highestProb
				newPath[toState] = path[highestProbState] + [toState]

			# did we fill

			path = newPath

		bestState = ""
		bestProb = -2000

		for pos in self.current_trans_dict:
			if(V[i].has_key(pos) and
				V[i][pos] > bestProb and
				path.has_key(pos)):
				bestProb = V[i][pos]
				bestState = pos

		return bestProb, path[bestState]

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

			print 'working on ' + word + ' with ' + str(len(tranHistories))

			# I need to find the parts of speech that belong to this word
			for partOfSpeech in self.current_emiss_dict:

				# if this doesn't contain our key, let's leave
				if(not statesToProcess.has_key(partOfSpeech)):
					continue
				
				# handle the symbols
				foundSymbol = False
				for symbol in self.current_emiss_dict[partOfSpeech]:

					if(symbol != word):
						continue

					foundSymbol = True

					highestProb = -2000
					highestProbTrans = None 

					for fromState in statesToProcess[partOfSpeech]:
						# calculate the probabilities

						transProb = math.log10(statesToProcess[partOfSpeech][fromState] * self.current_emiss_dict[partOfSpeech][symbol])
						toState = partOfSpeech

						trans = transition.Transition(toState, fromState, word, transProb)

						# if this is the beginning, then we need to add the appropriate histories

						if(i == 0):
							tranHistory = transitionHistory.TransitionHistory()
							tranHistory.addTransition(trans)
							tempTranHistories.append(tranHistory)

						else:
							# find the transition history to append to
							for j in range(0, len(tranHistories)):
								
								# if we can add to an existing one
								if(tranHistories[j].canAddTransition(trans)):
									# clone it and add the new path
									newTranHistory = tranHistories[j].cloneHistoryAndAddTransition(trans)
									tempTranHistories.append(newTranHistory)

				if(not foundSymbol):
					if(len(statesToProcess) == 0):
						break

					fromState = ''

					for fromStateKey in statesToProcess[partOfSpeech]:
						fromState = fromStateKey
						break

					unknownWord = "<unk>"
					unknownStateProb = .234
					transProb = statesToProcess[partOfSpeech][fromState] * unknownStateProb
					trans = transition.Transition(partOfSpeech, fromState, word, transProb)

					if(i == 0):
						tranHistory = transitionHistory.TransitionHistory()
						tranHistory.addTransition(trans)
						tempTranHistories.append(tranHistory)
					else:
						# find the transition history to append to
						for j in range(0, len(tranHistories)):
							
							# if we can add to an existing one
							if(tranHistories[j].canAddTransition(trans)):
								# clone it and add the new path
								newTranHistory = tranHistories[j].cloneHistoryAndAddTransition(trans)
								tempTranHistories.append(newTranHistory)

			# get rid of old histories with new cloned ones
			# this also gids rid of the transitions that don't continue
			tranHistories = tempTranHistories

			# build the new states to process
			statesToProcess = self.buildStatesToProcess(statesToProcess)

		return tranHistories