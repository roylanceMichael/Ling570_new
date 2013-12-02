import trainvoc
import buildvectors
import sys
import os

def main():
	vects = buildvectors.BuildVectors()

	train_file = sys.argv[1]
	test_file = sys.argv[2]
	rare_thresh = sys.argv[3]
	feat_thresh = sys.argv[4]
	output_dir = sys.argv[5]

	if not os.path.exists(output_dir):       # create output directory
		os.makedirs(output_dir)

	train_file_input = open(train_file)
	train_file_text = train_file_input.read()

	### we'll need to output this into ex_train_voc
	train_voc_text = vects.sortAndPrint(train_file_text)

	f1out = open(os.path.join(output_dir, 'train_voc'), 'w')
	f1out.write(train_voc_text)

	vects.collectRareWords(int(rare_thresh))
	vects.buildInitFeaturesFromTraining(train_file_text)
	
	print 'printing init_feats '
	f2out = open(os.path.join(output_dir, 'init_feats'), 'w')
	f2out.write(vects.printInitFeats())
	print 'done printing init_feats'
	
	vects.buildKeptFeatures(int(feat_thresh))
	f3out = open(os.path.join(output_dir, 'kept_feats'), 'w')
	f3out.write(vects.printKeptFeats())
	print 'done printing kept_feats'

	f4out = open(os.path.join(output_dir, 'final_train.vectors.txt'), 'w')
	f4out.write(vects.printFeatures())
	print 'done printing train vectors'

	f1out.close()
	f2out.close()
	f3out.close()
	f4out.close()

if __name__ == '__main__':
	main()