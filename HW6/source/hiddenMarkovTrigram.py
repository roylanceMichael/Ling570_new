import math
import hiddenMarkovBigram

class HiddenMarkovTrigram(hiddenMarkovBigram.HiddenMarkovBigram):
	def __init__(self, unknownDictionary):
		hiddenMarkovBigram.HiddenMarkovBigram.__init__(self)
		self.unigramTransitionDictionary = { }
		self.trigramTransitionDictionary = { }
		self.emissionKeyDictionary = { } 
		self.unigramTotalWords = 0
		self.unknownDictionary = unknownDictionary

	def state_num(self):
		return len(self.trigramTransitionDictionary)

	def trans_line_num(self):
		# calculating this the hard way for the time being...
		return self.getDictLineCount(self.trigramTransitionDictionary)

	def addUnigram(self, pos):
		if(self.unigramTransitionDictionary.has_key(pos)):
			self.unigramTransitionDictionary[pos] = self.unigramTransitionDictionary[pos] + 1
		else:
			self.unigramTransitionDictionary[pos] = 1

	def getUnigramProb(self, pos):
		uni_total = self.getDictTotal(self.unigramTransitionDictionary)
		return self.unigramTransitionDictionary[pos] / float(self.unigramTotalWords)


	def getTrigramProb(self, from_state1, from_state2, to_state):
		from_state_key = from_state1 + "~" + from_state2

		from_dict = self.getDicts(from_state_key, self.trigramTransitionDictionary)
		from_total = self.getDictTotal(from_dict)
		to_total = from_dict[to_state]

		return float(to_total) / from_total

	def addParsedLine(self, parsedTuples):
		# given in the format of [[ wordTuple, wordTuple, wordTuple ]]
		if(len(parsedTuples) > 0):
			initFirstTuple = parsedTuples[0][0]
			initSecondTuple = parsedTuples[0][1]

			initFirstKey = initFirstTuple.pos + '~' + initSecondTuple.pos

			if(self.initDictionary.has_key(initFirstKey)):
				self.initDictionary[initFirstKey] = self.initDictionary[initFirstKey] + 1
			else:
				self.initDictionary[initFirstKey] = 1

			# including EOS here for now...
			parseTuplesLen = len(parsedTuples)

			for i in range(0, parseTuplesLen):
				self.unigramTotalWords += 1
				# add transitions for both
				firstTuple = parsedTuples[i][0]
				secondTuple = parsedTuples[i][1]
				thirdTuple = parsedTuples[i][2]

				# add in the unigram
				self.addUnigram(firstTuple.pos)

				# add in the bigram
				self.addTransition(secondTuple.pos, firstTuple.pos)

				# add in the trigram
				self.addTrigramTransitionDictionary(thirdTuple.pos, firstTuple.pos, secondTuple.pos)

				self.addEmission(firstTuple.word, firstTuple.pos)

				wordPosTuple = secondTuple.pos + "~" + secondTuple.word
				self.addToEmissionKeyDictionary(wordPosTuple, firstTuple.pos)
				

			# account for last tuples...
			thirdToLastTuple = parsedTuples[parseTuplesLen - 1][0]
			secondToLastTuple = parsedTuples[parseTuplesLen - 1][1]
			lastTuple = parsedTuples[parseTuplesLen - 1][2]

			# add in the unigramTransitionDictionary
			self.addUnigram(secondToLastTuple.pos)
			self.addUnigram(lastTuple.pos)

			# add in the bigram
			self.addTransition(lastTuple.pos, secondToLastTuple.pos)

			# add in the emissions
			self.addEmission(secondToLastTuple.word, secondToLastTuple.pos)
			self.addEmission(lastTuple.word, lastTuple.pos)

			self.addToEmissionKeyDictionary(secondToLastTuple.pos + "~" + secondToLastTuple.word, thirdToLastTuple.pos)
			self.addToEmissionKeyDictionary(lastTuple.pos + "~" + lastTuple.word, secondToLastTuple.pos)

			self.unigramTotalWords += 1

	def addToEmissionKeyDictionary(self, posTuple, previousPos):
		if(self.emissionKeyDictionary.has_key(posTuple)):
			self.emissionKeyDictionary[posTuple][previousPos] = 1
		else:
			self.emissionKeyDictionary[posTuple] = { previousPos: 1 } 

	def addTrigramTransitionDictionary(self, to_state, from_state1, from_state2):
### P(to_state | from_state1 from_state2)
		from_state_key = from_state1 + "~" + from_state2
		to_state_key = from_state2 + "~" + to_state
		self.addToDict(from_state_key, to_state_key, self.trigramTransitionDictionary)

	def getTransitionsTrigram(self, from_state1, from_state2):
		key = from_state1 + "~" + from_state2
		return self.getDicts(key, self.trigramTransitionDictionary)

	def getTrigramTransitionDictionary(self, from_state1, from_state2, to_state):
		from_state_key = from_state1 + "~" + from_state2
		to_state_key = from_state2 + "~" + to_state
		return self.getDict(from_state_key, to_state_key, self.trigramTransitionDictionary)

	# get smoothed interpolated probability
	# p(t3 | t1, t2) = lambda3 * P(t3 | t1, t2) + lambda2 * P(t3 | t2) + lambda1 * P(t3)
	def getSmoothedTrigramProbability(self, from_state1, from_state2, to_state, lambda1, lambda2, lambda3):
		trigramProbability = self.getTrigramProb(from_state1, from_state2, to_state)

		bigramToState = to_state.split("~")[1]
		bigramProbability = self.getBigramProb(from_state2, bigramToState)

		# https://catalyst.uw.edu/gopost/conversation/fxia/820083
		# For this hw, if (x, y) is an unseen bigram, you can simply set P(z | x, y) to be zero.
		# In that case, \sum_z P_smooth (z | x, y) will not add up to one, and that is fine.
		if(bigramProbability == 0):
			return 0

		unigramProbability = self.getUnigramProb(bigramToState)

		return lambda3 * trigramProbability + lambda2 * bigramProbability + lambda1	* unigramProbability

	def getSmoothedBigramProbability(self, from_state, to_state, lambda1, lambda2, lambda3):
		bigramProbability = self.getBigramProb(from_state, to_state)
		unigramProbability = self.getUnigramProb(to_state)
		return (lambda3 + lambda2) * bigramProbability + lambda1 * unigramProbability

	def reportTrigramTransitions(self, lambda1, lambda2, lambda3):
		# TODO: make sure that we're accounting for the bigram smoothing probability, see HW5
		strBuilder = ''

		for key in self.trigramTransitionDictionary:

			fromStates = key.split("~")
			from_state1 = fromStates[0]
			from_state2 = fromStates[1]

			if(from_state1 == "BOS"):
				prob = self.getSmoothedBigramProbability(from_state1, from_state2, lambda1, lambda2, lambda3)
				strBuilder = strBuilder + from_state1 + "~" + from_state1 + "\t" + from_state2 + "\t" + str(prob) + "\t" + str(math.log10(prob)) + "\n"

			subDict = self.trigramTransitionDictionary[key]

			for to_state in subDict:
				prob = self.getSmoothedTrigramProbability(from_state1, from_state2, to_state, lambda1, lambda2, lambda3)
				strBuilder = strBuilder + key + "\t" + to_state + "\t" + str(prob) + "\t" + str(math.log10(prob)) + "\n"

		return strBuilder

	def reportEmissionValuesWithUnknownWords(self, dictionary):
		strBuilder = ''

		for parentKey in dictionary:
			strBuilder = strBuilder + self.reportSubDictionaryValues(parentKey, dictionary[parentKey])

		return strBuilder

	def reportSubDictionaryValues(self, tag, symbolDictionary):
		total = self.getDictTotal(symbolDictionary)

		strBuilder = ''

		for symbol in symbolDictionary:
			
			if symbol == '</s>':
				continue

			unknownProb = self.getUnknownProb(tag)
			
			tagWordKey = tag + "~" + symbol
			if(self.emissionKeyDictionary.has_key(tagWordKey)):
				for previousTag in self.emissionKeyDictionary[tagWordKey]:
					state = previousTag + "~" + tag
					strBuilder = strBuilder + self.reportLineInfoSmoothing(state, symbol, symbolDictionary[symbol], total, unknownProb)
		
		return strBuilder

	def getUnknownProb(self, tag):
		if(self.unknownDictionary.has_key(tag)):
			return self.unknownDictionary[tag]
		return 0

	def calculateEmissionProb(self, numerator, denominator, unknownProb):
		if(numerator == 0 or denominator == 0):
			return unknownProb
		return (float(numerator) / denominator) * (1 - unknownProb)

	def reportSubDictionaryValuesNoSmoothing(self, parentKey, subDictionary):
		total = self.getDictTotal(subDictionary)

		strBuilder = ''
		for subKey in subDictionary:
			
			if subKey == 'EOS':
				continue

			strBuilder = strBuilder + self.reportLineInfo(parentKey, subKey, subDictionary[subKey], total)
		return strBuilder

	def reportLineInfoSmoothing(self, firstLabel, secondLabel, numerator, denominator, unknownProb):
### if known: Psmooth(w | tag) = P(w | tag) * (1 - P(<unk> | tag))
### else: Psmooth(w | tag) = P(<unk> | tag)

		prob = self.calculateEmissionProb(numerator, denominator, unknownProb)

		if(prob == 0):
			return (firstLabel + '\t' + secondLabel + '\t0\t0 - warning! 0 probability detected').strip() + '\n'	
		return (firstLabel + '\t' + secondLabel + '\t' + str(prob) + '\t' + str(math.log10(prob))).strip() + '\n'

	def getTransDictCount(self):
		totalCount = 0
		for key in self.trigramTransitionDictionary:
			subDict = self.trigramTransitionDictionary[key]
			fromStates = key.split("~")
			from_state1 = fromStates[0]
			from_state2 = fromStates[1]

			if(from_state1 == "BOS"):
				totalCount = totalCount + 1

			for subKey in subDict:
				totalCount = totalCount + 1

		return totalCount

	def printHmmFormat(self, lambda1, lambda2, lambda3):
		strBuilder = ''

		strBuilder = strBuilder + 'state_num=' + str(self.state_num()) + '\n'
		strBuilder = strBuilder + 'sym_num=' + str(self.sym_num()) + '\n'
		strBuilder = strBuilder + 'init_line_num=' + str(self.init_line_num()) + '\n'
		strBuilder = strBuilder + 'trans_line_num=' + str(self.getTransDictCount()) + '\n'
		strBuilder = strBuilder + 'emiss_line_num=' + str(self.emiss_line_num()) + '\n'
		strBuilder = strBuilder + '\n'
		# init
		strBuilder = strBuilder + '\init\n'

		# init is different, so we'll just do here
		strBuilder = strBuilder + self.reportSubDictionaryValuesNoSmoothing('', self.initDictionary)
		strBuilder = strBuilder + '\n'
		strBuilder = strBuilder + '\n'
		strBuilder = strBuilder + '\n'

		# todo: implement probabilities for transitions
		strBuilder = strBuilder + '\\transition\n'
		strBuilder = strBuilder + self.reportTrigramTransitions(lambda1, lambda2, lambda3)
		strBuilder = strBuilder + '\n'

		# emissions
		strBuilder = strBuilder + '\emission\n'
		strBuilder = strBuilder + self.reportEmissionValuesWithUnknownWords(self.emissionDictionary)

		return strBuilder

