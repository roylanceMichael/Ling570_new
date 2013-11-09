import unittest
import utilities
import hiddenMarkov

class UtilitiesTest(unittest.TestCase):
    def test_createsBigramTuplesFromStr(self):
        testSent = "<s>/BOS John/N likes/V Mary/N </s>/EOS"

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
        testSent = "<s>/BOS John/N likes/V Mary/N </s>/EOS"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)

        self.assertTrue(4, len(result))

        self.assertTrue(result[0][0].pos == "BOS", result[0][0].pos)
        self.assertTrue(result[0][1].pos == "N")
        self.assertTrue(result[0][0].word == "<s>", result[0][0].pos)
        self.assertTrue(result[0][1].word == "John")

        self.assertTrue(result[1][0].pos == "N")
        self.assertTrue(result[1][1].pos == "V")
        self.assertTrue(result[1][0].pos == "John", result[0][0].pos)
        self.assertTrue(result[1][1].pos == "likes")

        self.assertTrue(result[2][0].pos == "V")
        self.assertTrue(result[2][1].pos == "N")
        self.assertTrue(result[2][0].pos == "likes", result[0][0].pos)
        self.assertTrue(result[2][1].pos == "Mary")

        self.assertTrue(result[3][0].pos == "N")
        self.assertTrue(result[3][1].pos == "EOS", result[3][1].pos)
        self.assertTrue(result[3][0].pos == "Mary", result[0][0].pos)
        self.assertTrue(result[3][1].pos == "</s>")

    def test_createsEmissionTuplesFromStr(self):
        testSent = "John/N likes/V Mary/N"

        utils = utilities.Utilities()

        result = utils.createEmissionTuplesFromStr(testSent)
        # print result

        self.assertTrue(4, len(result))

        #                self.assertTrue(result[0][0] == "BOS", result[0][0])
        #                self.assertTrue(result[0][1] == "<s>")

        self.assertTrue(result[0][0] == "N")
        self.assertTrue(result[0][1] == "John")

        self.assertTrue(result[1][0] == "V")
        self.assertTrue(result[1][1] == "likes")

        self.assertTrue(result[2][0] == "N")
        self.assertTrue(result[2][1] == "Mary", result[2][1])

        #                self.assertTrue(result[4][0] == "EOS")
        #                self.assertTrue(result[4][1] == "</s>", result[4][1])

    def test_makeBigDict(self):
        testtup = [['N', 'John'], ['V', 'likes'], ['N', 'Mary']]

        utils = utilities.Utilities()

        result = utils.EmissionDictFromStr(testtup)
        # print result

        self.assertTrue(result == {'EOS': {'</s>': 1}, 'V': {'likes': 1}, 'BOS': {'<s>': 1}, 'N': {'John': 1, 'Mary': 1}})

    def test_Prob(self):
        ### test not working
        testdict = {'EOS': {'</s>': 1}, 'V': {'likes': 1}, 'BOS': {'<s>': 1}, 'N': {'John': 1, 'Mary': 1}}

        utils = utilities.Utilities()

        result = utils.ProbsFromDict(testdict)
        # print result

#        self.assertTrue(result == {'EOS': {'</s>': 1}, 'V': {'likes': 1}, 'BOS': {'<s>': 1}, 'N': {'John': 1, 'Mary': 1}})
	self.assertTrue(1 == result)

class HiddenMarkovModelTest(unittest.TestCase):
    def test_dictReportingCorrectResultWithSingleBigram(self):
        hmm = hiddenMarkov.HiddenMarkov()

        hmm.addTransition("N", "V")

        result = hmm.getTransition("N", "V")

        self.assertTrue(1 == result, str(result))

    def test_addParsedLineResult(self):
        # arrange
        testSent = "<s>/BOS John/N likes/V Mary/N </s>/EOS"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)
        hmm = hiddenMarkov.HiddenMarkov()

        # act
        hmm.addParsedLine(result)

        # assert
        self.assertTrue(hmm.init_line_num() == 1)
        self.assertTrue(hmm.emiss_line_num() == 5)
        self.assertTrue(hmm.trans_line_num() == 4)
        self.assertTrue(hmm.state_num() == 3, str(hmm.state_num()))
        self.assertTrue(hmm.sym_num() == 5)

    def test_printOutFeature(self):
        # arrange
        testSent = "<s>/BOS John/N likes/V Mary/N </s>/EOS"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)
        hmm = hiddenMarkov.HiddenMarkov()
        hmm.addParsedLine(result)

        # act
        printStr = hmm.printHmmFormat()

        # assert
        self.assertTrue(printStr == '', printStr)
        

def main():
    unittest.main()

if __name__ == '__main__':
	main()
