import math
import hiddenMarkov

class HiddenMarkovTrigram(hiddenMarkov.HiddenMarkov):
	def addParsedLine(self, parsedTuples):
		# given in the format of [ wordTuple, wordTuple, wordTuple ]
		if(len(parsedTuples) > 0):
			initFirstTuple = parsedTuples[0][0]
			initSecondTuple = parsedTuples[0][1]

			initFirstKey = initFirstTuple.pos + '~' + initSecondTuple.pos

			if(self.initDictionary.has_key(initFirstKey)):
				self.initDictionary[initFirstKey] = self.initDictionary[initFirstKey] + 1
			else:
				self.initDictionary[initFirstKey] = 1

			# not including EOS here for now...
			parseTuplesLen = len(parsedTuples) - 1

			for i in range(0, parseTuplesLen):
				# add transitions for both
				firstTuple = parsedTuples[i][0]
				secondTuple = parsedTuples[i][1]
				thirdTuple = parsedTuples[i][2]

				self.addTransition(thirdTuple.pos, firstTuple.pos, secondTuple.pos)

				# only add emissions for first, we'll add in last one at the end...
				self.addEmission(firstTuple.word, firstTuple.pos)

			# account for last tuple...
			lastTuple = parsedTuples[parseTuplesLen - 1][1]
			self.addEmission(lastTuple.word, lastTuple.pos)

	def addTransition(self, to_state, from_state1, from_state2):
		from_state_key = from_state1 + "~" + from_state2
		self.addToDict(from_state_key, to_state, self.transitionDictionary)

	def getTransitions(self, from_state1, from_state2):
		key = from_state1 + "~" + from_state2
		return self.getDicts(key, self.transitionDictionary)

	def getTransition(self, from_state1, from_state2, to_state):
		key = from_state1 + "~" + from_state2
		return self.getDict(key, to_state, self.transitionDictionary)