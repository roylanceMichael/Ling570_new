import utilities
import math
import re

class Viterbi(utilities.Utilities):
	def __init__(self):
		utilities.Utilities.__init__(self)
		self.unknownEmissProb = math.log10(.15)
		self.delimiter = "~"

	def findBeginningState(self):
		# get first key from current_trans_dict
		for state in self.current_trans_dict:
			break

		if("_" in state):
			self.delimiter = "_"
		elif("~" in state):
			self.delimiter = "~"
		elif("-" in state):
			self.delimiter = "-"

		tags = state.split(self.delimiter)

		if(len(tags) > 1):
			return "BOS" + self.delimiter + "BOS"
		else:
			return "BOS"

	def buildBeginningStateProbabilities(self, beginningState, word, incrementalStateProbs, path):
		# first, let's see if our states have been build...
		if(len(self.flattenedStates) == 0):
			self.buildFlattenedStates()

		for toState in self.flattenedStates:

			# do we exist in the current transition dictionary?
			if(self.current_trans_dict[beginningState].has_key(toState) and
				self.current_emiss_dict.has_key(toState) and
				self.current_emiss_dict[toState].has_key(word)):

				transitionProb = math.log10(self.current_trans_dict[beginningState][toState])
				emitProb = math.log10(self.current_emiss_dict[toState][word])
				incrementalStateProbs[0][toState] = transitionProb + emitProb
				path[toState] = [toState]

		# check to see if first word is unknown
		if(len(incrementalStateProbs[0]) == 0):
			
			# getting let's just set all transitions, let the best one win
			for toState in self.current_trans_dict[beginningState]:
				transProb = math.log10(self.current_trans_dict[beginningState][toState])
				incrementalStateProbs[0][toState] = transProb + self.unknownEmissProb
				path[toState] = [toState] 

	def getHighestProb(self, toState, words, incrementalStateProbs, i):
		highestProb = -2000
		highestProbState = ""

		for fromState in self.current_trans_dict:
			
			if(self.current_trans_dict[fromState].has_key(toState) and
				self.current_emiss_dict.has_key(toState) and
				incrementalStateProbs[i-1].has_key(fromState) and 
				self.current_emiss_dict[toState].has_key(words[i])):

				previousProb = incrementalStateProbs[i-1][fromState]
				transitionProb = self.current_trans_dict[fromState][toState]
				emissProb = self.current_emiss_dict[toState][words[i]]

				tempCalc = transitionProb * emissProb
				
				if(tempCalc != 0):
					tempCalc = math.log10(transitionProb * emissProb) + previousProb

				if(highestProb < tempCalc):
					highestProb = tempCalc
					highestProbState = fromState

		return (highestProb, highestProbState)

	def handleUnknownWord(self, incrementalStateProbs, i, path, newPath, words):
		currentWord = words[i]
		unknownWord = "<unk>"

		highestUnkToState = ''
		highestUnkFromState = ''
		highestUnknownProb = -2000

		for acceptableFromState in incrementalStateProbs[i-1]:

			# sanity check
			if(self.current_trans_dict.has_key(acceptableFromState)):

				for toState in self.current_trans_dict[acceptableFromState]:

					if(self.current_emiss_dict.has_key(toState) and
						self.current_emiss_dict[toState].has_key(unknownWord)):

						previousProb = incrementalStateProbs[i-1][acceptableFromState]
						transitionProb = self.current_trans_dict[acceptableFromState][toState]
						emissProb = self.current_emiss_dict[toState][unknownWord]

						probToCalculate = previousProb + math.log10(transitionProb) + math.log10(emissProb)

						if(probToCalculate > highestUnknownProb):
							highestUnknownProb = probToCalculate
							highestUnkFromState = acceptableFromState
							highestUnkToState = toState

		if(len(highestUnkFromState) > 0):
			# set the state and path
			incrementalStateProbs[i][highestUnkToState] = highestUnknownProb
			newPath[highestUnkToState] = path[highestUnkFromState] + [highestUnkToState]

	def processLine(self, line):
		words = re.split("\s+", line.strip())

		if(len(words) < 1):
			return "No observations given..."

		# testing this out
		V = [{}]
		path = {}

		# initialize
		beginningState = self.findBeginningState()

		# also handles unknown words
		self.buildBeginningStateProbabilities(beginningState, words[0], V, path)

		# process as normal
		# case where we have just one word, used later...
		i = 0
		for i in range(1, len(words)):
			# create a new dictionary at the end of the array
			V.append({})

			# temporary path that we build with existing states
			newPath = {}

			for toState in self.current_trans_dict:

				# manually do the max function here...
				(highestProb, highestProbState) = self.getHighestProb(toState, words, V, i)

				# if we didn't find any, we need to skip. we will handle unknown prob later
				if(not path.has_key(highestProbState)):
					continue 

				V[i][toState] = highestProb
				newPath[toState] = path[highestProbState] + [toState]

			# handle if words[i] is unknown
			if(len(V[i]) == 0):
				
				self.handleUnknownWord(V, i, path, newPath, words)
				if(len(V[i]) == 0):
					return "No transitions possible"

			path = newPath

		bestProb = -2000
		bestState = ""
		
		for pos in self.flattenedStates:
			if(V[i].has_key(pos) and
				V[i][pos] > bestProb and
				path.has_key(pos)):
				bestProb = V[i][pos]
				bestState = pos

		# just adding in beginning state to the first of the path
		if(not path.has_key(bestState)):
			return "No transitions possible"

		# TODO: fix this!..
		return bestProb, [beginningState] + path[bestState]
