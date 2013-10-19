#!/usr/bin/python

import sys
import re
import os


def main():

#  fn1 = sys.argv[1]
  fn2 = sys.argv[2] 
  f2 = open(fn2, 'ru')
#  f1 = open(fn1, 'rU')

  l = f2.readline()
  while l:
#    print l
    match = re.search(':\s([\w\"\s]+)\n', l)
#    print match
#    if match:
#      print match.group(1)
    l = f2.readline()
    l = f2.readline()
#    print l
    if l[0:5] == "Input":
      print match.group(1), '=> yes'
    else:
      print match.group(1), '=> no' 
      l = f2.readline()


#  f1.close()
  f2.close()

#  for filename in list_of_files:  
#      total += 1

#  line = sys.stdin.readline()
#  while line:
#    print tokenize(line)
#    line = sys.stdin.readline()


  
if __name__ == '__main__':
  main()
