import sys
import vectors


def main():

        vect = vectors.CreateVectors()
	if len(sys.argv) > 1:
		outputFile = sys.argv[1]
	        dirs = sys.argv[2:]

		vect.processDir(dirs, outputFile)



if __name__ == '__main__':
        main()             
