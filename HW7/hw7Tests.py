import unittest
import utilities
import viterbi


class ViterbiTest(unittest.TestCase):
	def test_getPrevPathState(self):
		# arrange
		VitInput = 'a'
		VitTest = viterbi.Viterbi()
#		VitDict = utilities.Utilities()
#		VitDict.current_symb_dict = {'a': {'DT': 0.1, 'N': 1.0}, 'the': {'DT': 0.7}}

		# act
		actualResult = VitTest.GetPrevPathState(VitInput)
#		print actualResult

		# assert
		self.assertTrue(actualResult == ['DT', 'N'])


        def test_getPrevPathProb(self):
                # arrange
                VitInput = ['DT', 'N']
                VitTest = viterbi.Viterbi()
#                VitDict = utilities.Utilities()
 #               VitDict.current_trans_dict = {'BOS': {'N': 1.0}, 'N': {'D': 0.5, 'V': 0.4}}

                # act
                actualResult = VitTest.GetPrevPathProb(VitInput)
#                print actualResult

                # assert
                self.assertTrue(actualResult == 1.0)


        def test_getMaxProbEmittingState(self):
                # arrange
                VitProb = 1.0
                VitTest = viterbi.Viterbi()
#                VitDict = utilities.Utilities()
#                VitDict.current_trans_dict = {'BOS': {'N': 1.0}, 'N': {'D': 0.5, 'V': 0.4}}

                # act
                actualResult = VitTest.GetPrevPathProb(VitProb)
#                print actualResult

                # assert
                self.assertTrue(actualResult == 'N')





class Utilities(unittest.TestCase):
    def test_movesToEmissVals1(self):
        # arrange
        hmmInput = """state_num=6
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

\emission
DT  the 0.7
DT  a   0.1
N   a   1.0""".split("\n")

        hmmFactory = utilities.Utilities()

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
#        self.assertTrue(hmmFactory.currentState == hmmFactory.emiss_state, hmmFactory.currentState)
#        self.assertTrue(hmmFactory.current_emiss_dict["DT"]["the"] == 0.7)
#        self.assertTrue(hmmFactory.current_emiss_dict["DT"]["a"] == 0.1)
                                                                                                                    
        self.assertTrue(hmmFactory.current_symb_dict["the"]["DT"] == 0.7)
        self.assertTrue(hmmFactory.current_symb_dict["a"]["DT"] == 0.1)


def main():
    unittest.main()

if __name__ == '__main__':
        main()
                       
