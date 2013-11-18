import unittest
import utilities
import viterbi
import transition
import transitionHistory
import math

class ViterbiTest(unittest.TestCase):
    def test_singleWordTransition(self):
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

        sentence = "a"

        # act
        result = vitTest.processLine(sentence)

        # assert
        expectedProbability = math.log10(.7) + math.log10(.5)
        self.assertTrue(result[0] == expectedProbability, str(expectedProbability) + " " + str(result[0]))
        self.assertTrue(result[1] == ['BOS', 'DT'])

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
        result = vitTest.processLine(sentence)

        # assert
        expectedProbability = math.log10(.4) + math.log10(.5) + math.log10(.4)
        self.assertTrue(result[0] == expectedProbability)
        self.assertTrue(result[1] == ['BOS', 'N', 'V'])

    def test_missingWordTransition(self):
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

        sentence = "far walk"

        # act
        result = vitTest.processLine(sentence)

        # assert
        expectedProb = math.log10(.15) + math.log10(.5) + math.log10(.4)
        self.assertTrue(expectedProb == result[0])
        self.assertTrue(["BOS", "N", "V"] == result[1])

    def test_missingWordTransitionMiddle(self):
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
DT N .6
DT V .4

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

        sentence = "the force"

        # act
        result = vitTest.processLine(sentence)

        # assert
        expectedProb = math.log10(.3) + math.log10(.5) + math.log10(.15) + math.log10(.4)
        self.assertTrue(str(expectedProb) == str(result[0]), str(expectedProb) + " " + str(result[0]))
        self.assertTrue(["BOS", "DT", "V"] == result[1])  

def main():
    unittest.main()

if __name__ == '__main__':
        main()
                       
