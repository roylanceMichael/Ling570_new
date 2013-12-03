from sets import Set
import feature
import trainvoc
import sys
import re
import utilities

class BuildVectors(trainvoc.TrainVoc):
	def __init__(self):
		trainvoc.TrainVoc.__init__(self)
		self.utils = utilities.Utilities()
		self.rareWords = Set()
		self.initFeatures = {}
		self.keptFeatures = {}
		self.trainFeatureVectors = []
		self.testFeatureVectors = []

	def collectRareWords(self, rare_thresh):
	# run this second
		for word in self.frequencyDict:
			if(self.frequencyDict[word] < rare_thresh):
				self.rareWords.add(word)

	def buildInitFeaturesFromTraining(self, strVal):
	# run this third
		lines = strVal.split('\n')
		features = []
		numSent = 0

		for line in lines:
			numWord = 0
			numSent += 1
			# split into words
			wordTags = line.split()

			for i in range(0, len(wordTags)):

				# get words
				prev2WordTag = self.utils.getModifiedWordTagTuple(wordTags, i, -2)
				prevWordTag = self.utils.getModifiedWordTagTuple(wordTags, i, -1)
				nextWordTag = self.utils.getModifiedWordTagTuple(wordTags, i, 1)
				next2WordTag = self.utils.getModifiedWordTagTuple(wordTags, i, 2)

				newFeature = feature.Feature(wordTags[i], prevWordTag, prev2WordTag, nextWordTag, next2WordTag)

				wordTagTuple = self.utils.getWordPosTuple(wordTags[i])

				reportSet = Set()

				# set if rareword
				if wordTagTuple != None and wordTagTuple[0] in self.rareWords:
					reportSet = newFeature.reportHashSet(True)
				else:
					reportSet = newFeature.reportHashSet(False)

				self.trainFeatureVectors.append((newFeature, numSent, numWord))

				for feat in reportSet:
					if feat in self.initFeatures:
						self.initFeatures[feat] = self.initFeatures[feat] + 1
					else:
						self.initFeatures[feat] = 1

				numWord += 1

	def buildKeptFeatures(self, featFreq):
		for key in self.initFeatures:
			if self.initFeatures[key] > featFreq:
				self.keptFeatures[key] = self.initFeatures[key]

		# update features to have just the kept features
		for trainFeatureTuple in self.trainFeatureVectors:
			trainFeatureTuple[0].setKeptFeatures(self.keptFeatures)

	def buildTestFeatures(self, testFeaturesStr):
		# run this last
		lines = testFeaturesStr.split('\n')
		features = []
		numSent = 0

		for line in lines:
			numWord = 0
			numSent += 1
			
			# split into words
			wordTags = line.split()

			for i in range(0, len(wordTags)):

				# get words
				prev2WordTag = self.utils.getModifiedWordTagTuple(wordTags, i, -2)
				prevWordTag = self.utils.getModifiedWordTagTuple(wordTags, i, -1)
				nextWordTag = self.utils.getModifiedWordTagTuple(wordTags, i, 1)
				next2WordTag = self.utils.getModifiedWordTagTuple(wordTags, i, 2)

				newFeature = feature.Feature(wordTags[i], prevWordTag, prev2WordTag, nextWordTag, next2WordTag)

				wordTagTuple = self.utils.getWordPosTuple(wordTags[i])

				reportSet = Set()

				# set if rareword
				if wordTagTuple != None and wordTagTuple[0] in self.rareWords:
					reportSet = newFeature.reportHashSet(True)
				else:
					reportSet = newFeature.reportHashSet(False)

				newFeature.setKeptFeatures(self.keptFeatures)
				self.testFeatureVectors.append((newFeature, numSent, numWord))

				numWord += 1

	### print functions
	def printFeatures(self, featureVectors):
		strBuilder = ""

		for featureTuple in featureVectors:
			strBuilder = "%s%s-%s-%s%s" % (strBuilder, featureTuple[1], featureTuple[2], featureTuple[0].printSelf(), "\n")

		return strBuilder

	def printTestFeatures(self):
		return self.printFeatures(self.testFeatureVectors)

	def printTrainingFeatures(self):
		return self.printFeatures(self.trainFeatureVectors)

	def printInitFeats(self):
		return self.printDict(self.initFeatures)

	def printKeptFeats(self):
		return self.printDict(self.keptFeatures)

	def printDict(self, dictToPrint):
		strBuilder = ''

		topSort = sorted(dictToPrint.items(), key=lambda x: -x[1])

		for tup in topSort:
			strBuilder = "%s %s %s %s" % (strBuilder, tup[0], tup[1], "\n")

		return strBuilder

	def makeVectors(self, text, rare_thresh):
	### I would like frequencyDict to be inherited globally from trainvoc

		lines = text.split('\n')   # take the text that we read in main and split it into sentences
		numSent = 0   # sentence counter we'll need for the output
		
		for line in lines:   # iterating through sentences
#			print line
			numSent += 1
			numWord = 0   # word counter we'll need for the output
			wordsAndTags = line.split()

#			print wordsAndTags
			for wordAndTag in wordsAndTags:	# iterating through words
				wordPosTuple = self.utils.getWordPosTuple(wordAndTag)

				if wordPosTuple == None:
					print 'Valid word/pos not found in ' + wordAndTag

				word = wordPosTuple[0]

				if word in self.frequencyDict: # theoretically, None should never be in freqDict
#					print str(word) + ':' + str(freqDict[word])
					if int(self.frequencyDict[word]) < int(rare_thresh):
						# rare word
						print word + '- rare word!'

					else:
						# normal word
						print word + '- normal word'

				else:
					print 'Valid word/pos found, but not in freqdict ' + wordAndTag             