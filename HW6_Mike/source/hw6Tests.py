import unittest
import utilities
import hiddenMarkov

class UtilitiesTest(unittest.TestCase):
    def test_createsBigramTuplesFromStr(self):
        testSent = "<s>/BOS John/N likes/V Mary/N </s>/EOS"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)

        self.assertTrue(4, len(result))

        self.assertTrue(result[0][0] == "BOS", result[0][0])
        self.assertTrue(result[0][1] == "N")

        self.assertTrue(result[1][0] == "N")
        self.assertTrue(result[1][1] == "V")

        self.assertTrue(result[2][0] == "V")
        self.assertTrue(result[2][1] == "N")

        self.assertTrue(result[3][0] == "N")
        self.assertTrue(result[3][1] == "EOS", result[3][1])

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

class NgramDictionaryTest(unittest.TestCase):
    def test_dictReportingCorrectResultWithSingleBigram(self):
        hmm = hiddenMarkov.HiddenMarkov()

        hmm.addTransition("N", "V")

        result = hmm.getTransition("N", "V")

        self.assertTrue(1 == result, str(result))

def main():
    unittest.main()

if __name__ == '__main__':
	main()
