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

  l = cfsa.readline()  
  match = re.search('\((\w+)\s*\(\w+', l)
  start = match.group(1)

  while l:
    l = l.translate(None, '"\n\t')
#    print l
    match = re.search('\((\w+)\s*\((\w+)\s*(\w+|\*e\*)', l)
    if match.group(1) not in fsmStates:
      fsmStates[match.group(1)] = [[match.group(3), match.group(2)]]
#      print match.group(3)
    else:
      fsmStates[match.group(1)].append([match.group(3), match.group(2)])

    l = cfsa.readline()

  return (fsmStates, start, final)


def generate_new_states(current_state, fsa, string):
  current_node = current_state[0]
  index = current_state[1]
  search_states = []
#  global fsa
  # make an *e*-transition
  for transition in fsa[current_node[1]]:
    if '*e*' in transition[0]:
      new_state = transition[1]
      search_states.append(transition)      

#  print search_states
  # make a transition to the next state
#  print current_node[1]
  new_state = current_node[1]
  if index+1 < len(string):
    for transition in fsa[new_state]:
    #  print transition
     # print string[index+1]
#      print transition[0]
      if string[index+1] in transition[0]:
        search_states.append(transition)
#  print search_states

  return search_states


def accept_state(search_state, length):
#  print search_state
#  global string
  current_node = search_state[0]
  index = search_state[1]  # should be the actual index; char for now
#  print search_state[1]
#  print string[index]
  if current_node[1] == final and index == length-1:
    return True
  if current_node[1] == final and current_node[0] == '*e*':
    return True
  else:
    return False



def main():

  fm = sys.argv[1] 
  f = open(fm, 'ru')
  exs = sys.argv[2]
  sts = open(exs, 'rU')

  fsa, start, final = make_fsa(f)

 # global string

  string = sts.readline()
#  print string

  while string:  # line 99
    string = string.translate(None, '" ')
    string = string.strip()
    length = len(string)
#    print length
    state = start
    i = 0
  
    listofstates = []
    for transition in fsa[state]:
      if string[i] in transition[0]:
        listofstates.append(transition)
#    if '*e*' in transition[0]:
 #     listofstates.append(transition)
      
    agenda = (listofstates, string[i])
#    print agenda

    agenda_index = 0
    while agenda_index < len(agenda[0]):
      next_on_agenda = agenda[0][agenda_index]
#    print next_on_agenda

      current_search_state = (next_on_agenda, i)

      if accept_state(current_search_state, length):
        print string, '=> yes!' # return accept
        break
      else:
#      print fsa[state]
        l = generate_new_states(current_search_state, fsa, string)
        for el in l:
          listofstates.append(el)
        agenda = (listofstates, i)
#    print len(agenda)[0]
   # print agenda_index

      if agenda_index == len(agenda[0])-1: # is empty
        print string, '=> no'
        break

      else:
        agenda_index += 1 #print 'no'
#  string = sts.readline()
#    for c in string:
#      print string, '=> yes'
    string = sts.readline()

  f.close()

  sts.close()


  
if __name__ == '__main__':
  main()
