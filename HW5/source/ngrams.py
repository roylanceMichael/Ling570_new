import sys
import re


class NGrams:
#  def __init__(self):
#    self.sentence = ""

  def BOS_EOS(self, text):
    text = re.sub(r'^', '<s> ', text, flags=re.MULTILINE)
    text = re.sub(r'$', ' </s>', text, flags=re.MULTILINE)
    
    return text


  def count_unigrams(self, text):
    list_all = self.BOS_EOS(text)
    uni_dict = {}
    for token in list_all.split():
    #  print token
      if not token in uni_dict:
        uni_dict[token] = 1
      else:
        uni_dict[token] = uni_dict[token] + 1
    sort_dict = sorted(uni_dict.items(), key = lambda a: -a[1])
    return sort_dict
   

  def count_bigrams(self, text):
    list_all = self.BOS_EOS(text)
    t = list_all.split()
#    print t
    bi_dict = {} 
    for i in range(0, len(t)-2):
      #print t[i] + ' ' + t[i+1]
      bigram = t[i] + ' ' + t[i+1]
      if not bigram in bi_dict and not t[i] == '</s>':
        bi_dict[bigram] = 1
      elif t[i] == '</s>':
        continue
      else:
        bi_dict[bigram] = bi_dict[bigram] + 1

    sort_dict = sorted(bi_dict.items(), key = lambda a: -a[1])
    return sort_dict 
   

  def count_trigrams(self, text):
    list_all = self.BOS_EOS(text)
    t = list_all.split()
#    print t
    tri_dict = {}
    for i in range(0, len(t)-3):
#      print t[i] + ' ' + t[i+1] + ' ' + t[i+2]
      trigram = t[i] + ' ' + t[i+1] + ' ' + t[i+2]
      if not trigram in tri_dict and not (t[i] == '</s>' or t[i+1] == '</s>'):
        tri_dict[trigram] = 1
      elif (t[i] == '</s>' or t[i+1] == '</s>'):
        continue
      else:
        tri_dict[trigram] = tri_dict[trigram] + 1

    sort_dict = sorted(tri_dict.items(), key = lambda a: -a[1])
    return sort_dict
 
