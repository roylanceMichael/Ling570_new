import unittest
import utilities


class UtilitiesTest(unittest.TestCase):
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
                       
