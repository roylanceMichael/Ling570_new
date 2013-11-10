import math
import hiddenMarkovBigram

class HiddenMarkovTrigram(hiddenMarkovBigram.HiddenMarkovBigram):
	def __init__(self):
		hiddenMarkovBigram.HiddenMarkovBigram.__init__(self)
		self.unigrams = { }
		self.transitionTrigram = { } 

	def addUnigram(self, pos):
		if(self.unigrams.has_key(pos)):
			self.unigrams[pos] = self.unigrams[pos] + 1
		else:
			self.unigrams[pos] = 1

	def getUnigramProb(self, pos):
		if(self.unigrams.has_key(pos)):
			return self.unigrams[pos] / float(len(self.unigrams))

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

				# add in the unigram
				self.addUnigram(firstTuple.pos)

				# add in the bigram
				self.addTransition(secondTuple.pos, firstTuple.pos)

				# add in the trigram
				self.addTransitionTrigram(thirdTuple.pos, firstTuple.pos, secondTuple.pos)

				# only add emissions for first, we'll add in last one at the end...
				self.addEmission(firstTuple.word, firstTuple.pos)

			# account for last tuples...
			secondToLastTuple = parsedTuples[parseTuplesLen - 1][1]
			lastTuple = parsedTuples[parseTuplesLen - 1][2]

			# add in the unigrams
			self.addUnigram(secondToLastTuple.pos)
			self.addUnigram(lastTuple.pos)

			# add in the bigram
			self.addTransition(lastTuple.pos, secondToLastTuple.pos)

			# add in the emissions
			self.addEmission(secondToLastTuple.word, secondToLastTuple.pos)
			self.addEmission(lastTuple.word, lastTuple.pos)

	def addTransitionTrigram(self, to_state, from_state1, from_state2):
		from_state_key = from_state1 + "~" + from_state2
		self.addToDict(from_state_key, to_state, self.transitionTrigram)

	def getTransitionsTrigram(self, from_state1, from_state2):
		key = from_state1 + "~" + from_state2
		return self.getDicts(key, self.transitionTrigram)

	def getTransitionTrigram(self, from_state1, from_state2, to_state):
		key = from_state1 + "~" + from_state2
		return self.getDict(key, to_state, self.transitionTrigram)