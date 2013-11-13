import unittest
import utilities
import hiddenMarkovFactory
import hiddenMarkovBigram
import hiddenMarkovTrigram

utils = utilities.Utilities()
unknownProbFile = utils.createUnkProbDict("""NNP 0.378926539698244
NN 0.158602620087336
JJ 0.263349514563107
CD 0.313821138211382
NNS 0.220447284345048
VBN 0.228235294117647
VB 0.196337741607325
VBD 0.112023460410557
VBG 0.316326530612245
RB 0.0856269113149847
VBZ 0.099290780141844
VBP 0.0645161290322581
IN 0.00422255340288127
JJR 0.0833333333333333
JJS 0.114942528735632
PRP$ 0.0173611111111111
UH 1
RP 0.0234375
MD 0.00872093023255814
PRP 0.00490196078431373
WDT 0.0165745856353591
CC 0.002
WRB 0.0227272727272727
FW 1
RBS 0.0526315789473684
NNPS 1""")

class HiddenMarkovFactoryTest(unittest.TestCase):
    def test_addFirstSixLinesToDictionary(self):
        # arrange
        hmmInput = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11""".split("\n")
        
        hmmFactory = hiddenMarkovFactory.HiddenMarkovFactory()

        # act
        hmmFactory.readInput(hmmInput[0])
        hmmFactory.readInput(hmmInput[1])
        hmmFactory.readInput(hmmInput[2])
        hmmFactory.readInput(hmmInput[3])
        hmmFactory.readInput(hmmInput[4])

        # assert
        self.assertTrue(hmmFactory.current_state_num == 6, str(hmmFactory.current_state_num))
        self.assertTrue(hmmFactory.current_sym_num == 11)
        self.assertTrue(hmmFactory.current_init_line == 2)
        self.assertTrue(hmmFactory.current_trans_line_num == 13)
        self.assertTrue(hmmFactory.current_emiss_line_num == 11)

    def test_addInitToDictionary(self):
        # arrange
        hmmInput = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     1.0 """.split("\n")
        
        hmmFactory = hiddenMarkovFactory.HiddenMarkovFactory()

        # act
        hmmFactory.readInput(hmmInput[0])
        hmmFactory.readInput(hmmInput[1])
        hmmFactory.readInput(hmmInput[2])
        hmmFactory.readInput(hmmInput[3])
        hmmFactory.readInput(hmmInput[4])
        hmmFactory.readInput(hmmInput[5])
        hmmFactory.readInput(hmmInput[6])
        hmmFactory.readInput(hmmInput[7])

        # assert
        self.assertTrue(hmmFactory.current_init_dict["BOS"] == 1.0)

    def test_movesToTrans(self):
        # arrange
        hmmInput = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     1.0 

\\transition""".split("\n")
        
        hmmFactory = hiddenMarkovFactory.HiddenMarkovFactory()

        # act
        hmmFactory.readInput(hmmInput[0])
        hmmFactory.readInput(hmmInput[1])
        hmmFactory.readInput(hmmInput[2])
        hmmFactory.readInput(hmmInput[3])
        hmmFactory.readInput(hmmInput[4])
        hmmFactory.readInput(hmmInput[5])
        hmmFactory.readInput(hmmInput[6])
        hmmFactory.readInput(hmmInput[7])
        hmmFactory.readInput(hmmInput[8])
        hmmFactory.readInput(hmmInput[9])

        # assert
        self.assertTrue(hmmFactory.currentState == hmmFactory.trans_state, hmmFactory.currentState)

    def test_movesToTransVals(self):
        # arrange
        hmmInput = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     1.0 

\\transition
N V 0.5
N D 0.5""".split("\n")
        
        hmmFactory = hiddenMarkovFactory.HiddenMarkovFactory()

        # act
        hmmFactory.readInput(hmmInput[0])
        hmmFactory.readInput(hmmInput[1])
        hmmFactory.readInput(hmmInput[2])
        hmmFactory.readInput(hmmInput[3])
        hmmFactory.readInput(hmmInput[4])
        hmmFactory.readInput(hmmInput[5])
        hmmFactory.readInput(hmmInput[6])
        hmmFactory.readInput(hmmInput[7])
        hmmFactory.readInput(hmmInput[8])
        hmmFactory.readInput(hmmInput[9])
        hmmFactory.readInput(hmmInput[10])
        hmmFactory.readInput(hmmInput[11])

        # assert
        self.assertTrue(hmmFactory.currentState == hmmFactory.trans_state, hmmFactory.currentState)
        self.assertTrue(hmmFactory.current_trans_dict["N"]["V"] == 0.5)
        self.assertTrue(hmmFactory.current_trans_dict["N"]["D"] == 0.5)

    def test_movesToEmissVals1(self):
        # arrange
        hmmInput = """state_num=6
sym_num=11
init_line_num=2
trans_line_num=13
emiss_line_num=11

\init
BOS     1.0 

\\transition
N V 0.5
N D 0.5

\emission
DT  the 0.7
DT  a   0.3
N   a   1.0""".split("\n")
        
        hmmFactory = hiddenMarkovFactory.HiddenMarkovFactory()

        # act
        hmmFactory.readInput(hmmInput[0])
        hmmFactory.readInput(hmmInput[1])
        hmmFactory.readInput(hmmInput[2])
        hmmFactory.readInput(hmmInput[3])
        hmmFactory.readInput(hmmInput[4])
        hmmFactory.readInput(hmmInput[5])
        hmmFactory.readInput(hmmInput[6])
        hmmFactory.readInput(hmmInput[7])
        hmmFactory.readInput(hmmInput[8])
        hmmFactory.readInput(hmmInput[9])
        hmmFactory.readInput(hmmInput[10])
        hmmFactory.readInput(hmmInput[11])
        hmmFactory.readInput(hmmInput[12])
        hmmFactory.readInput(hmmInput[13])
        hmmFactory.readInput(hmmInput[14])
        hmmFactory.readInput(hmmInput[15])
        hmmFactory.readInput(hmmInput[16])

        # assert
        self.assertTrue(hmmFactory.currentState == hmmFactory.emiss_state, hmmFactory.currentState)
        self.assertTrue(hmmFactory.current_emiss_dict["DT"]["the"] == 0.7)
        self.assertTrue(hmmFactory.current_emiss_dict["DT"]["a"] == 0.3)
        self.assertTrue(hmmFactory.getActualInitLineNum() == 1)
        self.assertTrue(hmmFactory.getActualTransLineNum() == 2)
        self.assertTrue(hmmFactory.getActualEmissLineNum() == 3, str(hmmFactory.getActualEmissLineNum()))
        self.assertTrue(hmmFactory.getActualStateNum() == 1)
        self.assertTrue(hmmFactory.getActualSymNum() == 2)

        print hmmFactory.reportLineNumberDifference()

class UtilitiesTest(unittest.TestCase):
    def test_createsUnkDict(self):
        # arrange
        testStr = """
        NNP 0.555
        TR 0.222
        """
        utils = utilities.Utilities()

        # act
        testDict = utils.createUnkProbDict(testStr)

        # assert
        self.assertTrue(testDict["NNP"] == 0.555)
        self.assertTrue(testDict["TR"] == 0.222)


    def test_createsTrigramTuplesFromStr(self):
        testSent = "John/N likes/V Mary/N"

        utils = utilities.Utilities()

        result = utils.createTrigramTuplesFromStr(testSent)

        self.assertTrue(2, len(result))

        self.assertTrue(result[0][0].pos == "BOS", result[0][0].pos)
        self.assertTrue(result[0][1].pos == "N")
        self.assertTrue(result[0][2].pos == "V")

        self.assertTrue(result[1][0].pos == "N")
        self.assertTrue(result[1][1].pos == "V")
        self.assertTrue(result[1][2].pos == "N")

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

class HiddenMarkovTrigramModelTest(unittest.TestCase):
    def test_unigramsExistWithCorrectProbabilities(self):
        # arrange
        utils = utilities.Utilities()
        rawSent = "Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ"
        sentence = utils.createTrigramTuplesFromStr(rawSent)

        hmm = hiddenMarkovTrigram.HiddenMarkovTrigram({})

        # act
        hmm.addParsedLine(sentence)

        # assert - make sure that items exist in the proper dictionaries
        self.assertTrue(hmm.unigramTransitionDictionary["NNP"] == 2)
        self.assertTrue(hmm.unigramTransitionDictionary[","] == 1)
        self.assertTrue(hmm.unigramTransitionDictionary["CD"] == 1)
        self.assertTrue(hmm.unigramTransitionDictionary["NNS"] == 1)
        self.assertTrue(hmm.unigramTransitionDictionary["JJ"] == 1)

        self.assertTrue(hmm.getUnigramProb("NNP") == 2 / float(7))
        self.assertTrue(hmm.getUnigramProb(",") == 1 / float(7))
        self.assertTrue(hmm.getUnigramProb("CD") == 1 / float(7))
        self.assertTrue(hmm.getUnigramProb("NNS") == 1 / float(7))
        self.assertTrue(hmm.getUnigramProb("JJ") == 1 / float(7))

    def test_bigramExistsWithCorrectProbabilities(self):
        # arrange
        utils = utilities.Utilities()
        rawSent = "Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ"
        sentence = utils.createTrigramTuplesFromStr(rawSent)

        hmm = hiddenMarkovTrigram.HiddenMarkovTrigram({})

        # act
        hmm.addParsedLine(sentence)

        # assert
        self.assertTrue(hmm.getBigramProb("NNP", "NNP") == .5)
        self.assertTrue(hmm.getBigramProb("NNP", ",") == .5)

        self.assertTrue(hmm.getBigramProb(",", "CD") == 1)

        self.assertTrue(hmm.getBigramProb("CD", "NNS") == 1)

        self.assertTrue(hmm.getBigramProb("NNS", "JJ") == 1)

    def test_trigramExistsWithCorrectProbabilities(self):
        # arrange
        utils = utilities.Utilities()
        rawSent = "Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ"
        sentence = utils.createTrigramTuplesFromStr(rawSent)

        hmm = hiddenMarkovTrigram.HiddenMarkovTrigram({})

        # act
        hmm.addParsedLine(sentence)

        # assert
        self.assertTrue(hmm.getTrigramProb("NNP", "NNP", ",") == 1)

        self.assertTrue(hmm.getTrigramProb("NNP", ",", "CD") == 1)

        self.assertTrue(hmm.getTrigramProb(",", "CD", "NNS") == 1)

        self.assertTrue(hmm.getTrigramProb("CD", "NNS", "JJ") == 1)

    def test_correctProbabilitiesWithLambdas1(self):
        # arrange
        utils = utilities.Utilities()
        rawSent = "Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ something/NNP cool/NNP here/VB"
        sentence = utils.createTrigramTuplesFromStr(rawSent)
        hmm = hiddenMarkovTrigram.HiddenMarkovTrigram(unknownProbFile)
        hmm.addParsedLine(sentence)
        lambda1 = 0.05
        lambda2 = 0.8
        lambda3 = 0.15

        # act
        result = hmm.getSmoothedTrigramProbability("NNP", "NNP", ",", lambda1, lambda2, lambda3)

        # assert
        # print hmm.printHmmFormat(lambda1, lambda2, lambda3)

        trigramProb = hmm.getTrigramProb("NNP", "NNP", ",")
        bigramProb = hmm.getBigramProb("NNP", ",")
        unigramProb = hmm.getUnigramProb(",")

        expectedResult = lambda3 * trigramProb + lambda2 * bigramProb + lambda1 * unigramProb

        self.assertTrue(result == expectedResult, str(result) + " " + str(expectedResult))

    def test_correctEmissionProbabilityWhenNotZero(self):
        # arrange
        hmm = hiddenMarkovTrigram.HiddenMarkovTrigram({})

        # act
        result = hmm.calculateEmissionProb(5, 10, .3)

        # assert
        expectedResult = (float(5) / 10) * (1 - .3)
        self.assertTrue(result == expectedResult)

    def test_correctEmissionProbabilityWhenZero(self):
        # arrange
        hmm = hiddenMarkovTrigram.HiddenMarkovTrigram({})

        # act
        result = hmm.calculateEmissionProb(0, 10, .3)

        # assert
        expectedResult = .3
        self.assertTrue(result == expectedResult)

class HiddenMarkovBigramModelTest(unittest.TestCase):
    def test_firstSentence(self):
        # arrange
        utils = utilities.Utilities()
        sentence1 = utils.createBigramTuplesFromStr("Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ ,/, will/MD join/VB the/DT board/NN as/IN a/DT nonexecutive/JJ director/NN Nov./NNP 29/CD ./.")

        hmm = hiddenMarkovBigram.HiddenMarkovBigram()

        # act
        hmm.addParsedLine(sentence1)

        # assert 
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

        hmm = hiddenMarkovBigram.HiddenMarkovBigram()
        
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
        hmm = hiddenMarkovBigram.HiddenMarkovBigram()

        hmm.addTransition("N", "V")

        result = hmm.getTransition("V", "N")

        self.assertTrue(1 == result, str(result))

    def test_addParsedLineResult(self):
        # arrange
        testSent = "John/N likes/V Mary/N"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)
        hmm = hiddenMarkovBigram.HiddenMarkovBigram()

        # act
        hmm.addParsedLine(result)

        # assert
        self.assertTrue(hmm.init_line_num() == 1)
        self.assertTrue(hmm.emiss_line_num() == 3)
        self.assertTrue(hmm.trans_line_num() == 3)
        self.assertTrue(hmm.state_num() == 3, str(hmm.state_num()))
        self.assertTrue(hmm.sym_num() == 3, str(hmm.sym_num()))

    def test_printOutFeature(self):
        # arrange
        testSent = "John/N likes/V Mary/N"

        utils = utilities.Utilities()

        result = utils.createBigramTuplesFromStr(testSent)
        hmm = hiddenMarkovBigram.HiddenMarkovBigram()
        hmm.addParsedLine(result)

        # act
        printStr = hmm.printHmmFormat()

        # assert
        expectedResult = """state_num=3
sym_num=3
init_line_num=1
trans_line_num=3
emiss_line_num=3

\init
BOS\t1.0\t0.0

\\transition
V\tN\t1.0\t0.0
BOS\tN\t1.0\t0.0
N\tV\t0.5\t-0.301029995664



\emissions
V\tlikes\t1.0\t0.0
N\tJohn\t0.5\t-0.301029995664
N\tMary\t0.5\t-0.301029995664
"""
        self.assertTrue(str(len(printStr)) == str(len(expectedResult)), str(len(printStr)) + "-" + str(len(expectedResult)))



def main():
    unittest.main()

if __name__ == '__main__':
	main()
