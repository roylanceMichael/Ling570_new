import sys
import vectors


def main():
        vect = vectors.CreateVectors()
        ratio = sys.argv[3]

        dirs = sys.argv[4:]

	result = vect.processDir(ratio, dirs)



if __name__ == '__main__':
        main()             
