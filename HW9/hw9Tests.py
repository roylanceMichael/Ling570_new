import unittest
import trainvoc
import buildvectors
import utilities

class TrainVocTests(unittest.TestCase):
	def test_frequencyCount(self):
		# arrange
		trnvoc = trainvoc.TrainVoc()
		testStr = "something/PN somewhere/PN sunshine\/test/PZ"

		# act
		trnvoc.buildFrequency(testStr)

		# assert
		self.assertTrue(trnvoc.frequencyDict["something"] == 1)
		self.assertTrue(trnvoc.frequencyDict["somewhere"] == 1)
		self.assertTrue(trnvoc.frequencyDict["sunshine\/test"] == 1)

	def test_sortAndPrint(self):
		# arrange
		trnvoc = trainvoc.TrainVoc()
		testStr = """something/PN somewhere/PN sunshine\/test/PZ
		something/PR something/PZ sunshine\/test/PT"""

		# act
		reportedText = trnvoc.sortAndPrint(testStr)

		# assert
		lines = reportedText.split("\n")
		self.assertTrue(lines[0] == "something\t3")
		self.assertTrue(lines[1] == "sunshine\/test\t2")
		self.assertTrue(lines[2] == "somewhere\t1")

class BuildVectors(unittest.TestCase):
	def test_makeVectors(self):
		# arrange
		bv = buildvectors.BuildVectors()
		testStr = """something/PN somewhere/PN sunshine\/test/PZ
		something/PR something/PZ sunshine\/test/PT"""
		
		bv.buildFrequency(testStr)

		# act
		bv.collectRareWords(2)
		
		# assert
		self.assertTrue(len(bv.rareWords) == 1)
		self.assertTrue("somewhere" in bv.rareWords)

		self.assertTrue(len(bv.nonRareWords) == 2)
		self.assertTrue("something" in bv.nonRareWords)
		self.assertTrue("sunshine\/test" in bv.nonRareWords)

class UtilitiesTests(unittest.TestCase):
	def test_getWordPosTupleSimple(self):
		# arrange
		utils = utilities.Utilities()
		testStr = "sunshine/PT"

		# act
		wordPosTuple = utils.getWordPosTuple(testStr)

		# assert
		self.assertTrue(wordPosTuple[0] == "sunshine")
		self.assertTrue(wordPosTuple[1] == "PT")

	def test_getWordPosTupleComplex(self):
		# arrange
		utils = utilities.Utilities()
		testStr = "sunshine\/test/PT"

		# act
		wordPosTuple = utils.getWordPosTuple(testStr)

		# assert
		self.assertTrue(wordPosTuple[0] == "sunshine\/test")
		self.assertTrue(wordPosTuple[1] == "PT")

def main():
    unittest.main()

if __name__ == '__main__':
	main()