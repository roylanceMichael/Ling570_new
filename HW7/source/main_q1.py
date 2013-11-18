#!/usr/bin/python
import viterbi
import utilities
import sys

def main():
	# first is input_hmm
	# second is test_file

	vit = viterbi.Viterbi()
	hmmInputFile = sys.argv[1]
	input_t = open(hmmInputFile)
	t = input_t.readline()
	
	while t:
		vit.readInput(t)
		t = input_t.readline()

	testFile = sys.argv[2]
	input_t = open(testFile)
	t = input_t.readline().strip()

	while t:
		result = vit.processLine(t)

		# didn't process correctly, will return an error
		if(type(result) is str):
			print str(t + " => " + result).strip()

		# did process correctly
		else:
			strBuilder = " => "
			for word in result[1]:
				strBuilder = strBuilder + " " + word
			
			print str(t + strBuilder.strip() + " " + str(result[0])).strip()
		
		t = input_t.readline().strip()

if __name__ == '__main__':
	main()
