import sys
import os
import process
import process2
import utilities


def main():
	if len(sys.argv) > 1:

		featureFile = sys.argv[1]
		featF = open(featureFile)
		fs = featF.read()

		outputFile = sys.argv[2]

		dirs = sys.argv[3:]

		utils = utilities.CreateDataFiles()

		f1 = open(outputFile, 'w')

		allDirs = []
		for eachDir in dirs:   # cycle through the list of directories
			subdirs = os.walk(eachDir).next()[1]

			if len(subdirs) > 0:
				for subdir in subdirs:
					allDirs.append(os.path.join(eachDir, subdir))
			else:
				allDirs.append(eachDir)

		# print 'our list'+ str(allDirs)
				
		utils.buildDataStructures(allDirs)

		proc2 = process2.Process2(utils, len(allDirs))
			
		for eachSubdir in allDirs:

			filenames = os.listdir(eachSubdir)
			filenames.sort()

			n = len(filenames)

			for i in range(0, n):
				inputFOutput = os.path.join(eachSubdir, filenames[i])   # create a path for each file
				f = open(inputFOutput)
		
				text = f.read()

				result = proc2.buildVector(fs, text)

				f1.write("%s %s %s %s" % (inputFOutput, os.path.basename(eachSubdir), result, "\n"))

				f.close()

				print 'finished with file # ' + str(i) + ' out of ' + str(n)

if __name__ == '__main__':
	main()
