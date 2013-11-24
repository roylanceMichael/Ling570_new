import os
import sys
import process


class CreateVectors:
	def __init__(self):
	### training and testing portions as dictionaries
		self.trainDict = {}
		self.testDict = {}


	def processDir(self, ratio, dirs, trainFileName, testFileName):
		f1 = open(trainFileName, 'w')
		f2 = open(testFileName, 'w')

		proc = process.ProcessFile()
		for eachDir in dirs:   # cycle through the list of directories
			filenames = os.listdir(eachDir)
			n = float(len(filenames))
#			print n
#			print float(ratio)
			trainNum = round(float(ratio) * n)
			trainNum = int(round(trainNum))
#			print trainNum 
			for i in range(0, trainNum):
				inputFTrain = os.path.join(eachDir, filenames[i])   # create a path for each file
				f = open(inputFTrain)
				line = f.readline()
				while len(line.strip()) > 0:
			                line = f.readline()

			        text = f.read()

				result = proc.sortAndPrint(text)
				
#				match = re.search()
				
			        f1.write("%s %s %s %s" % (inputFTrain, os.path.basename(eachDir), result, "\n"))
	
				f.close()

			for j in range(trainNum + 1, len(filenames)):

				inputFTest = os.path.join(eachDir, filenames[j])
				f = open(inputFTest)
			        line = f.readline()
                                while len(line.strip()) > 0:
                                        line = f.readline()

                                text = f.read()

				result = proc.sortAndPrint(text)
			
			        f2.write("%s %s %s %s" % (inputFTest, os.path.basename(eachDir), result, "\n"))
  				
				f.close()


	def printTrainDict(self):
		
		strBuilder = ''
                for key in sorted(self.trainDict.iterkeys()):
                        strBuilder = strBuilder + "%s %s " % (key, self.trainDict[key])
                return strBuilder
			
	def printTestDict(self):
		
		strBuilder = ''
                for key in sorted(self.testDict.iterkeys()):
                        strBuilder = strBuilder + "%s %s " % (key, self.testDict[key])
                return strBuilder
