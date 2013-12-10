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
#	print proc2.buildFeatureList(fs)

		outputFile = sys.argv[2]

		dirs = sys.argv[3:]

		utils = utilities.CreateDataFiles()
		utils.buildDataStructures(dirs)

		proc2 = process2.Process2(utils, len(dirs))

		f1 = open(outputFile, 'w')

    	for eachDir in dirs:   # cycle through the list of directories
			filenames = os.listdir(eachDir)
			filenames.sort()
			n = len(filenames)

			for i in range(0, n):
				inputFOutput = os.path.join(eachDir, filenames[i])   # create a path for each file
				f = open(inputFOutput)

				text = f.read()

				result = proc2.buildVector(fs, text)

				f1.write("%s %s %s %s" % (inputFOutput, os.path.basename(eachDir), result, "\n"))

				f.close()


if __name__ == '__main__':
	main()
