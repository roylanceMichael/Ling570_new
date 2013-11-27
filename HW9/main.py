import trainvoc
import buildvectors
import sys


def main():
	procF = trainvoc.TrainVoc()
	vects = buildvectors.BuildVectors()

	iFile = sys.argv[1]
	
	### later adjust to sys.argv[3]
	rare_thresh = sys.argv[2]
	
	inputF = open(iFile)
	
	text = inputF.read()

	### we'll need to output this into ex_train_voc
	print procF.sortAndPrint(text)

	vects.makeVectors(text, rare_thresh, procF.frequencyDict)

	inputF.close()



if __name__ == '__main__':
	main()
