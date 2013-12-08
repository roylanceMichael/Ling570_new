import sys
import utilities


### Here we can flesh out the features, if it hasn't been done in other places already
### This is what I thought the vector may look like:
### word	F1(word frequency) F2(prevalentL=, prevalentR=), F3(unique=left/right), F4(markedWord=left/right), F5(pref=), F6(prev2W=)


class Features(utilities.CreateDataFiles):
	def __init__(self):
		utilities.CreateDataFiles.__init__(self)


	def checkIfUnique(self, curW):
	### used in F3; requires filled uniqueLeft and uniqueRight
		utils = utilities.CreateDataFiles()
		if curW in utils.uniqueLeft:
			unique = 'left'
		elif curW in utils.uniqueRight:
			unique = 'right'
		else: 
			unique = 'not'   # not sure if this should be output at all; maybe ignore alltogether?
		return unique
