import utilities
import re
from sets import Set

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
		if curWLen > 0:
			self.suf.append(self.curW[curWLen-1])
			self.pref.append(self.curW[0])

		if curWLen > 1:
			self.suf.append(self.curW[curWLen-2])
			self.pref.append(self.curW[1])

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
			returnSet.add("containCap")

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
		if rareWord:
			return self.reportRareWordHashSet()

		return self.reportNonRareWordHashSet()

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