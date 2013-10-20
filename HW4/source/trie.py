class Trie:
  
  def __init__(self):
    self._end = "#"


  def make_trie(self, words):
    root = dict()
#    print words.split()
    for word in words.split():
      current_dict = root
#      print current_dict
      for letter in word:
        current_dict = current_dict.setdefault(letter, {})
      current_dict = current_dict.setdefault(self._end, self._end)
    print root
#    print current_dict
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
 

