import re
import sys
import process
import features

### Doing many things for q3 here; will have to be expanded with more features

class Process2(process.ProcessFile):
	def __init__(self, utils, dirNum):
		process.ProcessFile()
		self.dirNum = dirNum
		self.utils = utils
		freq = {}

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
		feat = features.Features(self.utils)
		return feat.findPrevalence(word)
	
	def F3(self, word):
	### F3 checks if the word is uniquely found in left of right training sets
		feat = features.Features(self.utils)
		return feat.checkIfUnique(word)


	def F4(self, bigram):
	### F4 checks if the bigram is uniquely found in left of right training sets
		feat = features.Features(self.utils)
		return feat.checkIfUniqueBigram(bigram)


	def loadVector(self, fs, word, nextWord):
	### choosing features that are active and running code for them; return vector - a list of values
	### can be optimized to avoid running it for each word - need to return a list of functions
		fList = self.buildFeatureList(fs)
		vector = []

		if 'F1' in fList:
			f1 = self.F1(word)
			vector.append(word + ' ' + str(f1))

		if 'F2' in fList and self.dirNum == 2:
			f2 = self.F2(word)

			if f2 != None:
				vector.append('prevalence1=%s' % str(f2[0]))
				vector.append('prevalence2=%s' % str(f2[1]))
			else:
				vector.append('prevalence1=none')
				vector.append('prevalence2=none')

		if 'F3' in fList:
			f3 = self.F3(word)
			vector.append('unique=' + str(f3))

		if 'F4' in fList:
			bigram = str(word + ' ' + nextWord)
			f4 = self.F4(bigram)
			vector.append('unique_bigram(' + bigram + ')=' + str(f4))
		
		return vector


	def buildVector(self, fs, text):
	### building vector for output
		self.freq = self.getFrequencies(text)
#		print self.freq	
		strBuilder = ''
                
		for i in range(0, len(self.just_words(text))-1):
			word = self.just_words(text)[i]
			nextWord = self.just_words(text)[i+1]
			vector = self.loadVector(fs, word, nextWord)
			strBuilder = strBuilder + '\n' + word + '\t' + ' '.join(vector)
		return strBuilder
		
