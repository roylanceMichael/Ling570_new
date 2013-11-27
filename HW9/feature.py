import utilities

class Feature:
	def __init__(self, wordTag, prevWordTag, prev2WordTag, nextWordTag, next2WordTag):
		# don't want to keep this around for entire lifetime of model
		utils = utilities.Utilities()
		self.featureDict = {}

		self.wordTag = wordTag

		self.setupAttr(utils, "cur", wordTag)
		self.setupAttr(utils, "prev", prevWordTag)
		self.setupAttr(utils, "next", nextWordTag)
		self.setupAttr(utils, "prev2", prev2WordTag)
		self.setupAttr(utils, "next2", next2WordTag)

		self.handle2TCases()
		self.handleEosBosCases()

		#TODO: tests around hyphens, caps, numbers, suffixes or prefixes...

	def handle2TCases(self):
		# rules for handling prev2T and next2T
		if self.prev2T != None:
			self.prev2T = self.prev2T + "+" + self.prevT

		if self.next2T != None:
			self.next2T = self.nextT + "+" + self.next2T


	def handleEosBosCases(self):
		# special rules to handle BOS and EOS
		if self.prevT == None:
			self.prevT = "BOS"
			self.prevW = "BOS"
		
		if self.prev2T == None:
			self.prev2T = "BOS+BOS"
			self.prev2W = "BOS"

		if self.nextT == None:
			self.nextT = "EOS"
			self.nextW = "EOS"

		if self.next2T == None:
			self.next2T = "EOS+EOS"
			self.next2W = "EOS"

	def printSelf(self):
		strBuilder = ""

		if(self.curW != None):
			strBuilder = strBuilder + "curW=" + self.curW + " " 
		
		if(self.prevW != None):
			strBuilder = strBuilder + "prevW=" + self.prevW + " "
		if(self.prevT != None):
			strBuilder = strBuilder + "prevT=" + self.prevT + " " 
		if(self.prev2W != None):
			strBuilder = strBuilder + "prev2W=" + self.prev2W + " "
		if(self.prev2T != None):
			strBuilder = strBuilder + "prev2T=" + self.prev2T + " " 
		
		if(self.nextW != None):
			strBuilder = strBuilder + "nextW=" + self.nextW + " "
		if(self.nextT != None):
			strBuilder = strBuilder + "nextT=" + self.nextT + " " 
		if(self.next2W != None):
			strBuilder = strBuilder + "next2W=" + self.next2W + " "
		if(self.next2T != None):
			strBuilder = strBuilder + "next2T=" + self.next2T + " " 

		return strBuilder


	def setupAttr(self, utils, key, strVal):
		if(strVal == None):
			setattr(self, key + "W", None)
			setattr(self, key + "T", None)
			return

		wordTagTuple = utils.getWordPosTuple(strVal)

		if(wordTagTuple != None):
			setattr(self, key + "W", wordTagTuple[0])
			setattr(self, key + "T", wordTagTuple[1])
			return
		
		setattr(self, key + "W", None)
		setattr(self, key + "T", None)

	@staticmethod
	def buildFeatures(strVal):
		lines = strVal.split('\n')
		features = []

		for line in lines:
			# split into words
			wordTags = line.split()

			for i in range(0, len(wordTags)):

				# get words
				prev2WordTag = Feature.getModifiedWordTagTuple(wordTags, i, -2)
				prevWordTag = Feature.getModifiedWordTagTuple(wordTags, i, -1)
				nextWordTag = Feature.getModifiedWordTagTuple(wordTags, i, 1)
				next2WordTag = Feature.getModifiedWordTagTuple(wordTags, i, 2)

				newFeature = Feature(wordTags[i], prevWordTag, prev2WordTag, nextWordTag, next2WordTag)

				features.append(newFeature)

		return features

	@staticmethod
	def getModifiedWordTagTuple(wordTags, index, modifier):
		modifiedIndex = index + modifier
		
		# make sure we're within bounds
		if len(wordTags) > modifiedIndex and modifiedIndex > -1:
			return wordTags[modifiedIndex]

		return None