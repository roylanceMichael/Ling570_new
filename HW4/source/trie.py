import fsa


class Trie:
  
  def __init__(self):
    self._end = "#"


  def make_trie(self, words):
    root = dict()
    for word in words.split():
      current_dict = root
#      print current_dict
      i = 0
      for letter in word:
        current_dict = current_dict.setdefault(letter, {})
      current_dict = current_dict.setdefault(self._end, self._end)
#    print root
    return root


  def in_trie(self, trie, word):
    current_dict = trie
    for letter in word:
      if letter in current_dict:
        current_dict = current_dict[letter]
      else:
        return False
    else:
      if self._end in current_dict:
        return True
      else:
        return False


  def make_fsm_trie(self, words):
    root = dict()
#    print words.split()
    fsa_lexItem = fsa.Fsa()   #
    fsa_lexItem.startState = "st0"   #
    i = 0
    for word in words.split():
      current_dict = root
      for letter in word:
        fsa_lexItem.transitionStates[i].value = letter   #
        fsa_lexItem.transitionStates[i].fromState = "st{}".format(i)  #
        fsa_lexItem.transitionStates[i].toState = "st{}".format(i+1)   #

        current_dict = current_dict.setdefault(letter, {})
        i += 1   #
      current_dict = current_dict.setdefault(self._end, self._end)
#    print root
    print fsa_lexItem   #
    return root
 

