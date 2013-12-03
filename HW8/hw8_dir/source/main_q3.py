import sys
import vectors


def main():

        vect = vectors.CreateVectors()
	if len(sys.argv) > 4:
		trainFile = sys.argv[1]
		testFile = sys.argv[2]
	        ratio = sys.argv[3]
	        dirs = sys.argv[4:]

		if float(ratio) < 0.0 or float(ratio) > 1.0:
			print 'ratio should be greater than 0 and less than 1'
			return

		vect.processDir(ratio, dirs, trainFile, testFile)



if __name__ == '__main__':
        main()             
