#! /bin/bash

sh ./morph.sh $1 $2 1>fn1 2>fn2
python2.7 cleanout.py fn1 fn2 > $3

