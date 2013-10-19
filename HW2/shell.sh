#! /bin/bash

sh ./test.sh $1 $2 1>fn1 2>fn2
python cleanout.py fn1 fn2

