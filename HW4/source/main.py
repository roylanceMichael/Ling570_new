import sys
import fsa

def main():
	fstFile = sys.argv[1]
	userInput = sys.argv[2]

	fstReader = open(fstFile)
	userInputReader = open(userInput)

	fstText = ''
	fstLines = fstReader.readlines()
	
	for i in range(0, len(fstLines)):
		fstText = fstText + fstLines[i]

	# print fstText

	fsaObj = fsa.Fsa()
	fsaObj.parse(fstText)

	userInputLine = userInputReader.readline()
	while(userInputLine):
		cleansedLine = userInputLine.strip()
		#result = fsaObj.processInput(cleansedLine)
		#print result
		print cleansedLine + " => " + fsaObj.returnHighestProb(cleansedLine)
		userInputLine = userInputReader.readline()

if __name__ == '__main__':
	main()