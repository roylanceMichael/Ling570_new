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
	t = input_t.readline()

	while t:
		result = vit.processLineForwards(t)
		print t + " => " + vit.reportBestPath(result)
		t = input_t.readline()

if __name__ == '__main__':
	main()
