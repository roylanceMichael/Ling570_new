#!/opt/python-2.7/bin/python2.7

import sys
import re
import os

final = '0'
#string = 0
#fsa = {}


def make_fsa(filename):
  cfsa = filename
#  global fsa
  fsmStates = {} #{'not accepted':[]}

  global final
  l = cfsa.readline()
  final = l.strip()
  fsmStates[final] = []
#  print fsmStates
#  print len(l)

  l = cfsa.readline()  
  match = re.search('\((\w+)\s*\(\w+', l)
  start = match.group(1)
#  print start
#  print final
#  print l
#  print len(l)
  while l:
#    print len(l)
    l = l.translate(None, '"\n\t')
 #   print l, len(l)
    match = re.search('\((\w+)\s*\((\w+)\s*(\w+|\*e\*)', l)
  #  print match.group(1)
   # print fsmStates
    if (match.group(1)) not in fsmStates:
      fsmStates[match.group(1)] = [[match.group(3), match.group(2)]]
#      print match.group(3)
    else:
      fsmStates[match.group(1)].append([match.group(3), match.group(2)])

    l = cfsa.readline()

  return (fsmStates, start, final)


def generate_new_states(current_state, fsa, string):
  current_node = current_state[0]
  print 'current_node', current_node
  index = current_state[1]
  print string[index], index
  search_states = []
#  global fsa
  # make an *e*-transition
#  print fsa[current_node[1]]
 ## if current_node[1] in fsa:
   ## for transition in fsa[current_node[1]]:
     ## if '*e*' in transition[0]:
       ## new_state = transition[1]
       ## search_states.append([transition, index])      
##    print 'for new search:', search_states
  
#  print search_states


#def generate_new_states(current)
  # make a transition to the next state
#  print current_node[1]
  new_state = current_node[1]
  print 'new state', new_state
  if index+1 < len(string) and new_state in fsa:
    print fsa[new_state]
    for transition in fsa[new_state]:
   #   print fsa[new_state]
    #  print transition
      print string[index+1]
#      print transition[0]
      if string[index+1] in transition[0]:
        search_states.append(transition)
  print 'return to agenda', search_states[0]

  return search_states


def accept_state(search_state, length):
  print 'SearchState', search_state
#  global string
  current_node = search_state[0][1]
  index = search_state[1]  # should be the actual index; char for now
  print 'search state: ', search_state[0][1]
  print 'index in string:', index
#  print length
  if current_node == final and index == length-1: #or search_state[0][0] == '*e*'):
    return True
#  if current_node == final and search_state[0][0] == '*e*':
#    return True
  else:
    return False



def main():

  fm = sys.argv[1] 
  f = open(fm, 'ru')
  exs = sys.argv[2]
  sts = open(exs, 'rU')

  fsa, start, final = make_fsa(f)
  print fsa
  print start
 # print final
 # global string

  string = sts.readline()
 # print string

  while string:  # line 99
    string = string.translate(None, '" ')
    string = string.strip()
    length = len(string)
#    print length
  #  print string
    state = start
    i = 0
  
    listofstates = []
    for transition in fsa[state]:
      if string[i] in transition[0]:
        listofstates.append(transition)
      if '*e*' in transition[0]:
        listofstates.append(transition)
      
    agenda = (listofstates, string[i])
    print '\n'
    print agenda
    print agenda[0]
    if not agenda[0]:
      print string, '=> no'
      print '\n'

    agenda_index = 0
    print len(agenda[0])
    while agenda_index < len(agenda[0]):
      next_on_agenda = agenda[0][agenda_index]
      print next_on_agenda

      current_search_state = (next_on_agenda, i)
      print 'CSS', current_search_state
      if accept_state(current_search_state, length):
        print string, '=> yes!' # return accept
        print '\n'
        break
      else:
#      print fsa[state]
        listofstates.append(generate_new_states(current_search_state, fsa, string))
#        for news in newss:
#          listofstates.append(news)
        agenda = (listofstates[0], i+1)
        print 'Last agenda:', agenda
#    print len(agenda)[0]
      print agenda_index

      if not agenda[0][agenda_index]: # == len(agenda[0])-1: # is empty
        print string, '=> no'
        print '\n'
        break

      else:
        agenda_index += 1 #print 'no'
        print agenda_index
#  string = sts.readline()
#    for c in string:
#      print string, '=> yes'
    string = sts.readline()

  f.close()

  sts.close()


  
if __name__ == '__main__':
  main()
