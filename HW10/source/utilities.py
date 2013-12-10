from __future__ import division
import sys
import os
import process


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

		proc = process.ProcessFile()
        	for i in range(0, len(filenames)):
        		inputFOutput = os.path.join(directory, filenames[i])   # create a path for each file
	                f = open(inputFOutput)
        	        text = text + f.read()
                	result = proc.frequency(text)
		
		return result	

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


	def bigramFrequency(self, text):
		bigramDict = {}
		proc = process.ProcessFile()
		listAllWords = proc.just_words(text)
	        for i in range(0, len(listAllWords)-1):
			bigram = listAllWords[i] + ' ' + listAllWords[i+1]
                        if bigram in bigramDict:
                                bigramDict[bigram] += 1
                        else:
                                bigramDict[bigram] = 1
                return bigramDict


        def makeBigramDictFromDir(self, directory):
        ### tool to make a {word : frequency} dict from the input directory
                filenames = os.listdir(directory)
                filenames.sort()
                text = ''
                proc = process.ProcessFile()
                for i in range(0, len(filenames)):
                        inputFOutput = os.path.join(directory, filenames[i])   # create a path for each file
                        f = open(inputFOutput)
                        text = text + f.read()
                        result = self.bigramFrequency(text)
                return result
	

	def buildDataStructures(self, dirs):

		for labelDir in dirs:
			self.labelDict[labelDir] = self.makeDictFromDir(labelDir)
			self.bigramLabelDict[labelDir] = self.makeBigramDictFromDir(labelDir)

		for primaryKey in self.labelDict:
			dictForLabel = self.labelDict[primaryKey]
			
			otherDicts = []
			
			for otherKey in self.labelDict:
				if otherKey != primaryKey:
					otherDicts.append(self.labelDict[otherKey])

			# { "../examples/training/left": { "testing": 1, "something": 2 }, "../examples/training/right": { "barney": 1, "where": 2}}
			self.labelUniques[primaryKey] = self.compareDictsMultiple(dictForLabel, otherDicts)


		for primaryKey in self.bigramLabelDict:
			dictForLabel = self.bigramLabelDict[primaryKey]

			otherDicts = []

			for otherKey in self.bigramLabelDict:
				if otherKey != primaryKey:
					otherDicts.append(self.bigramLabelDict[primaryKey])

			self.uniqueBiLabelDict[primaryKey] = self.compareDictsMultiple(dictForLabel, otherDicts)

		if len(dirs) == 2:
			self.k = self.compareSizeOfCorpora(dirs[0], dirs[1])
			self.wordsThatDifferSignificantlyInFrequency(dirs[0], dirs[1])

	def main(self):
		leftDir = sys.argv[1]
		rightDir = sys.argv[2]
		outputDir = 'HelpfulDataFiles'

		if not os.path.exists(outputDir):       # create output directory
			os.makedirs(outputDir)

		### frequency dictionaries for each group
		self.leftDict = self.makeDictFromDir(leftDir)
		self.rightDict = self.makeDictFromDir(rightDir)

		f_out = open(os.path.join(outputDir, 'full_frequency_lists'), 'w')
		f_out.write('LEFT' + '\n' + self.sortAndPrint(self.leftDict) + '\n' + 'RIGHT' + '\n' + self.sortAndPrint(self.rightDict))

		### frequency dictionaries for bigrams
		self.bigramLeftDict = self.makeBigramDictFromDir(leftDir)
		self.bigramRightDict = self.makeBigramDictFromDir(rightDir)
		
		f4_out = open(os.path.join(outputDir, 'full_frequency_bigram_lists'), 'w')
		f4_out.write('LEFT' + '\n' + self.sortAndPrint(self.bigramLeftDict) + '\n' + 'RIGHT' + '\n' + self.sortAndPrint(self.bigramRightDict))
		
		### dictionaries of words that belong uniquely to one of the groups
		self.uniqueLeft = self.compareDicts(self.leftDict, self.rightDict)   
		self.uniqueRight = self.compareDicts(self.rightDict, self.leftDict)

		### dicts sorted according to frequency
		f3outL = open(os.path.join(outputDir, 'unique_words_left'), 'w')
		f3outL.write(self.sortAndPrint(self.uniqueLeft))
		f3outR = open(os.path.join(outputDir, 'unique_words_right'), 'w')
		f3outR.write(self.sortAndPrint(self.uniqueRight))

		### dictionaries of bigrams that belong uniquely to one of the groups
		self.uniqueBiLeft = self.compareDicts(self.bigramLeftDict, self.bigramRightDict)   
		self.uniqueBiRight = self.compareDicts(self.bigramRightDict, self.bigramLeftDict)
		
		### dicts sorted according to frequency
		f4outL = open(os.path.join(outputDir, 'unique_bigrams_left'), 'w')
		f4outL.write(self.sortAndPrint(self.uniqueBiLeft))
		f4outR = open(os.path.join(outputDir, 'unique_bigrams_right'), 'w')
		f4outR.write(self.sortAndPrint(self.uniqueBiRight))
		
		self.k = self.compareSizeOfCorpora(leftDir, rightDir)  

		f2out = open(os.path.join(outputDir, 'words_different_frequency'), 'w')
		f2out.write(self.wordsThatDifferSignificantlyInFrequency())

	#	listLeft = makeListFromFile(wordsLeft)
	#	listRight = makeListFromFile(wordsRight)


	
if __name__ == '__main__':
       	CreateDataFiles().main()
