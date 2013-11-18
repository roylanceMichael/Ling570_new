import convert
import sys


def main():
	conv = convert.Convert()
	
	for line in sys.stdin:   # read line by line from stdin
		print conv.wordTag(line)



if __name__ == '__main__':
	main()
