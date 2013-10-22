import unittest
import transitionState
import utilities
import fsa
import trie

# homework 4 tests
class ExpandedFsmTest(unittest.TestCase): 
	def test_readInFsmAndThenLexiconValue3(self):
		utils = utilities.Utilities()
		testStr = """walk       reg_verb_stem
		cut        irreg_verb_stem
		s          3sg"""

		lexiconVals = utils.readLexicon(testStr)

		fsaStr = """q3
(q0 (q1 reg_verb_stem))
(q0 (q3 irreg_verb_stem))
(q1 (q3 3sg))"""

		fsaObj = fsa.Fsa()
		fsaObj.parse(fsaStr)

		# fsaObj.transitionStates:
		# from: q0 to: q3 value:reg_verb_stem

		fsaObj.parseLexicon(lexiconVals)

		# startState: q0 endState: q3
		# from: q0 to: st1 value: w
		# from: st1 to: st2 value: a
		# from: st2 to: st3 value: l
		# from: st3 to: q3 value: k

		tranStates = fsaObj.expandedTransitionStates
		self.assertTrue(len(tranStates) == 8, 'actual val was ' + str(len(tranStates)))

		firstTranState = tranStates[0]
		self.assertTrue(firstTranState.fromState == "q1")
		self.assertTrue(firstTranState.toState == "q3")
		self.assertTrue(firstTranState.value == "s")

		fifthTranState = tranStates[1]
		self.assertTrue(fifthTranState.fromState == "q0")
		self.assertTrue(fifthTranState.toState == "st1")
		self.assertTrue(fifthTranState.value == "w")

		secondTranState = tranStates[2]
		self.assertTrue(secondTranState.fromState == "st1")
		self.assertTrue(secondTranState.toState == "st2")
		self.assertTrue(secondTranState.value == "a")

		thirdTranState = tranStates[3]
		self.assertTrue(thirdTranState.fromState == "st2")
		self.assertTrue(thirdTranState.toState == "st3")
		self.assertTrue(thirdTranState.value == "l")

		fourthTranState = tranStates[4]
		self.assertTrue(fourthTranState.fromState == "st3")
		self.assertTrue(fourthTranState.toState == "q3")
		self.assertTrue(fourthTranState.value == "k")

		sixthTranState = tranStates[5]
		self.assertTrue(sixthTranState.fromState == "q0")
		self.assertTrue(sixthTranState.toState == "st4")
		self.assertTrue(sixthTranState.value == "c")

		seventhTranState = tranStates[6]
		self.assertTrue(seventhTranState.fromState == "st4")
		self.assertTrue(seventhTranState.toState == "st5")
		self.assertTrue(seventhTranState.value == "u")

		eightTranState = tranStates[7]
		self.assertTrue(eightTranState.fromState == "st5")
		self.assertTrue(eightTranState.toState == "q3")
		self.assertTrue(eightTranState.value == "t")

	def test_readInFsmAndThenLexiconValue(self):
		utils = utilities.Utilities()
		testStr = """walk       reg_verb_stem"""

		lexiconVals = utils.readLexicon(testStr)

		fsaStr = """q3
(q0 (q3 reg_verb_stem))"""

		fsaObj = fsa.Fsa()
		fsaObj.parse(fsaStr)

		# fsaObj.transitionStates:
		# from: q0 to: q3 value:reg_verb_stem

		fsaObj.parseLexicon(lexiconVals)

		# startState: q0 endState: q3
		# from: q0 to: st1 value: w
		# from: st1 to: st2 value: a
		# from: st2 to: st3 value: l
		# from: st3 to: q3 value: k

		tranStates = fsaObj.expandedTransitionStates
		self.assertTrue(len(tranStates) == 4, 'actual val was ' + str(len(tranStates)))

		firstTranState = tranStates[0]
		self.assertTrue(firstTranState.fromState == "q0")
		self.assertTrue(firstTranState.toState == "st1")
		self.assertTrue(firstTranState.value == "w")

		secondTranState = tranStates[1]
		self.assertTrue(secondTranState.fromState == "st1")
		self.assertTrue(secondTranState.toState == "st2")
		self.assertTrue(secondTranState.value == "a")

		thirdTranState = tranStates[2]
		self.assertTrue(thirdTranState.fromState == "st2")
		self.assertTrue(thirdTranState.toState == "st3")
		self.assertTrue(thirdTranState.value == "l")

		fourthTranState = tranStates[3]
		self.assertTrue(fourthTranState.fromState == "st3")
		self.assertTrue(fourthTranState.toState == "q3")
		self.assertTrue(fourthTranState.value == "k")

	def test_readInFsmAndThenLexiconValue1(self):
		utils = utilities.Utilities()
		testStr = """walk       reg_verb_stem
		was	reg_verb_stem"""

		lexiconVals = utils.readLexicon(testStr)

		fsaStr = """q3
(q0 (q3 reg_verb_stem))"""

		fsaObj = fsa.Fsa()
		fsaObj.parse(fsaStr)

		# fsaObj.transitionStates:
		# from: q0 to: q3 value:reg_verb_stem

		fsaObj.parseLexicon(lexiconVals)

		# startState: q0 endState: q3
		# from: q0 to: st1 value: w
		# from: st1 to: st2 value: a
		# from: st2 to: st3 value: l
		# from: st3 to: q3 value: k

		tranStates = fsaObj.expandedTransitionStates
		self.assertTrue(len(tranStates) == 5, 'actual val was ' + str(len(tranStates)))

		firstTranState = tranStates[0]
		self.assertTrue(firstTranState.fromState == "q0")
		self.assertTrue(firstTranState.toState == "st1")
		self.assertTrue(firstTranState.value == "w")

		secondTranState = tranStates[1]
		self.assertTrue(secondTranState.fromState == "st1")
		self.assertTrue(secondTranState.toState == "st2")
		self.assertTrue(secondTranState.value == "a")

		thirdTranState = tranStates[2]
		self.assertTrue(thirdTranState.fromState == "st2")
		self.assertTrue(thirdTranState.toState == "st3")
		self.assertTrue(thirdTranState.value == "l")

		fourthTranState = tranStates[3]
		self.assertTrue(fourthTranState.fromState == "st3")
		self.assertTrue(fourthTranState.toState == "q3")
		self.assertTrue(fourthTranState.value == "k")

		fifthTranState = tranStates[4]
		self.assertTrue(fifthTranState.fromState == "st3")
		self.assertTrue(fifthTranState.toState == "q3")
		self.assertTrue(fifthTranState.value == "s")

	def test_readInFsmAndThenLexiconValue2(self):
		utils = utilities.Utilities()
		testStr = """walk       reg_verb_stem
		s          3sg"""

		lexiconVals = utils.readLexicon(testStr)

		fsaStr = """q3
(q0 (q1 reg_verb_stem))
(q1 (q3 3sg))"""

		fsaObj = fsa.Fsa()
		fsaObj.parse(fsaStr)

		# fsaObj.transitionStates:
		# from: q0 to: q3 value:reg_verb_stem

		fsaObj.parseLexicon(lexiconVals)

		# startState: q0 endState: q3
		# from: q0 to: st1 value: w
		# from: st1 to: st2 value: a
		# from: st2 to: st3 value: l
		# from: st3 to: q3 value: k

		tranStates = fsaObj.expandedTransitionStates
		self.assertTrue(len(tranStates) == 5, 'actual val was ' + str(len(tranStates)))

		firstTranState = tranStates[0]
		self.assertTrue(firstTranState.fromState == "q1")
		self.assertTrue(firstTranState.toState == "q3")
		self.assertTrue(firstTranState.value == "s")

		fifthTranState = tranStates[1]
		self.assertTrue(fifthTranState.fromState == "q0")
		self.assertTrue(fifthTranState.toState == "st1")
		self.assertTrue(fifthTranState.value == "w")

		secondTranState = tranStates[2]
		self.assertTrue(secondTranState.fromState == "st1")
		self.assertTrue(secondTranState.toState == "st2")
		self.assertTrue(secondTranState.value == "a")

		thirdTranState = tranStates[3]
		self.assertTrue(thirdTranState.fromState == "st2")
		self.assertTrue(thirdTranState.toState == "st3")
		self.assertTrue(thirdTranState.value == "l")

		fourthTranState = tranStates[4]
		self.assertTrue(fourthTranState.fromState == "st3")
		self.assertTrue(fourthTranState.toState == "q3")
		self.assertTrue(fourthTranState.value == "k")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
