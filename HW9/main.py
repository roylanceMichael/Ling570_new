import trainvoc
import buildvectors
import sys

def main():
	vects = buildvectors.BuildVectors()

	iFile = sys.argv[1]
	
	### later adjust to sys.argv[3]
	rare_thresh = sys.argv[2]
	
	inputF = open(iFile)
	
	text = inputF.read()

	### we'll need to output this into ex_train_voc
	print vects.sortAndPrint(text)

	vects.collectRareWords(int(rare_thresh))

	inputF.close()

if __name__ == '__main__':
	main()