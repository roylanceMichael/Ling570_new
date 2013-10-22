import unittest
import transitionState
import utilities
import fsa

class LexiconReadingTest(unittest.TestCase):

	def test_readInLexicon_simple(self):
		utils = utilities.Utilities()
		testStr = """walk       reg_verb_stem"""

		actualResult = utils.readLexicon(testStr)

		self.assertTrue(actualResult['reg_verb_stem'][0] == 'walk')

	def test_readInLexicon_moreComplex(self):
		utils = utilities.Utilities()
		testStr = """walk       reg_verb_stem
					talk       reg_verb_stem
					impeach    reg_verb_stem"""

		actualResult = utils.readLexicon(testStr)

		self.assertTrue(actualResult['reg_verb_stem'][0] == 'walk')
		self.assertTrue(actualResult['reg_verb_stem'][1] == 'talk')
		self.assertTrue(actualResult['reg_verb_stem'][2] == 'impeach')

	def test_readInLexicon_complex(self):
		utils = utilities.Utilities()
		testStr = """walk       reg_verb_stem
talk       reg_verb_stem
impeach    reg_verb_stem

cut        irreg_verb_stem
speak      irreg_verb_stem
sing       irreg_verb_stem

caught     irreg_past_verb_form
ate        irreg_past_verb_form
sang       irreg_past_verb_form
spoke      irreg_past_verb_form

eaten      irreg_past_verb_form
sung       irreg_past_verb_form
spoken     irreg_past_verb_form

ed         past
ed         past_participle
ing        pres_part
s          3sg
"""

		actualResult = utils.readLexicon(testStr)

		self.assertTrue(actualResult['reg_verb_stem'][0] == 'walk')
		self.assertTrue(actualResult['reg_verb_stem'][1] == 'talk')
		self.assertTrue(actualResult['reg_verb_stem'][2] == 'impeach')

		self.assertTrue(actualResult['irreg_verb_stem'][0] == 'cut')
		self.assertTrue(actualResult['irreg_verb_stem'][1] == 'speak')
		self.assertTrue(actualResult['irreg_verb_stem'][2] == 'sing')

		self.assertTrue(actualResult['irreg_past_verb_form'][0] == 'caught')
		self.assertTrue(actualResult['irreg_past_verb_form'][1] == 'ate')
		self.assertTrue(actualResult['irreg_past_verb_form'][2] == 'sang')
		self.assertTrue(actualResult['irreg_past_verb_form'][3] == 'spoke')

		self.assertTrue(actualResult['irreg_past_verb_form'][4] == 'eaten')
		self.assertTrue(actualResult['irreg_past_verb_form'][5] == 'sung')
		self.assertTrue(actualResult['irreg_past_verb_form'][6] == 'spoken')

		self.assertTrue(actualResult['past'][0] == 'ed')
		self.assertTrue(actualResult['past_participle'][0] == 'ed')
		self.assertTrue(actualResult['pres_part'][0] == 'ing')
		self.assertTrue(actualResult['3sg'][0] == 's')

class FsaTests(unittest.TestCase):

	def test_canReadMorphologyFile(self):
		testStr = """q3
(q0 (q3 irreg_past_verb_form))
(q0 (q1 reg_verb_stem))
(q1 (q3 past))
(q1 (q3 past_participle))
(q0 (q2 reg_verb_stem))
(q0 (q2 irreg_verb_stem))
(q2 (q3 pres_part))
(q2 (q3 3sg))
(q1 (q3 *e*))
(q2 (q3 *e*))"""

		fsaObj = fsa.Fsa()
		fsaObj.parse(testStr)

		self.assertTrue(fsaObj.endState == "q3")
		self.assertTrue(fsaObj.startState == "q0")

		self.assertTrue(fsaObj.transitionStates[0].value == "irreg_past_verb_form")
		self.assertTrue(fsaObj.transitionStates[0].fromState == "q0")
		self.assertTrue(fsaObj.transitionStates[0].toState == "q3")

		self.assertTrue(fsaObj.transitionStates[9].value == fsaObj.epsilonState)
		self.assertTrue(fsaObj.transitionStates[9].fromState == "q2")
		self.assertTrue(fsaObj.transitionStates[9].toState == "q3")


class TrieTests(unittest.TestCase):

  def test_fillTrie_small(self):
    testStr = """sing
sang
spoke
"""

    trieObj = trie.Trie()
    actualResult = trieObj.make_trie(testStr)
    # print actualResult
    self.assertTrue(actualResult == {'s': {'i': {'n': {'g': {'#': '#'}}}, 'a': {'n': {'g': {'#': '#'}}}, 'p': {'o': {'k': {'e': {'#': '#'}}}}}})


  def test_isinTrie(self):
    testStr = """sing
sang
spoke
"""
    testWord1 = "sing"
    
    trieObj = trie.Trie()
    ourtrie = trieObj.make_trie(testStr)
    actualResult = trieObj.in_trie(ourtrie, testWord1)
	# print actualResult
    self.assertTrue(actualResult == True)


class FstTransitionStates(unittest.TestCase):

	# as a TA, I will need to make sure that an FST has the output and weight attribute
	def test_outputAttributeExists(self):
		fromState = 'A'
		toState = 'B'
		value = 'C'
		output = 'coolOutput'
		props = [ output ]

		tranState = transitionState.TransitionState(fromState, toState, value, props)
		self.assertTrue(tranState.output == output)

	def test_weightAttributeExists(self):
		fromState = 'A'
		toState = 'B'
		value = 'C'
		output = 'coolOutput'
		weight = '.43'
		props = [ output, weight ]

		tranState = transitionState.TransitionState(fromState, toState, value, props)
		self.assertTrue(tranState.output == output)
		self.assertTrue(tranState.weight == weight)

class FstTests(unittest.TestCase):
	
	# this is where we'll continue on with testing
	def test_ctor(self):
		self.assertTrue(1==1)

	# So your code needs to 
	# follow multiple paths for an input string and check whether any of the paths ends 
	# at a final state.
	# So your code needs to 
	# follow multiple paths for an input string and check whether any of the paths ends 
 	# at a final state.
	# If there are multiple paths that end at a final state, choose the one 
	# with the highest probability. Your algorithm can be an extension of the algorithm 
	# in Figure 2.19 on Page 35 of J&M. 

	def test_correctIdentifiesOutputAndWeightInFsa(self):
		fsaObj = fsa.Fsa()
		testStr = """S
		(S (S "they" "PRO" 1.0))
		(S (S "can" "AUX" 0.99))
		(S (S "can" "VERB" 0.01))
		(S (S "fish" "NOUN" 0.7))
		(S (S "fish" "VERB" 0.3))
		"""

		fsaObj.parse(testStr)

		self.assertTrue(len(fsaObj.transitionStates) == 5)

		firstTranState = fsaObj.transitionStates[0]
		self.assertTrue(firstTranState.fromState == "S")
		self.assertTrue(firstTranState.toState == "S")
		self.assertTrue(firstTranState.value == "they")
		self.assertTrue(firstTranState.output == "PRO")
		self.assertTrue(firstTranState.weight == "1.0")

	def test_correctIdentifiesOutputAndWeightInFsa(self):
		fsaObj = fsa.Fsa()
		testStr = """S
		(S (S "they" "PRO" 1.0))
		(S (S "can" "AUX" 0.99))
		(S (S "can" "VERB" 0.01))
		(S (S "fish" "NOUN" 0.7))
		(S (S "fish" "VERB" 0.3))
		"""

		fsaObj.parse(testStr)

		# "they" "can" "fish" => (PRO) (AUX) (NOUN)
		userInput = "\"they\" \"can\" \"fish\""

		# this is an array of TransitionStates => [ tranState1, tranState2... ]
		actualResult = fsaObj.processFst(userInput)
		self.assertTrue(len(actualResult) == 4, 'len was ' + str(len(actualResult)))

		# a list of transitions
		for j in range(0, len(actualResult)):

			firstResult = actualResult[j]

			for i in range(0, len(firstResult)):
				# will blow up if not correct object
				testStr = firstResult[i].fromState + " -> " + firstResult[i].toState + " val: " + firstResult[i].value + " -> " + firstResult[i].output + " -> " + str(firstResult[i].weight)

	def test_correctlyReturnsHighestProbabilityOutput(self):
		fsaObj = fsa.Fsa()
		testStr = """S
		(S (S "they" "PRO" 1.0))
		(S (S "can" "AUX" 0.99))
		(S (S "can" "VERB" 0.01))
		(S (S "fish" "NOUN" 0.7))
		(S (S "fish" "VERB" 0.3))
		"""

		fsaObj.parse(testStr)

		# "they" "can" "fish" => "PRO" "AUX" "NOUN" .7
		userInput = "\"they\" \"can\" \"fish\""

		# this is an array of TransitionStates => [ tranState1, tranState2... ]
		actualResult = fsaObj.returnHighestProb(userInput)
		expectedResult = "\"PRO\" \"AUX\" \"NOUN\" 0.693"
		self.assertTrue(expectedResult == actualResult, actualResult + " <-> " + expectedResult)

	def test_correctlyDoesNotPrintEpsilon(self):
		fsaObj = fsa.Fsa()
		testStr = """S4
		(S0 (S1 "they" "PRO" 1.0))
		(S1 (S2 "can" "AUX" 0.8))
		(S1 (S3 "fish" "VERB" 0.1))
		(S1 (S3 "can" "VERB" 0.1))
		(S2 (S3 "can" "VERB" 0.7))
		(S2 (S3 "fish" "VERB" 0.3))
		(S3 (S4 "fish" "NOUN" 0.5))
		(S3 (S4 "can"  "NOUN" 0.1))
		(S3 (S4 *e*  *e* 0.4))
		"""

		fsaObj.parse(testStr)

		# "they" "can" "fish" => "PRO" "AUX" "NOUN" .7
		userInput = "\"they\" \"can\" \"fish\""

		# this is an array of TransitionStates => [ tranState1, tranState2... ]
		actualResult = fsaObj.returnHighestProb(userInput)
		expectedResult = "\"PRO\" \"AUX\" \"VERB\" *e* 0.096"
		self.assertTrue(expectedResult == actualResult, actualResult + " <-> " + expectedResult)


# old tests
class TransitionStateTests(unittest.TestCase):
	
	def test_ctor(self):
		tranState = transitionState.TransitionState('what', 'who', 'where', [])
		self.failIf(tranState == None)

	def test_canAccessProperties(self):
		fromState = 'A'
		toState = 'B'
		value = 'C'
		props = []

		tranState = transitionState.TransitionState(fromState, toState, value, props)
		self.failIf(tranState.fromState != fromState)
		self.failIf(tranState.toState != toState)
		self.failIf(tranState.value != value)
		self.failIf(tranState.props != props)

	def test_canAccessPropertiesArray(self):
		# (A (B C TestVal TestVal1))
		fromState = 'A'
		toState = 'B'
		value = 'C'
		props = [ 'TestVal', 'TestVal1']

		tranState = transitionState.TransitionState(fromState, toState, value, props)
		self.failIf(tranState.fromState != fromState)
		self.failIf(tranState.toState != toState)
		self.failIf(tranState.value != value)
		self.failIf(tranState.props != props)
		self.assertTrue(tranState.props[0] == 'TestVal')
		self.assertTrue(tranState.props[1] == 'TestVal1', 
			'we should have received TestVal2, received ' + tranState.props[1])

class UtilitiesTests(unittest.TestCase):

	def test_ctor(self):
		utils = utilities.Utilities()
		self.assertFalse(utils == None)

	def test_cleanseStringSingleApos(self):
		utils = utilities.Utilities()
		testVal = 'hello ''world'''
		expected = 'hello world'
		result = utils.cleanseInput(testVal)
		self.assertTrue(result, expected)

	def test_cleanseStringDoubleApos(self):
		utils = utilities.Utilities()
		testVal = 'hello "world"'
		expected = 'hello world'
		result = utils.cleanseInput(testVal)
		self.assertTrue(result, expected)

	def test_valsBeforeParen(self):
		utils = utilities.Utilities();
		testVal = 'what is this(something)'
		expected = ['what', 'is', 'this']
		result = utils.valsBeforeParen(testVal)
		self.assertTrue(result[0] == expected[0])
		self.assertTrue(result[1] == expected[1])
		self.assertTrue(result[2] == expected[2])

	def test_valsBeforeParenWithoutParen(self):
		utils = utilities.Utilities();
		testVal = 'what is this'
		expected = ['what', 'is', 'this']
		result = utils.valsBeforeParen(testVal)
		self.assertTrue(result[0] == expected[0])
		self.assertTrue(result[1] == expected[1])
		self.assertTrue(result[2] == expected[2])

	def test_valsBeforeParenMoreComplex(self):
		utils = utilities.Utilities();
		testVal = 'what is this(something to do'
		expected = ['what', 'is', 'this']
		result = utils.valsBeforeParen(testVal)
		self.assertTrue(result[0] == expected[0])
		self.assertTrue(result[1] == expected[1])
		self.assertTrue(result[2] == expected[2])

	def test_parenIndexExists(self):
		utils = utilities.Utilities();
		testVal = 'what is this(something to do)'
		result = utils.parenIndex(testVal)
		self.assertTrue(result['start'] == 13, 'got ' + str(result['start']))
		self.assertTrue(result['end'] == 28, 'got ' + str(result['start']))

	def test_parenIndexDoesNotExist(self):
		utils = utilities.Utilities();
		testVal = 'what is this(something to do'
		result = utils.parenIndex(testVal)
		self.assertTrue(result['start'] == -1, 'got ' + str(result['start']))
		self.assertTrue(result['end'] == -1, 'got ' + str(result['start']))

	def test_createTransitionState(self):
		utils = utilities.Utilities();
		testVal = '(F(Batman Joker What Is This))'
		result = utils.createTransitionState(testVal)
		self.assertTrue(result.fromState == 'F')
		self.assertTrue(result.toState == 'Batman')
		self.assertTrue(result.value == 'Joker')
		self.assertTrue(len(result.props) == 3)
		self.assertTrue(result.props[0] == 'What')
		self.assertTrue(result.props[1] == 'Is')
		self.assertTrue(result.props[2] == 'This')

# how do I want this represented?
# F
# (F (F 1))
# that means, if I'm given 1 I'm good
# maybe right now I can just simply represent them as objects
# for example 
# (F (F 1)) => { "F": {"F": 1 }}

class FsaTest(unittest.TestCase):

	def test_ctor(self):
		fsaObj = fsa.Fsa()
		self.assertTrue(fsaObj != None)

	def test_fsaGoodString(self):
		fsaObj = fsa.Fsa()
		testStr = """F
		(F (F 1))"""

		fsaObj.parse(testStr)
		
		self.assertTrue("F", fsaObj.endState)
		self.assertTrue(len(fsaObj.transitionStates) == 1)

		tranState = fsaObj.transitionStates[0];

		self.assertTrue(tranState.fromState == "F")
		self.assertTrue(tranState.toState == "F")
		self.assertTrue(tranState.value == "1")

	def test_fsaBetterString(self):
		fsaObj = fsa.Fsa()
		testStr = """F
		(R (T 1))
		(T (F 2))
		"""

		fsaObj.parse(testStr)
		
		self.assertTrue("F", fsaObj.endState)
		self.assertTrue(len(fsaObj.transitionStates) == 2)

		firstTranState = fsaObj.transitionStates[0];

		self.assertTrue(firstTranState.fromState == "R")
		self.assertTrue(firstTranState.toState == "T")
		self.assertTrue(firstTranState.value == "1")

		secondTranState = fsaObj.transitionStates[1];

		self.assertTrue(secondTranState.fromState == "T")
		self.assertTrue(secondTranState.toState == "F")
		self.assertTrue(secondTranState.value == "2")

	def test_fsaBestString(self):
		fsaObj = fsa.Fsa()
		testStr = """F
		(R (T 1))
		(T (F 2))
		(X (X 2))
		(X (C 3))
		(C (C 1))
		(G (G 22))
		(G (B 2))
		(B (F 21))
		"""

		fsaObj.parse(testStr)
		
		self.assertTrue("F", fsaObj.endState)
		self.assertTrue(len(fsaObj.transitionStates) == 8)

		firstTranState = fsaObj.transitionStates[0];

		self.assertTrue(firstTranState.fromState == "R")
		self.assertTrue(firstTranState.toState == "T")
		self.assertTrue(firstTranState.value == "1")

		secondTranState = fsaObj.transitionStates[1];

		self.assertTrue(secondTranState.fromState == "T")
		self.assertTrue(secondTranState.toState == "F")
		self.assertTrue(secondTranState.value == "2")

		thirdTranState = fsaObj.transitionStates[2];

		self.assertTrue(thirdTranState.fromState == "X")
		self.assertTrue(thirdTranState.toState == "X")
		self.assertTrue(thirdTranState.value == "2")

		fourthTranState = fsaObj.transitionStates[3];

		self.assertTrue(fourthTranState.fromState == "X")
		self.assertTrue(fourthTranState.toState == "C")
		self.assertTrue(fourthTranState.value == "3")

		fifthTranState = fsaObj.transitionStates[4];

		self.assertTrue(fifthTranState.fromState == "C")
		self.assertTrue(fifthTranState.toState == "C")
		self.assertTrue(fifthTranState.value == "1")

		sixTranState = fsaObj.transitionStates[5];

		self.assertTrue(sixTranState.fromState == "G")
		self.assertTrue(sixTranState.toState == "G")
		self.assertTrue(sixTranState.value == "22")

		seventhTranState = fsaObj.transitionStates[6];

		self.assertTrue(seventhTranState.fromState == "G")
		self.assertTrue(seventhTranState.toState == "B")
		self.assertTrue(seventhTranState.value == "2")

		eightTranState = fsaObj.transitionStates[7];

		self.assertTrue(eightTranState.fromState == "B")
		self.assertTrue(eightTranState.toState == "F")
		self.assertTrue(eightTranState.value == "21")

	def test_getPreviousTransitionSimple(self):
		fsaObj = fsa.Fsa()
		testStr = """A
		(A (A 'a'))"""

		fsaObj.parse(testStr)

		previousStates = fsaObj.getPreviousTransitions("A")

		self.assertTrue(len(previousStates) == 1)

		previousState = previousStates[0]
		self.assertTrue(previousState.fromState == 'A')
		self.assertTrue(previousState.toState == 'A')
		self.assertTrue(previousState.value == 'a', previousState.value)

	def test_getPreviousTransitionMoreComplex(self):
		fsaObj = fsa.Fsa()
		testStr = """C
		(A (B 'a'))
		(B (C 'z'))
		(A (C 'f'))
		"""

		fsaObj.parse(testStr)

		previousStates = fsaObj.getPreviousTransitions("C")

		self.assertTrue(len(previousStates) == 2)

		firstState = previousStates[0]
		self.assertTrue(firstState.fromState == 'B')
		self.assertTrue(firstState.toState == 'C')
		self.assertTrue(firstState.value == 'z', firstState.value)

		secondState = previousStates[1]
		self.assertTrue(secondState.fromState == 'A')
		self.assertTrue(secondState.toState == 'C')
		self.assertTrue(secondState.value == 'f', secondState.value)

	def test_processInputSimple(self):
		fsaObj = fsa.Fsa()
		testStr = """A
		(A (A 'a'))
		"""

		fsaObj.parse(testStr)

		userInput = "\"a\""

		res = fsaObj.processInput(userInput)

		self.assertTrue(res)

	def test_processInputSimple2Inputs(self):
		fsaObj = fsa.Fsa()
		testStr = """A
		(A (A 'a'))
		"""

		fsaObj.parse(testStr)

		userInput = "\"a\" \"a\""

		res = fsaObj.processInput(userInput)
		
		self.assertTrue(res)

	def test_processInputSimple3Inputs(self):
		fsaObj = fsa.Fsa()
		testStr = """A
		(A (A 'a'))
		"""

		fsaObj.parse(testStr)

		userInput = "\"a\" \"a\" \"a\""

		res = fsaObj.processInput(userInput)
		
		self.assertTrue(res)


	def test_processInputSimpleBadInput(self):
		fsaObj = fsa.Fsa()
		testStr = """A
		(A (A 'a'))
		"""

		fsaObj.parse(testStr)

		userInput = "\"a\" \"a\" \"b\""

		res = fsaObj.processInput(userInput)
		
		self.assertFalse(res)

	def test_processInputSimpleBadInputMiddle(self):
		fsaObj = fsa.Fsa()
		testStr = """A
		(A (A 'a'))
		"""

		fsaObj.parse(testStr)

		userInput = "\"a\" \"b\" \"a\""

		res = fsaObj.processInput(userInput)
		
		self.assertFalse(res)

	def test_processInputEpsilonTransition_a_a_b(self):
		fsaObj = fsa.Fsa()
		testStr = """3
(0 (1 \"a\"))
(0 (3 *e*))
(0 (2 \"b\"))
(1 (1 \"a\"))
(1 (2 \"b\"))
(1 (3 *e*))
(2 (2 \"b\"))
(2 (3 *e*))
		"""

		fsaObj.parse(testStr)

		userInput = "\"a\" \"a\" \"b\""

		res = fsaObj.processInput(userInput)
		
		self.assertTrue(res)

	def test_processInputFsa1_b(self):
		fsaObj = fsa.Fsa()
		testStr = """3
(0 (1 \"a\"))
(0 (3 *e*))
(0 (2 \"b\"))
(1 (1 \"a\"))
(1 (2 \"b\"))
(1 (3 *e*))
(2 (2 \"b\"))
(2 (3 *e*))
		"""

		fsaObj.parse(testStr)

		userInput = "\"b\""

		res = fsaObj.processInput(userInput)
		
		self.assertTrue(res)

	def test_processInputFsa1_a_c(self):
		fsaObj = fsa.Fsa()
		testStr = """3
(0 (1 \"a\"))
(0 (3 *e*))
(0 (2 \"b\"))
(1 (1 \"a\"))
(1 (2 \"b\"))
(1 (3 *e*))
(2 (2 \"b\"))
(2 (3 *e*))
		"""

		fsaObj.parse(testStr)

		userInput = "\"a\" \"c\""

		res = fsaObj.processInput(userInput)
		
		self.assertFalse(res)

	def test_processInputFsa4_a_c(self):
		fsaObj = fsa.Fsa()
		testStr = """3
(0 (1 \"a\"))
(1 (1 \"a\"))
(1 (2 \"b\"))
(1 (3 \"b\"))
(2 (2 \"b\"))
(2 (3 \"b\"))
"""

		fsaObj.parse(testStr)

		userInput = "\"a\" \"c\""

		res = fsaObj.processInput(userInput)
		
		self.assertFalse(res)