#! /bin/bash

python2.7 ./source/main.py $1 $2 $3 $4 $5

mallet import-file --input $5/final_train.vectors.txt --output $5/final_train.vectors

mallet import-file --input $5/final_test.vectors.txt --output $5/final_test.vectors --use-pipe-from $5/final_train.vectors

vectors2classify --training-file $5/final_train.vectors --testing-file $5/final_test.vectors --output-classifier $5/me_model --trainer MaxEnt > $5/me.stdout 2>$5/me.stderr
