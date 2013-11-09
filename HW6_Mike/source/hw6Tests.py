import unittest
import utilities
import hiddenMarkov

class UtilitiesTest(unittest.TestCase):
    def test_createsBigramTuplesFromStr(self):
        testSent = "John/N likes/V Mary/N"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)

        self.assertTrue(4, len(result))

        self.assertTrue(result[0][0].pos == "BOS", result[0][0].pos)
        self.assertTrue(result[0][1].pos == "N")

        self.assertTrue(result[1][0].pos == "N")
        self.assertTrue(result[1][1].pos == "V")

        self.assertTrue(result[2][0].pos == "V")
        self.assertTrue(result[2][1].pos == "N")

        self.assertTrue(result[3][0].pos == "N")
        self.assertTrue(result[3][1].pos == "EOS", result[3][1].pos)

    def test_createsBigramTuplesEmissionsFromStr(self):
        testSent = "John/N likes/V Mary/N"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)

        self.assertTrue(4, len(result))

        self.assertTrue(result[0][0].pos == "BOS", result[0][0].pos)
        self.assertTrue(result[0][1].pos == "N")
        self.assertTrue(result[0][0].word == "<s>", result[0][0].pos)
        self.assertTrue(result[0][1].word == "John")

        self.assertTrue(result[1][0].pos == "N")
        self.assertTrue(result[1][1].pos == "V")
        self.assertTrue(result[1][0].word == "John", result[0][0].pos)
        self.assertTrue(result[1][1].word == "likes")

        self.assertTrue(result[2][0].pos == "V")
        self.assertTrue(result[2][1].pos == "N")
        self.assertTrue(result[2][0].word == "likes", result[0][0].pos)
        self.assertTrue(result[2][1].word == "Mary")

        self.assertTrue(result[3][0].pos == "N")
        self.assertTrue(result[3][1].pos == "EOS", result[3][1].pos)
        self.assertTrue(result[3][0].word == "Mary", result[0][0].pos)
        self.assertTrue(result[3][1].word == "</s>")


class HiddenMarkovModelTest(unittest.TestCase):
    def test_firstSentence(self):
        # arrange
        utils = utilities.Utilities()
        sentence1 = utils.createBigramTuplesFromStr("Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ ,/, will/MD join/VB the/DT board/NN as/IN a/DT nonexecutive/JJ director/NN Nov./NNP 29/CD ./.")

        hmm = hiddenMarkov.HiddenMarkov()

        # act
        hmm.addParsedLine(sentence1)

        # assert 
        # print hmm.printHmmFormat()
        nnpNovProb = hmm.getEmissionProbability("NNP", "Nov.")
        self.assertTrue(nnpNovProb == float(1) / 3)

        nnpCdProb = hmm.getTransitionProbability("NNP", "CD")
        self.assertTrue(nnpCdProb == float(1) / 3)

    def test_firstThreeSentences(self):
        # arrange
        utils = utilities.Utilities()

        sentence1 = utils.createBigramTuplesFromStr("Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ ,/, will/MD join/VB the/DT board/NN as/IN a/DT nonexecutive/JJ director/NN Nov./NNP 29/CD ./.")
        sentence2 = utils.createBigramTuplesFromStr("Mr./NNP Vinken/NNP is/VBZ chairman/NN of/IN Elsevier/NNP N.V./NNP ,/, the/DT Dutch/NNP publishing/VBG group/NN ./.")
        sentence3 = utils.createBigramTuplesFromStr("Rudolph/NNP Agnew/NNP ,/, 55/CD years/NNS old/JJ and/CC former/JJ chairman/NN of/IN Consolidated/NNP Gold/NNP Fields/NNP PLC/NNP ,/, was/VBD named/VBN a/DT nonexecutive/JJ director/NN of/IN this/DT British/JJ industrial/JJ conglomerate/NN ./.")   

        hmm = hiddenMarkov.HiddenMarkov()
        
        # act
        hmm.addParsedLine(sentence1)
        hmm.addParsedLine(sentence2)
        hmm.addParsedLine(sentence3)

        # assert emissions
        # print hmm.printHmmFormat()

        nnpDict = hmm.getEmissions("NNP")
        inDict = hmm.getEmissions("IN")

        nnpTotal = hmm.getDictTotal(nnpDict)
        inTotal = hmm.getDictTotal(inDict)

        self.assertTrue(nnpTotal == 14, str(nnpTotal))
        self.assertTrue(inTotal == 4, str(inTotal))

        # assert transitions


    def test_dictReportingCorrectResultWithSingleBigram(self):
        hmm = hiddenMarkov.HiddenMarkov()

        hmm.addTransition("N", "V")

        result = hmm.getTransition("V", "N")

        self.assertTrue(1 == result, str(result))

    def test_addParsedLineResult(self):
        # arrange
        testSent = "John/N likes/V Mary/N"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)
        hmm = hiddenMarkov.HiddenMarkov()

        # act
        hmm.addParsedLine(result)

        # assert
        self.assertTrue(hmm.init_line_num() == 1)
        self.assertTrue(hmm.emiss_line_num() == 3)
        self.assertTrue(hmm.trans_line_num() == 3)
        self.assertTrue(hmm.state_num() == 3, str(hmm.state_num()))
        self.assertTrue(hmm.sym_num() == 2)

    def test_printOutFeature(self):
        # arrange
        testSent = "John/N likes/V Mary/N"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)
        hmm = hiddenMarkov.HiddenMarkov()
        hmm.addParsedLine(result)

        # act
        printStr = hmm.printHmmFormat()

        # assert
        expectedResult = """state_num=3
sym_num=2
init_line_num=1
trans_line_num=3
emiss_line_num=3
\init
BOS\t1.0

\\transition
V\tN\t1.0
BOS\tN\t1.0
N\tV\t1.0

\emissions
V\tlikes\t1.0
N\tJohn\t0.5
N\tMary\t0.5
"""
        self.assertTrue(str(len(printStr)) == str(len(expectedResult)), str(len(printStr)) + "-" + str(len(expectedResult)))



def main():
    unittest.main()

if __name__ == '__main__':
	main()
