#!/opt/python-2.7/bin/python2.7

#Created on 7 Oct, 2013
#author: Olga Whelan

import sys
import re
import os


def main():

  fn2 = sys.argv[2] 
  f2 = open(fn2, 'ru')

  l = f2.readline()
  while l:
#    print l
    match = re.search(':\s([\w\"\s]+)\n', l)   # extracting the input string
#    print match
    string = re.sub(' ', '', match.group(1))
    l = f2.readline()
    l = f2.readline()
    if l[0:5] == "Input":
      print string, '=> yes'
    else:
      print string, '=> no' 
      l = f2.readline()

  f2.close()


  
if __name__ == '__main__':
  main()
