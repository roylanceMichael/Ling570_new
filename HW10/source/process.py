import re


### this is an almost exact copy of our code in hw8


class ProcessFile:
	def just_words(self, text):
		words = re.sub('[^0-9a-zA-Z-]', ' ', text)
		words = words.lower()
		listall = words.split()
		return listall


	def frequency(self, text):
		vectorDict = {}
		for word in self.just_words(text):
			if word in vectorDict:
				vectorDict[word] += 1
			else:
				vectorDict[word] = 1
		return vectorDict


	def sortAndPrint(self, text):
		wordcount = self.frequency(text)
		strBuilder = ''
		for key in sorted(wordcount.iterkeys()):
			strBuilder = strBuilder + "%s %s " % (key, wordcount[key])
		return strBuilder
