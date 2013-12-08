from __future__ import division
import sys
import os
import process


### This file is here solely for the purpose of helping us think about the features. 
### If run, it creates a directory with different interesting data to look at and draw inspiration from. 
### To run from command line: python utilities.py ../examples/training/left ../examples/training/right
### Global dictionaries and a couple methods might be useful in pulling some actual data for the features. Then corresponding methods should be run before main_q3.py


class CreateDataFiles:
### here we create a bunch of files and dictionaries that we'll need for forming our feature vectors
	def __init__(self):
		leftDict = {}
		rightDict = {}
		leftDifference = {}
		rightDifference = {}
		self.uniqueLeft = {}
		self.uniqueRight = {}


	def makeDictFromDir(self, directory):
	### tool to make a {word : frequency} dict from the input directory
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


	def wordsThatDifferSignificantlyInFrequency(self, k):
	### F2: list of words that are three times more frequent than in the other
		for key in self.leftDict:
			if not key.isdigit():
				if key in self.rightDict and self.leftDict[key] > 5 and self.rightDict[key] > 5:
					kvalue = int(int(self.rightDict[key])/k)
					denom = int(self.leftDict[key]) + kvalue
					if (min(float(int(self.leftDict[key])/denom), float(kvalue/denom)) < 0.25 and
						key not in self.leftDifference):
						self.leftDifference[key] = self.leftDict[key]
						self.rightDifference[key] = self.rightDict[key]

		### dicts sorted according to frequency
		strBuilder = 'LEFT' + '\n' + self.sortAndPrint(self.leftDifference) + '\n' + 'RIGHT' + '\n' + self.sortAndPrint(self.rightDifference)
		return strBuilder
			

	def compareDicts(self, dict1, dict2):
	### F3: make dictionaries {word : frequency} for words that belong uniquely to one of the groups
		uniqueWords = {}
		for key in dict1:
			if key not in dict2 and dict1[key] > 1:
				uniqueWords[key] = dict1[key]
	
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

		### dictionaries of words that belong uniquely to one of the groups
		self.uniqueLeft = self.compareDicts(self.leftDict, self.rightDict)   
		self.uniqueRight = self.compareDicts(self.rightDict, self.leftDict)

		### dicts sorted according to frequency
		f3outL = open(os.path.join(outputDir, 'unique_words_left'), 'w')
                f3outL.write(self.sortAndPrint(self.uniqueLeft))
		f3outR = open(os.path.join(outputDir, 'unique_words_right'), 'w')
                f3outR.write(self.sortAndPrint(self.uniqueRight))

		k = self.compareSizeOfCorpora(leftDir, rightDir)  

		f2out = open(os.path.join(outputDir, 'words_different_frequency'), 'w')
                f2out.write(self.wordsThatDifferSignificantlyInFrequency(k))

	#	listLeft = makeListFromFile(wordsLeft)
	#	listRight = makeListFromFile(wordsRight)


	
if __name__ == '__main__':
       	CreateDataFiles().main()
