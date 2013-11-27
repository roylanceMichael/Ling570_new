import re


class ProcessFile:
	def just_words(self, text):
		words = re.sub('[^a-zA-Z]', ' ', text)
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
#		print vectorDict
		return vectorDict

	def sortAndPrint(self, text):
		wordcount = self.frequency(text)
		strBuilder = ''
		for key in sorted(wordcount.iterkeys()):
			strBuilder = strBuilder + "%s %s " % (key, wordcount[key])
		return strBuilder
