import re

class HiddenMarkovFactory:
	def __init__(self):
		self.current_state_num = 0
		self.current_sym_num = 0
		self.current_init_line = 0
		self.current_trans_line_num = 0
		self.current_emiss_line_num = 0
		self.current_init_dict = {}
		self.current_trans_dict = {}
		self.current_emiss_dict = {}

		self.state_num_state = "state_num"
		self.sym_num_state = "sym_num"
		self.init_line_num_state = "init_line_num"
		self.trans_line_num_state = "trans_line_num"
		self.emiss_line_num_state = "emiss_line_num"
		self.init_state = "init_state"
		self.trans_state = "trans_state"
		self.emiss_state = "emiss_state"

		self.currentState = self.state_num_state

		self.numberRegex = "[0-9]+$"

	# meant to be used as private...
	def readInput(self, hmmInputLine):
		if(hmmInputLine.strip() == ""):
			return

		if(self.currentState == self.state_num_state):
			self.currentState = self.sym_num_state
			match = re.search(self.numberRegex, hmmInputLine)

			if(match != None):
				self.current_state_num = int(hmmInputLine[match.start():match.end()])
		
		elif(self.currentState == self.sym_num_state):
			self.currentState = self.init_line_num_state
			match = re.search(self.numberRegex, hmmInputLine)

			if(match != None):
				self.current_sym_num = int(hmmInputLine[match.start():match.end()])		
		
		elif(self.currentState == self.init_line_num_state):
			self.currentState = self.trans_line_num_state
			match = re.search(self.numberRegex, hmmInputLine)

			if(match != None):
				self.current_init_line = int(hmmInputLine[match.start():match.end()])

		elif(self.currentState == self.trans_line_num_state):
			self.currentState = self.emiss_line_num_state
			match = re.search(self.numberRegex, hmmInputLine)

			if(match != None):
				self.current_trans_line_num = int(hmmInputLine[match.start():match.end()])	

		elif(self.currentState == self.emiss_line_num_state):
			self.currentState = self.init_state
			match = re.search(self.numberRegex, hmmInputLine)

			if(match != None):
				self.current_emiss_line_num = int(hmmInputLine[match.start():match.end()])

		elif(self.currentState == self.init_state):
			lineContents = re.split("\s+", hmmInputLine.strip())

			# assuming that 1st is from_state(s), 2rd is prob
			if(len(lineContents) > 0):
				firstItem = lineContents[0]
				if(firstItem == '\\transition'):
					self.currentState = self.trans_state
				elif(len(lineContents) > 1):
					# build up init dictionary
					self.current_init_dict[firstItem] = float(lineContents[1])
		elif(self.currentState == self.trans_state):
			lineContents = re.split("\s+", hmmInputLine.strip())

			# assuming that 1st is from_state(s), 2rd is prob
			if(len(lineContents) > 0):
				firstItem = lineContents[0]
				if(firstItem == '\\emission'):
					self.currentState = self.emiss_state
				elif(len(lineContents) > 2):
					to_state = lineContents[1]
					prob = float(lineContents[2])

					if(self.current_trans_dict.has_key(firstItem)):
						self.current_trans_dict[firstItem][to_state] = prob
					else:
						self.current_trans_dict[firstItem] = { to_state: prob }

		elif(self.currentState == self.emiss_state):
			lineContents = re.split("\s+", hmmInputLine.strip())

			# assuming that 1st is from_state(s), 2rd is prob
			if(len(lineContents) > 0):
				firstItem = lineContents[0]
				if(len(lineContents) > 2):
					symbol = lineContents[1]
					prob = float(lineContents[2])
					
					if(self.current_emiss_dict.has_key(firstItem)):
						self.current_emiss_dict[firstItem][symbol] = prob
					else:
						self.current_emiss_dict[firstItem] = { symbol: prob }