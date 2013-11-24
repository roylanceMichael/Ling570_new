import sys
import vectors


def main():
        vect = vectors.CreateVectors()
        ratio = sys.argv[3]

        dirs = sys.argv[4:]

	trainFile = sys.argv[1]

	testFile = sys.argv[2]
	
	result = vect.processDir(ratio, dirs, trainFile, testFile)



if __name__ == '__main__':
        main()             
