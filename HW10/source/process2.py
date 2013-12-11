import re
import sys
import process
import features

### Doing many things for q3 here; will have to be expanded with more features

class Process2(process.ProcessFile):
	def __init__(self, utils, dirNum):
		process.ProcessFile()
		freq = {}
		self.dirNum = dirNum
		self.utils = utils
		self.feat = features.Features(utils)
		self.functionList = []

	def buildFeatureList(self, fs):
	### collecting a list features that are selected for each run
		usedFeatures = re.findall(r'(F\d+)=1', fs)
                return usedFeatures

	def getFrequencies(self, text):
	### {word:frequency} for the file
		return self.frequency(text)

	def F1(self, word):
	### F1 is the unigram feature - returns very high accuracies
		return self.freq[word]

	def F2(self, word):
	### look at the words that are present in both groups, but differ (significantly) in count
		return self.feat.findPrevalence(word)
	
	def F3(self, word):
	### F3 checks if the word is uniquely found in left of right training sets
		return self.feat.checkIfUnique(word)


	def F4(self, bigram):
	### F4 checks if the bigram is uniquely found in left of right training sets
		return self.feat.checkIfUniqueBigram(bigram)


#       def F5(self, bigram):
#       ### F5 should be the bigram feature - return frequency
#               print self.utils.frequency(bigram)
#               return self.utils.frequency[1](bigram)


	def generateFeatureFunctions(self, fs):
		if len(self.functionList) > 0:
			return

		fList = self.buildFeatureList(fs)

		functionList = []

		if 'F1' in fList:
			functionList.append(self.F1Wrapper)

		if 'F2' in fList and self.dirNum == 2:
			functionList.append(self.F2Wrapper)

		if 'F3' in fList:
			functionList.append(self.F3Wrapper)

		if 'F4' in fList:
			functionList.append(self.F4Wrapper)

#               if 'F5' in fList:
#                       functionList.append(self.F5Wrapper)

		self.functionList = functionList

		return self.functionList

	def F1Wrapper(self, word, vectorArray, nextWord):
		f1 = self.F1(word)
		vectorArray.append(word + ' ' + str(f1))

	def F2Wrapper(self, word, vectorArray, nextWord):
		f2 = self.F2(word)

		if f2 != None:
			vectorArray.append('prevalence1=%s' % str(f2[0]))
			vectorArray.append('prevalence2=%s' % str(f2[1]))
		else:
			return
#			vectorArray.append('prevalence1=none')
#			vectorArray.append('prevalence2=none')

	def F3Wrapper(self, word, vectorArray, nextWord):
		f3 = self.F3(word)
		if str(f3) != 'None':
			vectorArray.append('unique=' + str(f3))

	def F4Wrapper(self, word, vectorArray, nextWord):
		bigram = str(word + ' ' + nextWord)
		f4 = self.F4(bigram)
		if str(f4) != 'None':
			vectorArray.append('unique_bigram(' + bigram + ')=' + str(f4))


#       def F5Wrapper(self, word, vectorArray, nextWord):
#               bigram = str(word + ' ' + nextWord)
#               f5 = self.F5(bigram)
#               vectorArray.append(bigram + ' ' + str(f5))


	def buildVector(self, fs, text):
	### building vector for output
		self.freq = self.getFrequencies(text)
		self.generateFeatureFunctions(fs)

	#	print self.freq	
		strBuilder = ''

		allWords = self.just_words(text)

		for i in range(0, len(allWords)-1):
			word = allWords[i]
			nextWord = allWords[i+1]
			vectorArray = []
			
			for j in range(0, len(self.functionList)):
				self.functionList[j](word, vectorArray, nextWord)
			
			strBuilder = strBuilder + '\t' + word + '\t' + ' '.join(vectorArray)

		return strBuilder
		
