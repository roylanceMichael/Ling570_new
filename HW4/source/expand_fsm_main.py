import sys
import fsa
import utilities

def main():
	utils = utilities.Utilities()
	lexiconFile = sys.argv[1]
	morphRulesFile = sys.argv[2]

	lexiconReader = open(lexiconFile)
	morphRulesReader = open(morphRulesFile)

	lexiconText = ''
	lexiconLines = lexiconReader.readlines()
	
	for i in range(0, len(lexiconLines)):
		lexiconText = lexiconText + lexiconLines[i]

	morphRulesText = ''
	morphRulesLines = morphRulesReader.readlines()
	
	for i in range(0, len(morphRulesLines)):
		morphRulesText = morphRulesText + morphRulesLines[i]

	# print lexiconText

	fsaObj = fsa.Fsa()
	fsaObj.parse(morphRulesText)
	lexiconVals = utils.readLexicon(lexiconText)
	fsaObj.parseLexicon(lexiconVals)

	print fsaObj.processCarmelFormatExpandedOutput()
	
if __name__ == '__main__':
	main()