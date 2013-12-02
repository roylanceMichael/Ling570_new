import unittest
import trainvoc
import buildvectors
import utilities
import feature

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
	def test_collectRareWords(self):
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

	def test_buildInitFeatures(self):
		# arrange
		bv = buildvectors.BuildVectors()
		testStr = """something/PN somewhere/PN sunshine\/test/PZ something/PR something/PZ sunshine\/test/PT"""
		
		bv.buildFrequency(testStr)
		bv.collectRareWords(2)

		# act
		bv.buildInitFeaturesFromTraining(testStr)
		
		# assert
		# somewhere and sunshine will report this
		self.assertTrue(bv.initFeatures["prevT=PN"] == 2)
		self.assertTrue(bv.initFeatures["prevW=something"] == 3)
		self.assertTrue(bv.initFeatures["prevW=sunshine\/test"] == 1)
		self.assertTrue(bv.initFeatures["curW=something"] == 3)

	def test_buildKeptFeatures(self):
		# arrange
		bv = buildvectors.BuildVectors()
		testStr = """something/PN somewhere/PN sunshine\/test/PZ something/PR something/PZ sunshine\/test/PT"""
		
		bv.buildFrequency(testStr)
		bv.collectRareWords(2)
		bv.buildInitFeaturesFromTraining(testStr)

		# act
		bv.buildKeptFeatures(2)
		
		# assert
		# somewhere and sunshine will report this
		self.assertTrue(len(bv.keptFeatures) == 2)
		self.assertTrue(bv.keptFeatures["prevW=something"] == 3)
		self.assertTrue(bv.keptFeatures["curW=something"] == 3)

	def test_buildKeptFeaturesTestForActualFeatures(self):
		# arrange
		bv = buildvectors.BuildVectors()
		testStr = """something/PN somewhere/PN sunshine\/test/PZ something/PR something/PZ sunshine\/test/PT"""
		
		bv.buildFrequency(testStr)
		bv.collectRareWords(2)
		bv.buildInitFeaturesFromTraining(testStr)

		# act
		bv.buildKeptFeatures(2)
		
		# assert
		# somewhere and sunshine will report this
		self.assertTrue(len(bv.trainFeatureVectors) == 6)
		
		self.assertTrue(len(bv.trainFeatureVectors[0].keptFeatures) == 1)
		self.assertTrue(bv.trainFeatureVectors[0].keptFeatures[0] == "curW=something")
		
		self.assertTrue(len(bv.trainFeatureVectors[1].keptFeatures) == 1)
		self.assertTrue(bv.trainFeatureVectors[1].keptFeatures[0] == "prevW=something")

		self.assertTrue(len(bv.trainFeatureVectors[2].keptFeatures) == 0)
		
		self.assertTrue(len(bv.trainFeatureVectors[3].keptFeatures) == 1)
		self.assertTrue(bv.trainFeatureVectors[3].keptFeatures[0] == "curW=something")

		self.assertTrue(len(bv.trainFeatureVectors[4].keptFeatures) == 2)
		self.assertTrue(bv.trainFeatureVectors[4].keptFeatures[0] == "prevW=something")
		self.assertTrue(bv.trainFeatureVectors[4].keptFeatures[1] == "curW=something")

		self.assertTrue(len(bv.trainFeatureVectors[5].keptFeatures) == 1)
		self.assertTrue(bv.trainFeatureVectors[5].keptFeatures[0] == "prevW=something")

class FeatureTests(unittest.TestCase):
	def test_buildsBOSCorrectly(self):
		# arrange
		bv = buildvectors.BuildVectors()
		testStr = """something/PN somewhere/PN sunshine\/test/PZ
		something/PR something/PZ sunshine\/test/PT"""

		# act
		features = feature.Feature.buildFeatures(testStr)

		# assert
		self.assertTrue(len(features) == 6)
		firstFeature = features[0]

		self.assertTrue(firstFeature.prevW == "BOS", firstFeature.prevW)
		self.assertTrue(firstFeature.prevT == "BOS")
		self.assertTrue(firstFeature.prev2W == "BOS")
		self.assertTrue(firstFeature.prev2T == "BOS+BOS")

	def test_buildsEOSCorrectly(self):
		# arrange
		testStr = """something/PN somewhere/PN sunshine\/test/PZ
		something/PR something/PZ sunshine\/test/PT"""

		# act
		features = feature.Feature.buildFeatures(testStr)

		# assert
		self.assertTrue(len(features) == 6)
		lastFeature = features[5]

		self.assertTrue(lastFeature.nextW == "EOS")
		self.assertTrue(lastFeature.nextT == "EOS")
		self.assertTrue(lastFeature.next2W == "EOS")
		self.assertTrue(lastFeature.next2T == "EOS+EOS")

	def test_buildsMiddleTuplesCorrectly(self):
		# arrange
		testStr = """something/PN somewhere/PN sunshine\/test/PZ something/PR something/PZ sunshine\/test/PT"""

		# act
		features = feature.Feature.buildFeatures(testStr)

		# assert
		self.assertTrue(len(features) == 6)
		# should be something/PR
		fourthFeature = features[3]

		self.assertTrue(fourthFeature.prevW == "sunshine\/test", fourthFeature.prevW)
		self.assertTrue(fourthFeature.prevT == "PZ")
		self.assertTrue(fourthFeature.prev2W == "somewhere")
		self.assertTrue(fourthFeature.prev2T == "PN+PZ", fourthFeature.prev2T)

		self.assertTrue(fourthFeature.nextW == "something")
		self.assertTrue(fourthFeature.nextT == "PZ")
		self.assertTrue(fourthFeature.next2W == "sunshine\/test")
		self.assertTrue(fourthFeature.next2T == "PZ+PT", fourthFeature.next2T)

	def test_checksMiddleForHyphen(self):
		# arrange
		testStr = """something/PN somewhere/PN sunshine\/test/PZ someth-ing/PR something/PZ sunshine\/test/PT"""

		# act
		features = feature.Feature.buildFeatures(testStr)

		# assert
		self.assertTrue(len(features) == 6)
		# should be something/PR
		fourthFeature = features[3]

		self.assertTrue(fourthFeature.containHyp == True)
		self.assertTrue(fourthFeature.containCap == False)
		self.assertTrue(fourthFeature.containNum == False)

	def test_checksMiddleForCap(self):
		# arrange
		testStr = """something/PN somewhere/PN sunshine\/test/PZ somethAing/PR something/PZ sunshine\/test/PT"""

		# act
		features = feature.Feature.buildFeatures(testStr)

		# assert
		self.assertTrue(len(features) == 6)
		# should be something/PR
		fourthFeature = features[3]

		self.assertTrue(fourthFeature.containHyp == False)
		self.assertTrue(fourthFeature.containCap == True)
		self.assertTrue(fourthFeature.containNum == False)

	def test_checksMiddleForNum(self):
		# arrange
		testStr = """something/PN somewhere/PN sunshine\/test/PZ someth9ing/PR something/PZ sunshine\/test/PT"""

		# act
		features = feature.Feature.buildFeatures(testStr)

		# assert
		self.assertTrue(len(features) == 6)
		# should be something/PR
		fourthFeature = features[3]

		self.assertTrue(fourthFeature.containHyp == False)
		self.assertTrue(fourthFeature.containCap == False)
		self.assertTrue(fourthFeature.containNum == True)

	def test_checksMiddleForPrefSuf(self):
		# arrange
		testStr = """something/PN somewhere/PN sunshine\/test/PZ someth9ing/PR something/PZ sunshine\/test/PT"""

		# act
		features = feature.Feature.buildFeatures(testStr)

		# assert
		self.assertTrue(len(features) == 6)
		# should be something/PR
		fourthFeature = features[3]

		self.assertTrue(len(fourthFeature.pref) == 2)
		self.assertTrue(len(fourthFeature.suf) == 2)
		self.assertTrue(fourthFeature.pref[0] == "s")
		self.assertTrue(fourthFeature.pref[1] == "o")
		self.assertTrue(fourthFeature.suf[0] == "g")
		self.assertTrue(fourthFeature.suf[1] == "n")

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