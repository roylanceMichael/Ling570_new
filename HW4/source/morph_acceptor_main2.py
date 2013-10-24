import sys
import fsa
import utilities

def main():
	utils = utilities.Utilities()
	fsm = sys.argv[1]
	word_list = sys.argv[2]

	fsmReader = open(fsm)

	fsmText = ''
	fsmLines = fsmReader.readlines()

	for i in range(0, len(fsmLines)):
		fsmText = fsmText + fsmLines[i]

	fsaObj = fsa.Fsa()
	fsaObj.parse(fsmText.strip())

	wordListReader = open(word_list)
	wordListText = ''
	wordListLines = wordListReader.readlines()

	strBuilder = ''

	for i in range(0, len(wordListLines)):
		word = wordListLines[i].strip()
		spaceDelimitedWord = ''

		for j in range(0, len(word)):
			spaceDelimitedWord = spaceDelimitedWord + word[j] + " "
			
		result = fsaObj.returnMorphedOutput(spaceDelimitedWord)

		strBuilder = strBuilder + word + ' => ' + result + '\n'

	print strBuilder
	
if __name__ == '__main__':
	main()