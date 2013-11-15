import utilities
import postuple


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


	def GetPrevPathWithHighestProb(self, emittingStates, prev_state):
	# find maximum of the probabilities of BOS -> [emittingStates]
		highestProbState = ''
		highestProb = 0.0
#		print emittingStates
		for state in emittingStates:
#			print state
			if self.current_trans_dict[prev_state].has_key(state):
				probability = self.current_trans_dict[prev_state][state]
				if probability > highestProb:
					highestProb = probability
					highestProbState = state

		return highestProbState, highestProb


		
