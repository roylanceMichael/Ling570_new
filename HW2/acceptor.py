#!/opt/python-2.7/bin/python2.7

import sys
import re
import os


def make_fsa(filename):
  cfsa = filename

  fsmStates = {'not accepted':[]}

  l = cfsa.readline()
  final = l.strip()
#  print final
  fsmStates[final] = []
#  print fsmStates

#  l = cfsa.readline()  

  l = cfsa.readline()
  match = re.search('\((\w+)\s*\(\w+', l)
  start = match.group(1)
#  print start

  while l:
    l = l.translate(None, '"')
#    print l  
    match = re.search('\((\w+)\s*\((\w+)\s*(\w+|\*e\*)', l)
    if match.group(1) not in fsmStates:
      fsmStates[match.group(1)] = [[match.group(3), match.group(2)]]
#      print match.group(3)
    else:
      fsmStates[match.group(1)].append([match.group(3), match.group(2)])
#      print match.group(3)

    l = cfsa.readline()

  return (fsmStates, start, final)



def main():

#  fn1 = sys.argv[1]
  fm = sys.argv[1] 
  f = open(fm, 'ru')
  exs = sys.argv[2]
  sts = open(exs, 'rU')

  fsa, start, final = make_fsa(f)
  print fsa
#  print fsa[final]
  print start
  print final

  string = sts.readline()
  while string:

#    print string
    state = start
#    print string
    string = string.translate(None, '" ')
    string = string.strip()
#    print len(string)

    for c in string:
      for tr in fsa[state]:
        if c in tr[0]:
          state = tr[1]
          break
      else:
        state = 'not accepted'
#      print state
#    i = 0 
#    while i< len(fsa[state]):
 #     i += 1
#    for c in string:
#    i = 0
#    print string[len(string)-1]
###    for c in string:
#      print fsa[state].values()
#          print 'problem'
#          state = 'not accepted'
#        print transition[0], '>', transition[1]
#        print string[i]
#          state = transition[1]
#          i += 1
#      else: state = 'not accepted'
#      if c not in fsa[state]:
#        print string, '=> no'
#        break
#      if state == final: #and c in fsa[final][0]:
#      else:
#    print fsa[final][0]
#    print i
#    print string[len(string)-1]
#    print string[i]
    if state == final:
      print string, '=> yes'
    else: print string, '=> no'     

    string = sts.readline()

  f.close()

  sts.close()


  
if __name__ == '__main__':
  main()
