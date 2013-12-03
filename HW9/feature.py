import utilities
import re
from sets import Set

class Feature:
	def __init__(self, wordTag, prevWordTag, prev2WordTag, nextWordTag, next2WordTag):
		# don't want to keep this around for entire lifetime of model
		utils = utilities.Utilities()
		self.isRareWord = False
		self.keptFeatures = []

		self.wordTag = wordTag

		self.setupAttr(utils, "cur", wordTag)
		self.setupAttr(utils, "prev", prevWordTag)
		self.setupAttr(utils, "next", nextWordTag)
		self.setupAttr(utils, "prev2", prev2WordTag)
		self.setupAttr(utils, "next2", next2WordTag)

		self.handle2TCases()
		self.handleEosBosCases()
		self.handleSufPrefCases()
		self.handleContainNum()
		self.handleContainCap()
		self.handleContainHyp()

	def handleContainNum(self):
		self.containNum = False
		numRegex = "[0-9]+"

		match = re.search(numRegex, self.curW)

		if match:
			self.containNum = True

	def handleContainCap(self):
		self.containCap = False
		capRegex = "[A-Z]+"

		match = re.search(capRegex, self.curW)

		if match:
			self.containCap = True

	def handleContainHyp(self):
		self.containHyp = False
		hypRegex = "[-]+"

		match = re.search(hypRegex, self.curW)

		if match:
			self.containHyp = True

	def handleSufPrefCases(self):
		self.suf = []
		self.pref = []
		
		curWLen = len(self.curW)
		maxPrexLen = 5

		if curWLen <= 4:
			maxPrexLen = curWLen - 1

		if maxPrexLen == 0:
			return

		# we want to get all the prefixes that are equal or less than 4
		for endIdx in range(1, maxPrexLen):
			self.pref.append(self.curW[:endIdx])

		# 'hello' ello llo lo o
		for endIdx in range(1, maxPrexLen):
			backIdx = curWLen - endIdx
			self.suf.append(self.curW[backIdx:])

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

	def reportRareWordHashSet(self):
		returnSet = Set()
		for i in range(0, len(self.pref)):
			returnSet.add("pref=%s" % self.pref[i])

		for i in range(0, len(self.suf)):
			returnSet.add("suf=%s" % self.suf[i])

		if self.containHyp:
			returnSet.add("containHyp")

		if self.containCap:
			returnSet.add("containUC")

		if self.containNum:
			returnSet.add("containNum")

		self.addHashSetForRareAndNonRare(returnSet)

		return returnSet

	def reportNonRareWordHashSet(self):
		set = Set()
		set.add("curW=%s" % self.curW)

		self.addHashSetForRareAndNonRare(set)

		return set

	def addHashSetForRareAndNonRare(self, set):
# taken off slide 11 on November 21st lecture
		set.add("prevT=%s" % self.prevT)
		set.add("prev2T=%s" % self.prev2T)

		set.add("prevW=%s" % self.prevW)
		set.add("prev2W=%s" % self.prev2W)
		set.add("nextW=%s" % self.nextW)
		set.add("next2W=%s" % self.next2W)

	def reportHashSet(self, rareWord):
		self.isRareWord = rareWord

		if rareWord:
			return self.reportRareWordHashSet()

		return self.reportNonRareWordHashSet()

	def replaceComma(self, strVal):
		return re.sub(",", "comma", strVal)

	def printSelf(self):
		strBuilder = self.replaceComma(self.curW) + " " + self.replaceComma(self.curT) + " "

		for keptFeature in self.keptFeatures:
			strBuilder = "%s %s 1 " % (strBuilder, self.replaceComma(keptFeature))

		return re.sub("\s+", " ", strBuilder)

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

	def setKeptFeatures(self, givenKeptFeaturesDict):
		# we already know if this is rare or not...
		hashSet = self.reportHashSet(self.isRareWord)

		for feature in hashSet:
			if feature in givenKeptFeaturesDict:
				self.keptFeatures.append(feature)

	@staticmethod
	def buildFeatures(strVal):
		utils = utilities.Utilities()
		lines = strVal.split('\n')
		features = []

		for line in lines:
			# split into words
			wordTags = line.split()

			for i in range(0, len(wordTags)):

				# get words
				prev2WordTag = utils.getModifiedWordTagTuple(wordTags, i, -2)
				prevWordTag = utils.getModifiedWordTagTuple(wordTags, i, -1)
				nextWordTag = utils.getModifiedWordTagTuple(wordTags, i, 1)
				next2WordTag = utils.getModifiedWordTagTuple(wordTags, i, 2)

				newFeature = Feature(wordTags[i], prevWordTag, prev2WordTag, nextWordTag, next2WordTag)

				features.append(newFeature)

		return features