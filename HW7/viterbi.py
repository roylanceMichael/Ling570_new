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

		for pos in self.current_trans_dict:

			# do we exist in the current transition dictionary?
			
			if(self.current_trans_dict[beginningState].has_key(pos) and
				self.current_emiss_dict.has_key(pos) and
				self.current_emiss_dict[pos].has_key(words[0])):

				transitionProb = math.log10(self.current_trans_dict[beginningState][pos])
				emitProb = math.log10(self.current_emiss_dict[pos][words[0]])
				V[0][pos] = transitionProb + emitProb
				path[pos] = [pos]

		for i in range(1, len(words)):
			V.append({})
			newPath = {}

			for pos in self.current_trans_dict:

				# manually do the max function here...
				highestProb = -2000
				highestProbState = ""
				for innerPos in self.current_trans_dict:

					if(self.current_trans_dict[innerPos].has_key(pos) and
						self.current_emiss_dict.has_key(pos) and
						self.current_emiss_dict[pos].has_key(words[i])):

						print 'got this far...'
						# we have the previousProb, the transitionProb and the emissProb
						print V
						previousProb = V[i-1][innerPos]
						transitionProb = self.current_trans_dict[innerPos][pos]
						emissProb = self.current_emiss_dict[pos][words[i]]

						tempCalc = math.log10(transitionProb * emissProb) + previousProb

						if(highestProb < tempCalc):
							highestProb = tempCalc
							highestProbState = innerPos
				
				if(len(highestProbState) == 0):
					continue

				V[i][pos] = highestProb
				print str(path) + " " + highestProbState
				newPath[pos] = path[highestProbState] + [pos]

			path = newPath

		print 'final result ' + str(i)
		print path
		print V

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