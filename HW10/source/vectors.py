import os
import sys
import process


class CreateVectors:
	def __init__(self):
		self.outDict = {}


	def processDir(self, dirs, outputFileName):
		f1 = open(outputFileName, 'w')

		proc = process.ProcessFile()
		for eachDir in dirs:   # cycle through the list of directories
			filenames = os.listdir(eachDir)
			filenames.sort()
			n = len(filenames)
#			print n
			for i in range(0, n):
				inputFOutput = os.path.join(eachDir, filenames[i])   # create a path for each file
				f = open(inputFOutput)

			        text = f.read()

				result = proc.sortAndPrint(text)
				
			        f1.write("%s %s %s %s" % (inputFOutput, os.path.basename(eachDir), result, "\n"))
	
				f.close()
