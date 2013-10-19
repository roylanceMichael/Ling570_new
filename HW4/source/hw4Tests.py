import unittest
import transitionState
import utilities
import fsa

# homework 4 tests
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

def main():
	unittest.main()

if __name__ == '__main__':
	main()