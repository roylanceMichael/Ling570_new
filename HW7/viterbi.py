import utilities
import math
import re
import postuple
import transition
import transitionHistory

class Viterbi(utilities.Utilities):
	def __init__(self):
		utilities.Utilities.__init__(self)
		self.unknownEmissProb = math.log10(.15)

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

	def getHighestProb(self, toState, word, incrementalStateProbs, i):
		highestProb = -2000
		highestProbState = ""
		
		for fromState in self.current_trans_dict:

			if(self.current_trans_dict[fromState].has_key(toState) and
				self.current_emiss_dict.has_key(toState) and
				incrementalStateProbs[i-1].has_key(fromState) and 
				self.current_emiss_dict[toState].has_key(word)):

				previousProb = incrementalStateProbs[i-1][fromState]
				transitionProb = self.current_trans_dict[fromState][toState]
				emissProb = self.current_emiss_dict[toState][word]

				tempCalc = math.log10(transitionProb * emissProb) + previousProb

				if(highestProb < tempCalc):
					highestProb = tempCalc
					highestProbState = fromState

		return (highestProb, highestProbState)

	def handleUnknownWord(self, incrementalStateProbs, i, path, newPath):
		# we're going to find the first acceptable transition here and add it in...
		# later, we'll randomize it a bit better

		for acceptableFromState in incrementalStateProbs[i-1]:

			# sanity check
			if(self.current_trans_dict.has_key(acceptableFromState)):

				# let's grab first key...
				for firstToState in self.current_trans_dict[acceptableFromState]:
					
					previousProb = incrementalStateProbs[i-1][acceptableFromState]
					transitionProb = self.current_trans_dict[acceptableFromState][firstToState]
					
					# set the state and path
					incrementalStateProbs[i][firstToState] = previousProb + math.log10(transitionProb) + self.unknownEmissProb
					newPath[firstToState] = path[acceptableFromState] + [firstToState]

					return

		# nothing to do here, we'll return on the first successful fromState/toState pair

	def processLine(self, line):
		words = re.split("\s+", line.strip())

		if(len(words) < 1):
			return "No observations given..."

		# testing this out
		V = [{}]
		path = {}

		# initialize
		beginningState = self.findBeginningState()
		
		if(beginningState == None):
			return "No beginning state found..."

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
				(highestProb, highestProbState) = self.getHighestProb(toState, words[i], V, i)

				# if we didn't find any, we need to skip. we will handle unknown prob later
				if(not path.has_key(highestProbState)):
					continue 

				V[i][toState] = highestProb
				newPath[toState] = path[highestProbState] + [toState]

			# handle if words[i] is unknown
			if(len(V[i]) == 0):
				
				self.handleUnknownWord(V, i, path, newPath)

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

		return bestProb, [beginningState] + path[bestState]