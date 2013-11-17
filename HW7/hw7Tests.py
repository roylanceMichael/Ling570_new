import unittest
import utilities
import viterbi
import transition
import transitionHistory
import math

class ViterbiTest(unittest.TestCase):
    def test_moreComplexTransition(self):
        # arrange
        # He
        # hmm => tran => bos pn 1.0 emmiss => pn he 1.0
        # [ state { previousPos, currentPos, symbol, stateProbability } ]
        hmm = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     0.9 

\\transition
BOS N 0.5
BOS DT 0.5
N V 0.4
N D 0.5
V PN 1.0

\emission
DT  the 0.3
DT  a   0.7
N   a   .4
N   test .6
V   walk 1.0""".split("\n")

        vitTest = viterbi.Viterbi()
        for i in range(0, len(hmm)):
            line = hmm[i]
            vitTest.readInput(line)

        sentence = "a walk"

        # act
        result = vitTest.processLineForwards(sentence)

        # assert
        self.assertTrue(1 == len(result), str(len(result)))
        self.assertTrue(2 == len(result[0].transitions), len(result[0].transitions))

        self.assertTrue(True == result[0].representsSentence(sentence))

        # P(walk | V) * P(V | N) * P(a | N) * P(N | BOS)
        expectedProb = math.log10(1.0 * 0.4 * 0.4 * 0.5)
        self.assertTrue(expectedProb == result[0].getProbability())

        self.assertTrue("BOS" == result[0].transitions[0].previousPos)
        self.assertTrue("N" == result[0].transitions[0].currentPos)
        self.assertTrue("a" == result[0].transitions[0].symbol)
        self.assertTrue(0.2 == result[0].transitions[0].probability, str(result[0].transitions[0].probability))

        self.assertTrue("N" == result[0].transitions[1].previousPos)
        self.assertTrue("V" == result[0].transitions[1].currentPos)
        self.assertTrue("walk" == result[0].transitions[1].symbol)
        self.assertTrue(0.4 == result[0].transitions[1].probability)

        bestPath = vitTest.reportBestPath(result)
        self.assertTrue("BOS N V -1.09691001301" == bestPath, bestPath)

    def test_slightlyMoreComplexTransition(self):
        # arrange
        # He
        # hmm => tran => bos pn 1.0 emmiss => pn he 1.0
        # [ state { previousPos, currentPos, symbol, stateProbability } ]
        hmm = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     0.9 

\\transition
BOS N 1.0
N V 0.4
N D 0.5
V PN 1.0

\emission
DT  the 0.3
DT  a   0.7
N   a   .4
N   test .6
V   walk 1.0""".split("\n")

        # a\N walk\V
        # P(walk | V) == 1.0 && P(V | N) == .4

        vitTest = viterbi.Viterbi()
        for i in range(0, len(hmm)):
            line = hmm[i]
            vitTest.readInput(line)

        # act
        result = vitTest.processLineForwards("a walk")

        # assert
        # [ state { previousPos: BOS, currentPos: N, symbol: a, stateProbability: 1.0 } ]
        self.assertTrue(1 == len(result))
        self.assertTrue(2 == len(result[0].transitions))

        self.assertTrue("BOS" == result[0].transitions[0].previousPos)
        self.assertTrue("N" == result[0].transitions[0].currentPos)
        self.assertTrue("a" == result[0].transitions[0].symbol)
        self.assertTrue(0.4 == result[0].transitions[0].probability)

        self.assertTrue("N" == result[0].transitions[1].previousPos)
        self.assertTrue("V" == result[0].transitions[1].currentPos)
        self.assertTrue("walk" == result[0].transitions[1].symbol)
        self.assertTrue(0.4 == result[0].transitions[1].probability)

class TransitionHistoryTests(unittest.TestCase):
    def test_canAddTransition(self):
        # arrange
        tranHis = transitionHistory.TransitionHistory()
        tran = transition.Transition("N", "V", "T", 0.5)
        newTran = transition.Transition("PN", "N", "He", 0.2)
        tranHis.addTransition(tran)

        # act
        res = tranHis.canAddTransition(newTran)

        # assert
        self.assertTrue(res == True, str(res))

    def test_cannotAddTransition(self):
        # arrange
        tranHis = transitionHistory.TransitionHistory()
        tran = transition.Transition("N", "V", "T", 0.5)
        newTran = transition.Transition("R", "PN", "He", 0.2)
        tranHis.addTransition(tran)

        # act
        res = tranHis.canAddTransition(newTran)

        # assert
        self.assertTrue(res == False)

    def test_addsTransition(self):
        # arrange
        tranHis = transitionHistory.TransitionHistory()
        tran = transition.Transition("N", "V", "T", 0.5)

        # act
        tranHis.addTransition(tran)

        # assert
        self.assertTrue(len(tranHis.transitions) == 1)

    def test_getsLastTransition(self):
        # arrange
        tranHis = transitionHistory.TransitionHistory()
        tran = transition.Transition("N", "V", "T", 0.5)

        # act
        tranHis.addTransition(tran)

        # assert
        self.assertTrue(len(tranHis.transitions) == 1)

def main():
    unittest.main()

if __name__ == '__main__':
        main()
                       
