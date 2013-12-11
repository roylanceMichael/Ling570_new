from __future__ import division
import sys
import os
import process
import re


### This file is here mainly to help us think about the features. 
### If run, it creates a directory with different interesting data to look at and draw inspiration from. 
### To run from command line: python utilities.py ../examples/training/left ../examples/training/right
### Global dictionaries and a couple methods might be useful in pulling some actual data for the features. Then corresponding methods should be run before main_q3.py


class CreateDataFiles:
### here we create a bunch of files and dictionaries that we'll need for forming our feature vectors
	def __init__(self):
		self.labelDict = {}
		self.labelUniques = {}
		
		self.bigramLabelDict = {}
		self.uniqueBiLabelDict = {}

		self.labelDifference = {}

		self.k = 0

	def makeDictFromDir(self, directory):
	### tool to make a {word : frequency} dict from the input directory
		print directory
		filenames = os.listdir(directory)
		filenames.sort()
		text = ''

		for i in range(0, len(filenames)):
			inputFOutput = os.path.join(directory, filenames[i])   # create a path for each file
			f = open(inputFOutput)
			text = text + f.read()

		result = self.frequency(text)
		return result	

	def frequency(self, text):
		unigramDict = {}
		bigramDict = {}
		words = self.just_words(text)

		for i in range(1, len(words)):
			prevWord = words[i-1]
			word = words[i]

			# uni first
			if word in unigramDict:
				unigramDict[word] += 1
			else:
				unigramDict[word] = 1

			bigramKey = prevWord + ' ' + word

			if bigramKey in bigramDict:
				bigramDict[bigramKey] += 1
			else:
				bigramDict[bigramKey] = 1

		return (unigramDict, bigramDict)


	def just_words(self, text):
		words = re.sub('[^0-9a-zA-Z-]', ' ', text)
		words = words.lower()
		listall = words.split()
		return listall

	def compareSizeOfCorpora(self, dir1, dir2):
	### F2: we will need to check by what coefficient one corpus is larger than the other
        	filenames1 = os.listdir(dir1)
	        n1 = len(filenames1)
        	filenames2 = os.listdir(dir2)
	        n2 = len(filenames2)

        	if n2 > n1:
                	k = float(round(n2 / n1, 3))
	        return k


	def sortAndPrint(self, dic):
	### turn a dict into a tuple and sort by key in descending order
        	top_sort = sorted(dic.items(), key = lambda a: -a[1]) # make into tuple and sort
	        strBuilder = ''
        	for tup in top_sort:  # slice of list
                	strBuilder = strBuilder + "%s %s %s %s" % (tup[0], '\t', tup[1], '\n')
	        return strBuilder


	def wordsThatDifferSignificantlyInFrequency(self, firstKey, secondKey):
	### F2: list of words that are three times more frequent than in the other
		self.labelDifference[firstKey] = {}
		self.labelDifference[secondKey] = {}

		for key in self.labelDict[firstKey]:
			if not key.isdigit():
				if key in self.labelDict[secondKey] and self.labelDict[firstKey][key] > 5 and self.labelDict[secondKey][key] > 5:

					kvalue = int(int(self.labelDict[secondKey][key])/self.k)
					denom = int(self.labelDict[firstKey][key]) + kvalue
					
					if (min(float(int(self.labelDict[firstKey][key])/denom), float(kvalue/denom)) < 0.25 and
						key not in self.labelDifference[firstKey]):

						self.labelDifference[firstKey][key] = self.labelDict[firstKey][key]
						self.labelDifference[secondKey][key] = self.labelDict[secondKey][key]

		### dicts sorted according to frequency
		strBuilder = 'LEFT' + '\n' + self.sortAndPrint(self.labelDifference[firstKey]) + '\n' + 'RIGHT' + '\n' + self.sortAndPrint(self.labelDifference[secondKey])
		return strBuilder
			

	def compareDicts(self, dict1, dict2):
	### F3: make dictionaries {word : frequency} for words that belong uniquely to one of the groups
		uniqueWords = {}
		for key in dict1:
			if key not in dict2 and dict1[key] > 1:
				uniqueWords[key] = dict1[key]
	
		return uniqueWords

	def compareDictsMultiple(self, firstDict, otherDicts):
		uniqueWords = {}
		for key in firstDict:
			uniqueWord = True
			
			for otherDict in otherDicts:
				if key in otherDict:
					uniqueWord = False
					break

			if uniqueWord:
				uniqueWords[key] = firstDict[key]

		return uniqueWords


	def makeListFromFile(self, filename):
	### F4: for reading in word lists
		f = open(filename)
		test = f.read()
	        f.close()
	        listall = text.split()
	        return result


	def checkAgainstTheWordList(self, curW, listW):
	### F4: see if current word is in word list
		if curW in listW:
			markedSide = 1

		return markedSide

	def buildDataStructures(self, dirs):

		for labelDir in dirs:
			resultTuple = self.makeDictFromDir(labelDir)
			self.labelDict[labelDir] = resultTuple[0]
			self.bigramLabelDict[labelDir] = resultTuple[1]


		print 'got done building the two dictionaries' 

		for primaryKey in self.labelDict:
			dictForLabel = self.labelDict[primaryKey]
			
			otherDicts = []
			
			for otherKey in self.labelDict:
				if otherKey != primaryKey:
					otherDicts.append(self.labelDict[otherKey])

			# { "../examples/training/left": { "testing": 1, "something": 2 }, "../examples/training/right": { "barney": 1, "where": 2}}
			self.labelUniques[primaryKey] = self.compareDictsMultiple(dictForLabel, otherDicts)


		print 'got done building unigram compare dicts'

		for primaryKey in self.bigramLabelDict:
			dictForLabel = self.bigramLabelDict[primaryKey]

			otherDicts = []

			for otherKey in self.bigramLabelDict:
				if otherKey != primaryKey:
					otherDicts.append(self.bigramLabelDict[otherKey])

			self.uniqueBiLabelDict[primaryKey] = self.compareDictsMultiple(dictForLabel, otherDicts)

		print 'got done building bigram compare dicts'

		if len(dirs) == 2:
			self.k = self.compareSizeOfCorpora(dirs[0], dirs[1])
			self.wordsThatDifferSignificantlyInFrequency(dirs[0], dirs[1])

		print 'got done building frequency stuff'
	
if __name__ == '__main__':
       	CreateDataFiles().main()
