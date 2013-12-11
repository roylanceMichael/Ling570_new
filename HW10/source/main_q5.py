import sys
import os


def main():
	param_file = sys.argv[1]
	train_dir = sys.argv[2]
	test_dir = sys.argv[3]
	output_dir = sys.argv[4]

	if not os.path.exists(output_dir):       # create output directory
		os.makedirs(output_dir)

if __name__ == '__main__':
	main()