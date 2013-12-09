import re
import sys
import process
import features

### Doing many things for q3 here; will have to be expanded with more features

class Process2(process.ProcessFile):
	def __init__(self, utils):
		process.ProcessFile()
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
#		print self.freq[word]
		return self.freq[word]

	
	def F3(self, word):
	### F3 checks if the word is uniquely found in left of right training sets
	### does not work properly yet; need to run compareDicts or make sure global dicts in utilities.py are filled
		feat = features.Features(self.utils)
		return feat.checkIfUnique(word)


	def loadVector(self, fs, word):
	### choosing features that are active and running code for them; return vector - a list of values
	### can be optimized to avoid running it for each word - need to return a list of functions
		fList = self.buildFeatureList(fs)
		vector = []
		if 'F1' in fList:
			f1 = self.F1(word)
			vector.append(word + ' ' + str(f1))
		if 'F2' in fList:
			f2 = self.F2(word)
			vector.append(f2)
		if 'F3' in fList:
			f3 = self.F3(word)
			vector.append('unique=' + str(f3))
		return vector


	def buildVector(self, fs, text):
	### building vector for output
		self.freq = self.getFrequencies(text)
#		print self.freq	
		strBuilder = ''
                
		for word in self.just_words(text):
			vector = self.loadVector(fs, word)
			strBuilder = strBuilder + '\n' + word + '\t' + ' '.join(vector)
		return strBuilder
		
