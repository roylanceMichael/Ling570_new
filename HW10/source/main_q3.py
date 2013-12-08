import sys
import os
import process
import process2


def main():
	procF = process.ProcessFile()
	proc2 = process2.Process2()

	featureFile = sys.argv[1]
	featF = open(featureFile)
	fs = featF.read()
#	print proc2.buildFeatureList(fs)

	label = sys.argv[3]

	iFile = sys.argv[2]
	
	inputF = open(iFile)
	
	text = inputF.read()
#	print inputF.name + ' ' + label + ' ' + procF.sortAndPrint(text)
	print inputF.name + ' ' + label + proc2.buildVector(fs, text)

	inputF.close()



if __name__ == '__main__':
	main()
