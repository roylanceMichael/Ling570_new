import unittest
import transitionState
import utilities
import fsa
import trie

# homework 4 tests
class ExpandedFsmTest(unittest.TestCase): 
	def test_readInSingleLexiconValueAndBuildTransitionState(self):
		utils = utilities.Utilities()
		testStr = """walk       reg_verb_stem"""

		lexicon = utils.readLexicon(testStr)

		fsaObj = fsa.Fsa()

		fsaObj.parseLexicon(lexicon)

		transitionStates = fsaObj.transitionStates

		self.assertTrue(len(transitionStates) == 4)
		
		self.assertTrue(fsaObj.startState == "q0")
		self.assertTrue(fsaObj.endState == "q1")

		self.assertTrue(transitionStates[0].fromState == "q0")
		self.assertTrue(transitionStates[0].toState == "st1")
		self.assertTrue(transitionStates[0].value == "w")

		self.assertTrue(transitionStates[1].fromState == "st1", transitionStates[1].fromState + " " + transitionStates[1].toState)
		self.assertTrue(transitionStates[1].toState == "st2")
		self.assertTrue(transitionStates[1].value == "a")

		self.assertTrue(transitionStates[2].fromState == "st2")
		self.assertTrue(transitionStates[2].toState == "st3")
		self.assertTrue(transitionStates[2].value == "l")

		self.assertTrue(transitionStates[3].fromState == "st3")
		self.assertTrue(transitionStates[3].toState == "q1")
		self.assertTrue(transitionStates[3].value == "k")

	def test_readInSingleLexiconValueAndBuildTransitionState(self):
		utils = utilities.Utilities()
		testStr = """sing       reg_verb_stem
		sang	past_tense
		spoke	reg_verb_stem"""

		lexicon = utils.readLexicon(testStr)

		fsaObj = fsa.Fsa()

		fsaObj.parseLexicon(lexicon)

		transitionStates = fsaObj.transitionStates

		self.assertTrue(len(transitionStates) == 11, str(len(transitionStates)))

		self.assertTrue(fsaObj.startState == "q0")
		self.assertTrue(fsaObj.endState == "q1")

		# from: q0 to: st1 value: s
		# from: st1 to: st2 value: i
		# from: st2 to: st3 value: n
		# from: st3 to: q1 value: g
		# from: st1 to: st4 value: p
		# from: st4 to: st5 value: o
		# from: st5 to: st6 value: k
		# from: st6 to: q1 value: e
		# from: st1 to: st7 value: a
		# from: st7 to: st8 value: n
		# from: st8 to: q1 value: g

		self.assertTrue(transitionStates[0].fromState == "q0")
		self.assertTrue(transitionStates[0].toState == "st1")
		self.assertTrue(transitionStates[0].value == "s")

		self.assertTrue(transitionStates[1].fromState == "st1")
		self.assertTrue(transitionStates[1].toState == "st2")
		self.assertTrue(transitionStates[1].value == "i")

		self.assertTrue(transitionStates[2].fromState == "st2")
		self.assertTrue(transitionStates[2].toState == "st3")
		self.assertTrue(transitionStates[2].value == "n")

		self.assertTrue(transitionStates[3].fromState == "st3")
		self.assertTrue(transitionStates[3].toState == "q1")
		self.assertTrue(transitionStates[3].value == "g")

		self.assertTrue(transitionStates[4].fromState == "st1")
		self.assertTrue(transitionStates[4].toState == "st4")
		self.assertTrue(transitionStates[4].value == "p")

		self.assertTrue(transitionStates[5].fromState == "st4")
		self.assertTrue(transitionStates[5].toState == "st5")
		self.assertTrue(transitionStates[5].value == "o")

		self.assertTrue(transitionStates[6].fromState == "st5")
		self.assertTrue(transitionStates[6].toState == "st6")
		self.assertTrue(transitionStates[6].value == "k")

		self.assertTrue(transitionStates[7].fromState == "st6")
		self.assertTrue(transitionStates[7].toState == "q1")
		self.assertTrue(transitionStates[7].value == "e")

		self.assertTrue(transitionStates[8].fromState == "st1")
		self.assertTrue(transitionStates[8].toState == "st7")
		self.assertTrue(transitionStates[8].value == "a")

		self.assertTrue(transitionStates[9].fromState == "st7")
		self.assertTrue(transitionStates[9].toState == "st8")
		self.assertTrue(transitionStates[9].value == "n")

		self.assertTrue(transitionStates[10].fromState == "st8")
		self.assertTrue(transitionStates[10].toState == "q1")
		self.assertTrue(transitionStates[10].value == "g")

	def test_readInSingleLexiconValueAndBuildTransitionState(self):
		utils = utilities.Utilities()
		testStr = """geese	testing
		fox       reg_verb_stem
		cat 	past_tense
		goose	reg_verb_stem
		"""

		lexicon = utils.readLexicon(testStr)

		fsaObj = fsa.Fsa()

		fsaObj.parseLexicon(lexicon)

		transitionStates = fsaObj.transitionStates

		for i in range(0, len(transitionStates)):
			tranState = transitionStates[i]

			print 'from:' + tranState.fromState + ' to:' + tranState.toState + ' value:' + tranState.value 

		self.assertTrue(len(transitionStates) == 11, str(len(transitionStates)))

		self.assertTrue(fsaObj.startState == "q0")
		self.assertTrue(fsaObj.endState == "q1")

		# from: q0 to: st1 value: f
		# from: st1 to: st2 value: o
		# from: st2 to: q1 value: x
		# from: q0 to: st3 value: g
		# from: st3 to: st4 value: o
		# from: st4 to: st5 value: o
		# from: st5 to: st6 value: s
		# from: st6 to: q1 value: e
		# from: q0 to: st7 value: c
		# from: st7 to: st8 value: a
		# from: st8 to: q1 value: t

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





def main():
	unittest.main()

if __name__ == '__main__':
	main()
