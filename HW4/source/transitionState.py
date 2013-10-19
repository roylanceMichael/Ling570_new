import utilities

class TransitionState:
	def __init__(self, fromState, toState, value, props):
		self.fromState = fromState
		self.toState = toState
		self.value = value
		self.props = props

		util = utilities.Utilities()
		
		if(len(props) > 1):
			self.output = util.cleanseInput(props[0])
			self.weight = util.cleanseInput(props[1])
		elif(len(props) > 0):
			self.output = util.cleanseInput(props[0])
			self.weight = 1
		else:
			self.output = None
			self.weight = None

		
