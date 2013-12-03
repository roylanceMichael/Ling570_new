import sys
import process

def main():
	procF = process.ProcessFile()
	label = sys.argv[2]

	iFile = sys.argv[1]
	
	inputF = open(iFile)
	l = inputF.readline()
	while len(l.strip()) > 0:
		l = inputF.readline()
	
	text = inputF.read()
	print inputF.name + ' ' + label + ' ' + procF.sortAndPrint(text)

	inputF.close()



if __name__ == '__main__':
	main()
