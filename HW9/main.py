import trainvoc
import sys


def main():
	procF = trainvoc.TrainVoc()

	iFile = sys.argv[1]
	
	inputF = open(iFile)
	
	text = inputF.read()
	print procF.sortAndPrint(text)

	inputF.close()



if __name__ == '__main__':
	main()
