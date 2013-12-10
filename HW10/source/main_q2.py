import sys
import vectors
import utilities

def main():

	vect = vectors.CreateVectors()   #vectors.CreateVectors()    # utilities.Frequencies()
	if len(sys.argv) > 1:
		outputFile = sys.argv[1]
		dirs = sys.argv[2:]
		vect.processDir(dirs, outputFile)

if __name__ == '__main__':
	main()
