#! /bin/bash

python2.7 ./source/main_q5.py $1 $2 $3 $4

./create_vectors2.sh $1 $4/train.vectors.txt $2

./create_vectors2.sh $1 $4/test.vectors.txt $3

mallet import-file --input $4/train.vectors.txt --output $4/train.vectors

mallet import-file --input $4/test.vectors.txt --output $4/test.vectors --use-pipe-from $4/train.vectors

vectors2classify --training-file $4/train.vectors --testing-file $4/test.vectors --output-classifier $4/me.model --trainer MaxEnt > $4/me.stdout 2>$4/me.stderr
