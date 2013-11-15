import utilities


#class State:
#	def __init__(self):




class Viterbi(utilities.Utilities):
	def __init__(self):
		utilities.Utilities.__init__(self)


	def GetPrevPathState(self, observation):
	# get list of states that output the observation
		emittingStates = []
		if observation in self.current_symb_dict:
			for key in self.current_symb_dict[observation]:
				emittingStates.append(key)
		return emittingStates


	def GetPrevPathProb(self, emittingStates):
	# find maximum of the probabilities of BOS -> [emittingStates]
		transitionProbs = []
#		print emittingStates
		for state in emittingStates:
#			print state
#			print self.current_trans_dict['BOS']
			if self.current_trans_dict['BOS'].has_key(state):
				transitionProbs.append(self.current_trans_dict['BOS'][state])
		maxprob = max(transitionProbs)

		return maxprob


	def GetMaxProbEmittingState(self, maxprob):
	# find a key by float value?
		for key, value in self.current_trans_dict['BOS']:
			if value == maxprob:
				return key
		
