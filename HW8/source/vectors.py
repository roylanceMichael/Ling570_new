import os
import sys


class CreateVectors:
	def __init__(self):
	### training and testing portions as strings
		self.trainText = ''
		self.testText = ''


	def processDir(self, ratio, dirs):
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
				self.trainText = self.trainText + f.read()
				
				f.close()

			for j in range(trainNum + 1, len(filenames)):
				inputFTest = os.path.join(eachDir, filenames[j])
				f = open(inputFTest)
				self.testText = self.testText + f.read()   # building the test string
				print self.testText

				f.close()

			
